import pygame
from .. import tools, setup
from .. import constants as C
import json
import os
from .voice import *


class Player(pygame.sprite.Sprite):
    def __init__(self, name):  # 被level文件下的setup_player调用 传入mario
        pygame.sprite.Sprite.__init__(self)
        self.name = name  # mario
        self.load_data()  # 加载游戏人物json数据
        self.setup_states()  # 加载人物状态
        self.setup_velocities()  # 加载人物速度参数
        self.setup_timers()  # 设置计时器
        self.load_images()  # 加载图片

    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)  # 读取人物参数
        with open(file_path) as f:
            self.player_data = json.load(f)  # 将人物数据赋值

    def setup_states(self):
        self.state = 'stand'  # 初始状态站着
        self.face_right = True  # 是否面向右边 不需要
        self.dead = False  # 是否死亡
        self.can_jump = True  # 角色是否能跳跃

    def setup_velocities(self):  # 设置角色速度
        speed = self.player_data['speed']  # 获取角色速度数据
        self.x_vel = 0
        self.y_vel = 0

        self.max_walk_vel = speed['max_walk_speed']  # 走路最大速度
        self.max_run_vel = speed['max_run_speed']  # 跑步最大速度 不需要
        self.max_y_vel = speed['max_y_velocity']  # 最大y轴速度
        self.jump_vel = speed['jump_velocity']  # 最大跳跃速度
        self.walk_accel = speed['walk_accel']  # 走路加速度
        self.run_accel = speed['run_accel']  # 跑步加速度 不需要
        self.turn_accel = speed['turn_accel']  # 转弯时的加速度 不需要
        self.gravity = C.GRAVITY  # 向上跳的重力
        self.anti_gravity = C.ANTI_GRAVITY  # 向下坠落的重力

        self.max_x_vel = self.max_walk_vel  # x方向最大速度即走路最大速度
        self.x_accel = self.walk_accel  # x加速度即走路加速度

    def setup_timers(self):
        self.walking_timer = 0  # 人物行走时间
        self.transition_timer = 0  # 变身时间 不需要
        self.death_timer = 0  # 死亡时间

    def load_images(self):  # 创建人物各个状态下各种帧的图片列表
        sheet = setup.GRAPHICS['mario_bros']  # 获取图片
        frame_rects = self.player_data['image_frames']
        self.right_small_normal_frames = []
        self.left_small_normal_frames = []
        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]

        self.all_frames = [self.right_small_normal_frames,self.left_small_normal_frames,]

        self.right_frames = self.right_small_normal_frames  # 初始状态为小
        self.left_frames = self.left_small_normal_frames  # 初始状态为小

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'], (0, 0, 0), C.PLAYER_MULTI)  # 加载向右图片
                left_image = pygame.transform.flip(right_image, True, False)  # 加载向左图片
                self.right_small_normal_frames.append(right_image)
                self.left_small_normal_frames.append(left_image)
        self.frame_index = 0
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self, keys):  # 在tools文件中被调用
        self.current_time = pygame.time.get_ticks()
        self.volumn = getVolumn()
        self.handle_states(keys)  # 处理各种状态

    def handle_states(self, keys):
        self.can_jump_or_not(keys)  # 检测角色是否可以跳起
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
        if not keys[pygame.K_a] or self.volumn < C.VOLUMN_THRESHOLD:
            self.can_jump = True

    def stand(self, keys):
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
        if keys[pygame.K_a] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_vel
        elif self.volumn > C.VOLUMN_THRESHOLD:
            self.state = 'jump'
            self.y_vel = self.jump_vel

        if self.current_time - self.walking_timer > self.calc_frame_duration():  # 切换帧造型
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time
        self.face_right = True
        if self.x_vel < 0:
            self.frame_index = 5
            self.x_accel = self.turn_accel
        self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)

    def jump(self, keys):
        self.frame_index = 4
        self.y_vel += self.anti_gravity
        self.can_jump = False

        if self.y_vel >= 0:
            self.state = 'fall'

        self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)

        if not keys[pygame.K_a] and self.volumn < C.VOLUMN_THRESHOLD:  # 没按下跳跃键时 转为下落状态
            self.state = 'fall'

    def fall(self, keys):
        self.y_vel = self.calc_vel(self.y_vel, self.gravity, self.max_y_vel)

        self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)

    def die(self, keys):
        self.rect.y += self.y_vel
        self.y_vel += self.anti_gravity

    def go_die(self):
        self.dead = True
        self.y_vel = self.jump_vel
        self.frame_index = 6
        self.state = 'die'
        self.death_timer = self.current_time

    def calc_vel(self, vel, accel, max_vel, is_positive=True):  # 根据速度 加速度 最大速度来计算当前速度
        if is_positive:
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)

    def calc_frame_duration(self):  # 帧的时间间隔 与当前速度有关
        duration = -60 / self.max_run_vel * abs(self.x_vel) + 80
        return duration





















