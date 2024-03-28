import pygame
from datetime import datetime


class Cam(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move = [0, 0]
        self.normal_fps = 60
        self.speed = 1
        self.const_for_speed = self.normal_fps * self.speed
        self.i = (0, 0, None, None)
        self.smooth_x = False
        self.smooth_y = False

        self.smooth_w = False
        self.smooth_s = False
        self.smooth_a = False
        self.smooth_d = False

        self.smoothes = [self.smooth_w, self.smooth_a, self.smooth_s, self.smooth_d]

    def stabilise_speed(self, a):  # стабилизация перемещения камеры
        try:
            true_fps = 1000000 // (datetime.now().microsecond - a)
        except Exception:
            true_fps = self.normal_fps
        if self.speed != self.const_for_speed // true_fps and true_fps > 0:
            self.speed = self.speed if 1.48 <= self.const_for_speed / true_fps <= 1.52 else self.const_for_speed / true_fps
            if self.move[0]:
                self.move[0] = self.speed * (abs(self.move[0]) // self.move[0])
            if self.move[1]:
                self.move[1] = self.speed * (abs(self.move[1]) // self.move[1])

    def inter(self):
        if self.smooth_a or self.smooth_d:
            self.move[0] = self.move[0] * 1.1 if abs(self.move[0] * 1.1) < self.speed * 20 else self.move[0]
        else:
            self.move[0] = self.move[0] / 1.1 if abs(self.move[0]) / 1.1 > 1 else 0
        if self.smooth_w or self.smooth_s:
            self.move[1] = self.move[1] * 1.1 if abs(self.move[1] * 1.1) < self.speed * 20 else self.move[1]
        else:
            self.move[1] = self.move[1] / 1.1 if abs(self.move[1]) / 1.1 > 1 else 0

    def event(self, i):
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_w:
                self.move[1] = self.speed
                self.smooth_w = True
            if i.key == pygame.K_s:
                self.move[1] = -self.speed
                self.smooth_s = True
            if i.key == pygame.K_a:
                self.move[0] = self.speed
                self.smooth_a = True
            if i.key == pygame.K_d:
                self.move[0] = -self.speed
                self.smooth_d = True
        elif i.type == pygame.KEYUP:
            if i.key == pygame.K_w:
                self.smooth_w = False
            if i.key == pygame.K_s:
                self.smooth_s = False
            if i.key == pygame.K_a:
                self.smooth_a = False
            if i.key == pygame.K_d:
                self.smooth_d = False

            # if i.key == pygame.K_w or i.key == pygame.K_s:
            #     self.smooth_y = False
            # if i.key == pygame.K_a or i.key == pygame.K_d:
            #     self.smooth_x = False
        elif i.type == pygame.MOUSEMOTION:
            self.i = (i.pos[0], i.pos[1], None, None)
        elif i.type == pygame.MOUSEBUTTONDOWN:
            self.i = (i.pos[0], i.pos[1], True, i.button)
        elif i.type == pygame.MOUSEBUTTONUP:
            self.i = (i.pos[0], i.pos[1], False, i.button)
