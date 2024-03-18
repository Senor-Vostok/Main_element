import pygame
from datetime import datetime


class Cam(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move = [0, 0]
        self.normal_fps = 60
        self.speed = 18  # не ставить связанные со степенью 3 и нечетные числа
        self.const_for_speed = self.normal_fps * self.speed
        self.i = (0, 0)

    def stabilise_speed(self, a):  # стабилизация перемещения камеры
        true_fps = 1000000 // (datetime.now().microsecond - a)
        if self.speed != self.const_for_speed // true_fps and true_fps > 0:
            self.speed = self.speed if 1.48 <= self.const_for_speed / true_fps <= 1.52 else self.const_for_speed / true_fps
            if self.move[0]: self.move[0] = self.speed * (abs(self.move[0]) // self.move[0])
            if self.move[1]: self.move[1] = self.speed * (abs(self.move[1]) // self.move[1])

    def event(self, i):
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_w:
                self.move[1] = self.speed
            if i.key == pygame.K_s:
                self.move[1] = -self.speed
            if i.key == pygame.K_a:
                self.move[0] = self.speed
            if i.key == pygame.K_d:
                self.move[0] = -self.speed
        elif i.type == pygame.KEYUP:
            if i.key == pygame.K_w or i.key == pygame.K_s:
                self.move[1] = 0
            if i.key == pygame.K_a or i.key == pygame.K_d:
                self.move[0] = 0
        elif i.type == pygame.MOUSEMOTION:
            self.i = (i.pos[0], i.pos[1])

    def update(self):
        pass
