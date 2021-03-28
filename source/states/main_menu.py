import pygame
from .. import setup
from .. import tools
from .. import constants as C
from ..components import info


class MainMenu:
    def __init__(self):
        game_info = {
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'small'
        }
        self.start(game_info)  # 初始化实例便调用start方法 传入游戏初始信息

    def start(self, game_info):  # 实例创建时初始化调用
        self.game_info = game_info  # 游戏信息赋值
        self.setup_background()  # 调用创建游戏背景方法
        self.setup_player()  # 创建人物
        # self.setup_cursor()  # 创建光标
        self.info = info.Info('main_menu', self.game_info)  # 创建info文件里的Info实例
        self.finished = False  # 标志开始菜单是否完成的标志 True即进入下一个状态 即加载页面
        self.next = 'load_screen'  # 设置下一个状态

    def setup_background(self):  # 创建背景
        self.background = setup.GRAPHICS['level_1']
        self.background_rect = self.background.get_rect()  # 获取背景矩形
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTI),  # 放大背景倍数
                                                                   int(self.background_rect.height * C.BG_MULTI)))
        self.viewport = setup.SCREEN.get_rect()  # 玩家能看到的窗口矩形
        self.caption = tools.get_image(setup.GRAPHICS['title_screen'], 1, 60, 176, 88, (255, 0, 220), C.BG_MULTI)  # 标题

    def setup_player(self):  # 获取人物图像
        self.player_image = tools.get_image(setup.GRAPHICS['mario_bros'], 178, 32, 12, 16, (0, 0, 0), C.PLAYER_MULTI)

    # def setup_cursor(self):  # 设置光标
    #     self.cursor = pygame.sprite.Sprite()
    #     self.cursor.image = tools.get_image(setup.GRAPHICS['item_objects'], 24, 160, 8, 8, (0, 0, 0), C.PLAYER_MULTI)
    #     rect = self.cursor.image.get_rect()
    #     rect.x, rect.y = (220, 360)
    #     self.cursor.rect = rect
    #     self.cursor.state = '1P'  # 状态机

    def update_cursor(self, keys):  # 游戏菜单选项功能 被update调用
        # if keys[pygame.K_UP]:
        # self.cursor.state = '1P'
        # self.cursor.rect.y = 360
        # elif keys[pygame.K_DOWN]:
        #     self.cursor.state = '2P'
        #     self.cursor.rect.y = 405
        if keys[pygame.K_RETURN]:  # 按下回车进入下一个状态
            self.reset_game_info()
            # if self.cursor.state == '1P':
            self.finished = True
            # elif self.cursor.state == '2P':
            #    self.finished = True

    def update(self, surface, keys):  # tools调用的刷新函数

        self.update_cursor(keys)  # 封面栗子头 实际上是光标选择检测

        surface.blit(self.background, self.viewport)  # 画开始菜单的游戏背景
        surface.blit(self.caption, (170, 100))  # 画开始菜单标题
        surface.blit(self.player_image, (110, 490))  # 画开始菜单游戏人物
        # surface.blit(self.cursor.image, self.cursor.rect)  # 画栗子头光标

        # self.info.update()  # 游戏信息更新 调用info文件
        self.info.draw(surface)  # 调用info文件里draw方法 画开始菜单元素

    def reset_game_info(self):  # 被update_cursor调用 重新设置游戏信息
        self.game_info.update({
            'score': 0,  # 游戏分数信息 无需用到
            'coin': 0,  # 游戏金币信息 无需用到
            'lives': 3,
            'player_state': 'small'  # 游戏人物状态 初始为小 无需用到
        })

