# 工具和游戏主控
import pygame
import os


class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()  # 创建图层
        self.clock = pygame.time.Clock()  # 游戏计时器
        self.keys = pygame.key.get_pressed()  # 获取按键
        self.state_dict = state_dict  # 状态字典
        self.state = self.state_dict[start_state]  # 初始化主菜单状态 在main_menu文件里 是一个值为类的字典

    def update(self):
        if self.state.finished:  # 检查当前阶段是否完成
            game_info = self.state.game_info  # 幅值当前阶段结束后游戏信息
            next_state = self.state.next  # 幅值下一个状态
            self.state.finished = False  # 将当前阶段状态结束标志改为假
            self.state = self.state_dict[next_state]  # 更改状态为下一个状态
            self.state.start(game_info)  # 调用当前状态函数 传入游戏信息

        self.state.update(self.screen, self.keys)  # 传入图层和按键

    def run(self):
        while True:
            for event in pygame.event.get():  # 获取游戏操作情况
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:  # 按下键盘
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:  # 松开键盘
                    self.keys = pygame.key.get_pressed()

            self.update()  # 循环调用update 刷新当前阶段

            pygame.display.update()  # 屏幕刷新
            self.clock.tick(60)


def load_graphics(path, accept=('.jpg', '.png', '.bmp', '.gif')):  # 获取图像 被setup文件里调用 赋值为GRAPHICS
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)  # 文件名和后缀
        if ext.lower() in accept:  # 防止获取错误文件
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics


def get_image(sheet, x, y, width, height, colorkey, scale):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (x, y, width, height))  # 0,0 代表画到哪个位置, x,y,w,h 代表sheet里哪个区域要取出来
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
    return image





