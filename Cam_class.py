import pygame
from Constants import *


class Cam(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move = [0, 0]
        self.speed = 1
        self.mouse_click = (0, 0, None, None)
        self.smooth_x = False
        self.smooth_y = False

    def inter(self):
        if self.smooth_x:
            self.move[0] = self.move[0] * CAMERA_BOOST if abs(self.move[0] * CAMERA_BOOST) < self.speed * MAX_BOOSTED_SPEED else self.move[0]
        else:
            self.move[0] = self.move[0] / CAMERA_BOOST if abs(self.move[0]) > CAMERA_BOOST else 0
        if self.smooth_y:
            self.move[1] = self.move[1] * CAMERA_BOOST if abs(self.move[1] * CAMERA_BOOST) < self.speed * MAX_BOOSTED_SPEED else self.move[1]
        else:
            self.move[1] = self.move[1] / CAMERA_BOOST if abs(self.move[1]) > CAMERA_BOOST else 0

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.smooth_y = True
                self.move[1] = self.speed
            if event.key == pygame.K_s:
                self.move[1] = -self.speed
                self.smooth_y = True
            if event.key == pygame.K_a:
                self.move[0] = self.speed
                self.smooth_x = True
            if event.key == pygame.K_d:
                self.move[0] = -self.speed
                self.smooth_x = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                self.smooth_y = False
            if event.key == pygame.K_a or event.key == pygame.K_d:
                self.smooth_x = False
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_click = (event.pos[0], event.pos[1], None, None)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_click = (event.pos[0], event.pos[1], True, event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_click = (event.pos[0], event.pos[1], False, event.button)
