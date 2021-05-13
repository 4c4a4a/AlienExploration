from ..components import info
import pygame


class LoadScreen:
    def start(self, game_info):
        self.game_info = game_info  # 设置游戏幅值
        self.finished = False  # 设置游戏阶段为未完成
        self.next = 'level'  # 下一阶段为正式关卡
        self.duration = 2000  # 阶段持续时间间隔
        self.timer = 0  # 计时器
        self.info = info.Info('load_screen', self.game_info)  # 传入当前阶段和游戏信息

    def update(self, surface, keys):  # 被tools中update调用
        self.draw(surface)  # 调用draw方法
        if self.timer == 0:  # 检测时间间隔
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished = True
            self.timer = 0

    def draw(self, surface):  # 画图
        surface.fill((0, 0, 0))  # 创建填满颜色的图层
        self.info.draw(surface)  # 在图层上绘画


class GameOver(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'main_menu'
        self.duration = 2000
        self.timer = 0
        self.info = info.Info('game_over', self.game_info)

class Win(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'main_menu'
        self.duration = 4650
        self.timer = 0
        self.setup_music()  # 载入音乐
        self.info = info.Info('win', self.game_info)

    def setup_music(self):
        pygame.mixer.music.load('resources/music/win_BGM.wav')
        pygame.mixer.music.play(start=0.0)

