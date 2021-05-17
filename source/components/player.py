import pygame
import tkinter
import json
import os
from .voice import *
from .. import tools, setup
from .. import constants as C
from tkinter import messagebox


class Player(pygame.sprite.Sprite):
    """游戏人物"""
    def __init__(self, name):
        """人物初始化，人物名、人物状态、人物运动、时钟、图像"""
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

    def load_data(self):
        """加载人物数据"""
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    def setup_states(self):
        """加载人物状态"""
        self.state = 'stand'
        self.face_right = True
        self.dead = False
        self.can_jump = True

    def setup_velocities(self):
        """加载人物运动"""
        speed = self.player_data['speed']
        self.x_vel = 0
        self.y_vel = 0

        self.max_walk_vel = speed['max_walk_speed']
        self.max_y_vel = speed['max_y_velocity']
        self.jump_vel = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.gravity = C.GRAVITY
        self.anti_gravity = C.ANTI_GRAVITY
        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel

    def setup_timers(self):
        """设置游戏时钟"""
        self.walking_timer = 0
        self.death_timer = 0

    def load_images(self):
        """加载人物图片"""
        sheet = setup.GRAPHICS['Gagarin']
        frame_rects = self.player_data['image_frames']
        self.right_small_normal_frames = []
        self.small_normal_frames = [self.right_small_normal_frames]
        self.all_frames = [self.right_small_normal_frames]
        self.right_frames = self.right_small_normal_frames

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'], (0, 0, 0), C.PLAYER_MULTI)
                self.right_small_normal_frames.append(right_image)
        self.frame_index = 0
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self, keys):
        """人物刷新函数"""
        self.current_time = pygame.time.get_ticks()
        self.volumn = getVolumn()
        self.handle_states(keys)
        key = sum(keys)
        if ~keys[pygame.K_RETURN] and key >= 1:
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showinfo("提示", "大声喊出来控制角色跳跃!")
            root.destroy()

    def handle_states(self, keys):
        """人物状态处理"""
        self.can_jump_or_not(keys)
        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'die':
            self.die(keys)
        self.image = self.right_frames[self.frame_index]

    def can_jump_or_not(self, keys):
        """判断人物当前是否可以跳跃"""
        if not keys[pygame.K_a] or self.volumn < C.VOLUMN_THRESHOLD:
            self.can_jump = True

    def stand(self, keys):
        """处理人物站立状态"""
        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0
        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_a] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel
        elif self.volumn > C.VOLUMN_THRESHOLD:
            self.state = 'jump'
            self.y_vel = self.jump_vel

    def walk(self, keys):
        """人物行走状态处理"""
        if keys[pygame.K_a] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel
        elif self.volumn > C.VOLUMN_THRESHOLD:
            self.state = 'jump'
            self.y_vel = self.jump_vel

        if self.current_time - self.walking_timer > self.calc_frame_duration():  # 切换帧
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time

        self.face_right = True
        self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)

    def jump(self, keys):
        """人物跳跃状态处理"""
        self.frame_index = 4
        self.y_vel += self.anti_gravity
        self.can_jump = False

        if self.y_vel >= 0:
            self.state = 'fall'

        self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)

        if not keys[pygame.K_a] and self.volumn < C.VOLUMN_THRESHOLD:  # 没按下跳跃键时 转为下落状态
            self.state = 'fall'

    def fall(self, keys):
        """人物下落状态处理"""
        self.y_vel = self.calc_vel(self.y_vel, self.gravity, self.max_y_vel)

        self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)

    def die(self, keys):
        """人物死亡运动处理"""
        self.rect.y += self.y_vel
        self.y_vel += self.anti_gravity

    def go_die(self):
        """人物死亡处理"""
        pygame.mixer.music.load('resources/music/death_BGM.wav')
        pygame.mixer.music.play(start=0.0)
        self.dead = True
        self.y_vel = self.jump_vel
        self.frame_index = 6
        self.state = 'die'
        self.death_timer = self.current_time

    def calc_vel(self, vel, accel, max_vel, is_positive=True):
        """计算人物当前速度"""
        if is_positive:
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)

    def calc_frame_duration(self):
        """计算人物"""
        duration = -60 / 12 * abs(self.x_vel) + 80
        return duration





















