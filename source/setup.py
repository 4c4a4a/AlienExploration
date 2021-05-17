import pygame
from . import constants as C
from . import tools
"""游戏开始时的关键设置"""

# pygame模块初始化
pygame.init()

# 窗口大小
SCREEN = pygame.display.set_mode((C.SCREEN_W, C.SCREEN_H))

# 游戏图像资源
GRAPHICS = tools.load_graphics('resources/graphics')
