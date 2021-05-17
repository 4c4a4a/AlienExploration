import pygame
import os
import json
from .. import tools, setup
from .. import constants as C
from ..components import info
from ..components import player, stuff


class Level:
    """游戏关卡"""
    def start(self, game_info):
        """游戏初始化设置，游戏信息、状态标志、下一状态、地图数据、背景音乐、游戏人物、地图碰撞"""
        self.game_info = game_info
        self.finished = False
        self.next = 'game_over'
        self.info = info.Info('level', self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_music()
        self.setup_start_positions()
        self.setup_player()
        self.setup_ground_items()

    def load_map_data(self):
        """加载游戏地图"""
        file_name = 'level_1.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

    def setup_background(self):
        """加载游戏背景画面"""
        self.image_name = self.map_data['image_name']
        self.background = setup.GRAPHICS[self.image_name]
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.BG_MULTI),
                                                                   int(rect.height * C.BG_MULTI)))
        self.background_rect = self.background.get_rect()
        self.game_window = setup.SCREEN.get_rect()
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))

    def setup_start_positions(self):
        """加载游戏人物、画面起点"""
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
        self.start_x, self.end_x, self.player_x, self.player_y = self.positions[0]

    def setup_player(self):
        """加载游戏人物"""
        self.player = player.Player('Gagarin')
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

    def setup_ground_items(self):
        """加载游戏中物品，地面、柱体、阶梯"""
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground', 'pipe', 'step']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def setup_music(self):
        """加载游戏背景音乐"""
        pygame.mixer.music.load('resources/music/level_BGM.wav')
        pygame.mixer.music.play(start=0.0)

    def update(self, surface, keys):
        """关卡刷新函数"""
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys)
        if self.player.dead:  # 角色死亡处理
            if self.current_time - self.player.death_timer > 1600:
                pygame.mixer.music.stop()
                self.finished = True
                self.update_game_info()
        else:                 # 正常刷新
            self.update_player_position()
            self.check_if_go_die()
            self.update_game_window()
        self.draw(surface)

    def update_player_position(self):
        """角色位置刷新"""
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
            self.next = 'win'
            pygame.mixer.music.stop()
            self.finished = True
        self.check_x_collisions()
        self.player.rect.y += self.player.y_vel
        self.check_y_collisions()

    def check_x_collisions(self):
        """检测x轴碰撞"""
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        if ground_item:
            self.adjust_player_x(ground_item)

    def check_y_collisions(self):
        """检测y轴碰撞"""
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        if ground_item:
            self.adjust_player_y(ground_item)
        self.check_will_fall(self.player)

    def adjust_player_x(self, sprite):
        """x轴碰撞处理"""
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0

    def adjust_player_y(self, sprite):
        """y轴碰撞处理"""
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'

    def check_will_fall(self, sprite):
        """角色下落检测，试探法"""
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group)
        collided = pygame.sprite.spritecollideany(sprite, check_group)
        if not collided and sprite.state != 'jump':
            sprite.state = 'fall'
        sprite.rect.y -= 1

    def update_game_window(self):
        """游戏画面跟随刷新"""
        third = self.game_window.x + self.game_window.width / 3
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.end_x:
            self.game_window.x += self.player.x_vel
            self.start_x = self.game_window.x

    def draw(self, surface):
        """绘制游戏画面"""
        self.game_ground.blit(self.background, self.game_window, self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)
        surface.blit(self.game_ground, (0, 0), self.game_window)
        self.info.draw(surface)

    def check_if_go_die(self):
        """检测角色死亡"""
        if self.player.rect.y > C.SCREEN_H:
            pygame.mixer.music.stop()
            self.player.go_die()

    def update_game_info(self):
        """游戏信息刷新"""
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next = 'game_over'
        else:
            self.next = 'load_screen'


