import random
import pygame

import obb.Constants


class Resource(pygame.sprite.Sprite):
    def __init__(self, xoy, image, flag=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.start = xoy
        self.rect = self.image.get_rect(center=xoy)
        self.drop_second = 0
        self.drop_speed = random.randint(1, obb.Constants.RESOURCE_SPEED_ANIMATION_MAX)
        self.drop_move = obb.Constants.RESOURCE_DROP_MOVE
        self.drop_delta = obb.Constants.RESOURCE_DROP_DELTA
        self.animation = flag
        self.take_cake = obb.Constants.RESOURCE_CUT_TO
        self.deviation = random.randint(-obb.Constants.RESOURCE_DEVIATION, obb.Constants.RESOURCE_DEVIATION + 1)

    def take(self, move):
        if not self.animation and self.take_cake != 0:
            vector = ((move[0] - self.rect.x) / self.take_cake, (move[1] - self.rect.y) / self.take_cake)
            self.rect.x += vector[0]
            self.rect.y += vector[1]
            self.take_cake -= 1
            return False
        if self.take_cake == 0:
            return True
        return False

    def drop_animation(self):
        if self.animation:
            self.drop_second += 1
            if self.drop_speed == self.drop_second:
                self.rect.y -= self.drop_move
                self.rect.x -= self.deviation
                self.drop_move -= self.drop_delta
                self.drop_delta += 1
                self.drop_second = 0
            if self.rect.y > self.start[1]:
                self.rect.y += self.drop_move
                self.animation = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move, move_there=None):
        res = False
        self.drop_animation()
        if move_there:
            res = self.take(move_there)
        return res