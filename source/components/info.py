import pygame
from .. import constants as C
from . import coin
from .. import setup, tools
pygame.font.init()


class Info:  # 信息实例 先在main_menu实例中的start中被创建
    def __init__(self, state, game_info):
        self.state = state  # 当前状态
        self.game_info = game_info  # 传入游戏信息
        self.create_state_labels()  # 创建实例时即调用 创建各个信息状态的标签 静态的
        # self.create_info_labels()  # 创建游戏信息的标签 可更新
        # self.flash_coin = coin.FlashingCoin()  # 创建coin文件里金币闪烁的事例 被update调用

    def create_state_labels(self):  # 将调用create_label函数
        self.state_labels = []
        if self.state == 'main_menu':  # 在主菜单时创建的标签数组
            self.state_labels.append((self.create_label('START GAME'), (272, 360)))
            self.state_labels.append((self.create_label('press "enter"'), (272, 420)))
            # self.state_labels.append((self.create_label('TOP - '), (290, 465)))
            # self.state_labels.append((self.create_label('000000'), (400, 465)))
        elif self.state == 'load_screen':
            # self.state_labels.append((self.create_label('WORLD'), (280, 200)))
            # self.state_labels.append((self.create_label('1 - 1'), (430, 200)))
            self.state_labels.append((self.create_label('X    {}'.format(self.game_info['lives'])), (380, 280)))  # 生命
            self.player_image = tools.get_image(setup.GRAPHICS['mario_bros'], 178, 32, 12, 16, (0, 0, 0), C.BG_MULTI)  # 任务图像
        elif self.state == 'game_over':
            self.state_labels.append((self.create_label('GAME OVER'), (280, 250)))

    # def create_info_labels(self):
    #     self.info_labels = []
    #     self.info_labels.append((self.create_label('MARIO'), (75, 30)))
    #     self.info_labels.append((self.create_label('WORLD'), (450, 30)))
    #     self.info_labels.append((self.create_label('TIME'), (625, 30)))
    #     self.info_labels.append((self.create_label('000000'), (75, 55)))
    #     self.info_labels.append((self.create_label('x00'), (300, 55)))
    #     self.info_labels.append((self.create_label('1 - 1'), (480, 55)))

    def create_label(self, label, size=40, width_scale=1.25, height_scale=1):  # 创建标签时调用的函数
        font = pygame.font.SysFont(C.FONT, size)  # 设置字体 作为常量存储在constants文件中
        label_image = font.render(label, True, (255, 255, 255))  # 创建字体的图像
        rect = label_image.get_rect()  # 获取字体图像的矩形
        label_image = pygame.transform.scale(label_image, (int(rect.width * width_scale),  # 放缩字体图像
                                                           int(rect.height * height_scale)))
        return label_image  # 返回字体图像

    # def update(self):  # 被main_menu文件update调用
    #     self.flash_coin.update()  #

    def draw(self, surface):  # main_menu文件update调用
        for label in self.state_labels:  # 画游戏的选项文字 信息文字
            surface.blit(label[0], label[1])
        # for label in self.info_labels:  # 游戏画面顶部信息
        #     surface.blit(label[0], label[1])
        # surface.blit(self.flash_coin.image, self.flash_coin.rect)  # 闪烁金币

        if self.state == 'load_screen':
            surface.blit(self.player_image, (300, 270))
