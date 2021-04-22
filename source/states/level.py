from ..components import info
import pygame
from .. import tools, setup
from .. import constants as C
from .. components import player, stuff
import os
import json


class Level:
    # def __init__(self):
    #     pygame.mixer.init()

    def start(self, game_info):  # 被tools文件update在切换阶段时调用
        self.game_info = game_info
        self.finished = False
        self.check_win = False
        self.next = 'game_over'  # 设置下一阶段
        self.info = info.Info('level', self.game_info)  # 传入关卡信息
        self.load_map_data()  # 载入第一关里的地图json文件数据
        self.setup_background()  # 载入游戏背景
        self.setup_music()  # 载入音乐
        self.setup_start_positions()  # 设置游戏开始的位置
        self.setup_player()  # 载入游戏角色
        self.setup_ground_items()  # 设置碰撞

    def load_map_data(self):  # 被start调用
        file_name = 'level_1.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)  # 将读取的json数据赋值给map_data

    def setup_background(self):  # 载入游戏的背景
        self.image_name = self.map_data['image_name']  # 将第一关json地图名称赋值给image_name
        self.background = setup.GRAPHICS[self.image_name]  # 载入地图的图片给background
        rect = self.background.get_rect()  # 获取地图矩形 为下一步放缩用
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.BG_MULTI),  # 放缩地图图片
                                                                   int(rect.height * C.BG_MULTI)))
        self.background_rect = self.background.get_rect()  # 获取放缩后的地图矩形
        self.game_window = setup.SCREEN.get_rect()  # 赋值游戏窗口
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))  # 游戏地图图层

    def setup_start_positions(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
        self.start_x, self.end_x, self.player_x, self.player_y = self.positions[0]  # 将游戏地图开始的位置和游戏人物开始的位置赋值

    def setup_player(self):
        self.player = player.Player('mario')  # 创建player文件下的Player实例
        self.player.rect.x = self.game_window.x + self.player_x  # 人物初始坐标在相对初始窗口的初始位置上
        self.player.rect.bottom = self.player_y  # 人物y坐标在初始y上

    def setup_ground_items(self):
        self.ground_items_group = pygame.sprite.Group()  # 创建精灵组批量处理地图中的物品
        for name in ['ground', 'pipe', 'step']:  # 遍历json中字典的ground pipe 和 step
            for item in self.map_data[name]:  # 遍历对应地图数据里的各个物品
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))  # 加入组中

    def setup_music(self):
        pygame.mixer.music.load('resources/music/level_BGM.wav')
        pygame.mixer.music.play(start=0.0)

    def update(self, surface, keys):  # 被tools文件update调用进入level阶段
        self.current_time = pygame.time.get_ticks()  # 获取当前时间
        self.player.update(keys)  # 调用player文件中update 处理按键对应的状态
        if self.player.dead:
            if self.current_time - self.player.death_timer > 1600:
                pygame.mixer.music.stop()
                self.finished = True  # 进入下一个状态 game over
                self.update_game_info()  # 调用方法
        else:
            self.update_player_position()
            self.check_if_go_die()
            self.update_game_window()
        self.draw(surface)

    def update_player_position(self):
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x  # 到达地图边缘时禁止通过
            self.next = 'game_over'  # ------------ 到达终点后的临时解决办法
            pygame.mixer.music.stop()
            self.check_win = True
            self.finished = True
        self.check_x_collisions()  # x方向碰撞检测

        self.player.rect.y += self.player.y_vel
        self.check_y_collisions()  # y方向碰撞检测

    def check_x_collisions(self):
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)  # 检测是否碰撞
        if ground_item:
            self.adjust_player_x(ground_item)  # 防止碰撞

    def check_y_collisions(self):
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)  # 检测是否碰撞
        if ground_item:
            self.adjust_player_y(ground_item)  # 防止碰撞
        self.check_will_fall(self.player)  # 检查是否需要下落

    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0

    def adjust_player_y(self, sprite):
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'

    def check_will_fall(self, sprite):
        sprite.rect.y += 1  # 试探性的进行检验是否要下落 将人物位置下调一个像素
        check_group = pygame.sprite.Group(self.ground_items_group)
        collided = pygame.sprite.spritecollideany(sprite, check_group)  # 检测是否与地图物品碰撞
        if not collided and sprite.state != 'jump':  # 没有碰撞且不在跳跃状态
            sprite.state = 'fall'  # 进入下落状态
        sprite.rect.y -= 1  # 恢复为了试探而下调的像素

    def update_game_window(self):  # 角色在前三分之一的窗口处可以自由移动
        third = self.game_window.x + self.game_window.width / 3
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.end_x:
            self.game_window.x += self.player.x_vel
            self.start_x = self.game_window.x

    def draw(self, surface):
        self.game_ground.blit(self.background, self.game_window, self.game_window)  # 画游戏环境
        self.game_ground.blit(self.player.image, self.player.rect)  # 画人物角色
        surface.blit(self.game_ground, (0, 0), self.game_window)
        self.info.draw(surface)

    def check_if_go_die(self):  # 被update调用
        if self.player.rect.y > C.SCREEN_H:  # 掉出地图外
            pygame.mixer.music.stop()
            self.player.go_die()

    def update_game_info(self):  # 被update调用
        if self.player.dead:  # 当角色处于死亡状态
            self.game_info['lives'] -= 1  # 生命减一
        if self.game_info['lives'] == 0:  # 生命为0时
            self.next = 'game_over'  # 下一状态改为game over
        else:
            self.next = 'load_screen'  # 还有生命就继续进入加载阶段


