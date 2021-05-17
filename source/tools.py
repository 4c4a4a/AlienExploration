import pygame
import os


class Game:
    """游戏主循环控制"""
    def __init__(self, state_dict, start_state):
        """初始化游戏窗口、时钟、状态、行为获取"""
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

    def update(self):
        """游戏刷新函数，控制状态的切换"""
        if self.state.finished:
            game_info = self.state.game_info          # 游戏信息传递
            next_state = self.state.next              # 状态切换
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.start(game_info)               # 新状态开始

        self.state.update(self.screen, self.keys)

    def run(self):
        """游戏主循环，获取游戏操作和控制刷新"""
        while True:
            for event in pygame.event.get():              # 获取游戏操作情况
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()                                 # 调用刷新函数，刷新状态

            pygame.display.update()                       # 显示刷新
            self.clock.tick(60)


def load_graphics(path, accept=('.jpg', '.png', '.bmp', '.gif')):
    """加载游戏图片资源"""
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)                       # 文件名与后缀分开赋值
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics


def get_image(sheet, x, y, width, height, colorkey, scale):
    """画出图像"""
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (x, y, width, height))  # 0,0 代表画到哪个位置, x,y,w,h 代表sheet里哪个区域要取出来
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
    return image





