import pygame
from . import constants as C
from . import tools

pygame.init()

SCREEN = pygame.display.set_mode((C.SCREEN_W, C.SCREEN_H))  # 游戏窗口

GRAPHICS = tools.load_graphics('resources/graphics')
