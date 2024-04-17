import pygame
from obb.Constants import CAMERA_BOOST, MAX_BOOSTED_SPEED


class Cam(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move = [0, 0]
        self.speed = 1
        self.normal_fps = 75
        self.mouse_click = (0, 0, None, None)
        self.smooth_w = False
        self.smooth_s = False
        self.smooth_a = False
        self.smooth_d = False

    def inter(self):
        if self.smooth_a or self.smooth_d:
            self.move[0] = self.move[0] * CAMERA_BOOST if abs(self.move[0] * CAMERA_BOOST) < self.speed * MAX_BOOSTED_SPEED else self.move[0]
        else:
            self.move[0] = self.move[0] / CAMERA_BOOST if abs(self.move[0]) > CAMERA_BOOST else 0
        if self.smooth_w or self.smooth_s:
            self.move[1] = self.move[1] * CAMERA_BOOST if abs(self.move[1] * CAMERA_BOOST) < self.speed * MAX_BOOSTED_SPEED else self.move[1]
        else:
            self.move[1] = self.move[1] / CAMERA_BOOST if abs(self.move[1]) > CAMERA_BOOST else 0

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.move[1] = self.speed
                self.smooth_w = True
            if event.key == pygame.K_s:
                self.move[1] = -self.speed
                self.smooth_s = True
            if event.key == pygame.K_a:
                self.move[0] = self.speed
                self.smooth_a = True
            if event.key == pygame.K_d:
                self.move[0] = -self.speed
                self.smooth_d = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.smooth_w = False
            if event.key == pygame.K_s:
                self.smooth_s = False
            if event.key == pygame.K_a:
                self.smooth_a = False
            if event.key == pygame.K_d:
                self.smooth_d = False
        pressed = True in pygame.mouse.get_pressed()
        number = None
        if pressed:
            number = [_ for _ in pygame.mouse.get_pressed()].index(True) + 1
        self.mouse_click = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], pressed, number]
