import pygame
from .. import constants as C
from .. import setup, tools
pygame.font.init()


class Info:  # 信息实例 先在main_menu实例中的start中被创建
    def __init__(self, state, game_info):
        self.state = state  # 当前状态
        self.game_info = game_info  # 传入游戏信息
        self.create_state_labels()  # 创建实例时即调用 创建各个信息状态的标签 静态的

    def create_state_labels(self):  # 将调用create_label函数
        self.state_labels = []
        if self.state == 'main_menu':  # 在主菜单时创建的标签数组
            self.state_labels.append((self.create_label('START GAME'), (272, 360)))
            self.state_labels.append((self.create_label('press "ENTER"', width_scale=0.8, height_scale=0.64), (305, 390)))
        elif self.state == 'load_screen':
            self.state_labels.append((self.create_label('X    {}'.format(self.game_info['lives'])), (380, 280)))  # 生命
            self.player_image = tools.get_image(setup.GRAPHICS['mario_bros'], 178, 32, 12, 16, (0, 0, 0), C.BG_MULTI)  # 任务图像
        elif self.state == 'game_over':
            self.state_labels.append((self.create_label('GAME OVER'), (280, 250)))

    def create_label(self, label, size=40, width_scale=1.25, height_scale=1.0):  # 创建标签时调用的函数
        font = pygame.font.SysFont(C.FONT, size)  # 设置字体 作为常量存储在constants文件中
        label_image = font.render(label, True, (255, 255, 255))  # 创建字体的图像
        rect = label_image.get_rect()  # 获取字体图像的矩形
        label_image = pygame.transform.scale(label_image, (int(rect.width * width_scale),  # 放缩字体图像
                                                           int(rect.height * height_scale)))
        return label_image  # 返回字体图像

    def draw(self, surface):  # main_menu文件update调用
        for label in self.state_labels:  # 画游戏的选项文字 信息文字
            surface.blit(label[0], label[1])

        if self.state == 'load_screen':
            surface.blit(self.player_image, (300, 270))
