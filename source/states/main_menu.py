import pygame
import tkinter
from .. import setup
from .. import tools
from .. import constants as C
from ..components import info
from tkinter import messagebox


class MainMenu:
    """游戏主菜单"""
    def __init__(self):
        """初始化主菜单对象"""
        game_info = {
            'lives': 3,
        }
        pygame.mixer.init()
        self.start(game_info)

    def start(self, game_info):
        """更多初始化设置，游戏信息、画面显示、游戏音乐、状态标志、下一状态信息"""
        self.game_info = game_info
        self.setup_background()
        self.setup_player()
        self.setup_music()
        self.info = info.Info('main_menu', self.game_info)
        self.finished = False
        self.next = 'load_screen'  # 下一个状态

    def setup_background(self):
        """创建主菜单背景及标题画面"""
        self.background = setup.GRAPHICS['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTI),
                                                                   int(self.background_rect.height * C.BG_MULTI)))
        self.viewport = setup.SCREEN.get_rect()
        self.caption = tools.get_image(setup.GRAPHICS['title_screen'], 1, 60, 176, 88, (255, 0, 220), C.BG_MULTI)

    def setup_player(self):
        """创建主菜单角色画面"""
        self.player_image = tools.get_image(setup.GRAPHICS['Gagarin'], 178, 32, 12, 16, (0, 0, 0), C.PLAYER_MULTI)

    def setup_music(self):
        """创建主菜单背景音乐"""
        pygame.mixer.music.load('resources/music/main_menu_BGM.wav')
        pygame.mixer.music.play(start=0.0)

    def update_cursor(self, keys):
        """按键处理刷新函数"""
        key = sum(keys)
        if keys[pygame.K_RETURN]:
            pygame.mixer.music.stop()
            self.reset_game_info()
            self.finished = True
        elif ~keys[pygame.K_RETURN] and key >= 1:
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showinfo("提示", "请按回车开始游戏!")
            root.destroy()

    def update(self, surface, keys):
        """主菜单刷新函数"""
        self.update_cursor(keys)
        surface.blit(self.background, self.viewport)  # 画出主菜单背景
        surface.blit(self.caption, (170, 100))        # 画出标题
        surface.blit(self.player_image, (110, 490))   # 画出角色
        self.info.draw(surface)

    def reset_game_info(self):
        """游戏信息重置"""
        self.game_info.update({
            'lives': 3,
        })

