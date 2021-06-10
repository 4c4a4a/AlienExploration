import pygame
from ..states.level import Level
from .. import constants as C
from .. import setup, tools
pygame.font.init()


class Info:
    """游戏文字信息绘制"""
    def __init__(self, state, game_info):
        """初始化设置，状态、当前信息、信息标签"""
        self.state = state
        self.game_info = game_info
        self.create_state_labels()

    def create_state_labels(self):
        """创建游戏信息标签列表"""
        self.state_labels = []
        if self.state == 'main_menu':
            self.state_labels.append((self.create_label('START GAME'), (272, 360)))
            self.state_labels.append((self.create_label('press "ENTER"', width_scale=0.8, height_scale=0.64), (305, 390)))
        elif self.state == 'load_screen':
            self.state_labels.append((self.create_label('X    {}'.format(self.game_info['lives'])), (380, 280)))
            self.player_image = tools.get_image(setup.GRAPHICS['Gagarin'], 178, 32, 12, 16, (0, 0, 0), C.BG_MULTI)
            self.state_labels.append((self.create_label("____Shout out to control the character's jump!____"), (-30, 530)))
        elif self.state == 'game_over':
            self.state_labels.append((self.create_label('GAME OVER'), (290, 280)))
        elif self.state == 'win':
            self.state_labels.append((self.create_label('YOU WIN!'), (300, 260)))

    def create_label(self, label, size=40, width_scale=1.25, height_scale=1.0):
        """创建文字图像"""
        font = pygame.font.SysFont('arial.ttf', size)
        label_image = font.render(label, True, (255, 255, 255))
        rect = label_image.get_rect()
        label_image = pygame.transform.scale(label_image, (int(rect.width * width_scale),
                                                           int(rect.height * height_scale)))
        return label_image

    def draw(self, surface):
        """画出有关信息文字图像"""
        for label in self.state_labels:
            surface.blit(label[0], label[1])

        if self.state == 'load_screen':
            surface.blit(self.player_image, (300, 270))
