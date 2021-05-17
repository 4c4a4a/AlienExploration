from ..components import info
import pygame


class LoadScreen:
    """游戏加载界面，游戏正在进行"""
    def start(self, game_info):
        """游戏初始化设置，游戏信息、状态时钟、状态标志、下一状态信息"""
        self.game_info = game_info
        self.finished = False
        self.next = 'level'
        self.duration = 2000  # 阶段持续时间间隔
        self.timer = 0
        self.info = info.Info('load_screen', self.game_info)

    def update(self, surface, keys):
        """加载界面刷新函数"""
        self.draw(surface)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished = True
            self.timer = 0

    def draw(self, surface):
        """画图刷新函数"""
        surface.fill((29, 22, 38))
        self.info.draw(surface)


class GameOver(LoadScreen):
    """游戏加载画面，游戏结束"""
    def start(self, game_info):
        """游戏初始化设置，游戏信息、状态时钟、下一状态"""
        self.game_info = game_info
        self.finished = False
        self.next = 'main_menu'
        self.duration = 2000
        self.timer = 0
        self.info = info.Info('game_over', self.game_info)


class Win(LoadScreen):
    """游戏加载画面，游戏胜利"""
    def start(self, game_info):
        """游戏初始化设置，游戏信息、状态时钟、下一状态、游戏背景音乐"""
        self.game_info = game_info
        self.finished = False
        self.next = 'main_menu'
        self.duration = 4650
        self.timer = 0
        self.setup_music()  # 载入音乐
        self.info = info.Info('win', self.game_info)

    def setup_music(self):
        """播放游戏背景音乐"""
        pygame.mixer.music.load('resources/music/win_BGM.wav')
        pygame.mixer.music.play(start=0.0)

