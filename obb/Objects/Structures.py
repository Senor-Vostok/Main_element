import random

import pygame
from obb.Constants import ANIMATION_SLOWDOWN_STRUCTURES


class ClassicStructure(pygame.sprite.Sprite):
    def __init__(self, image, xoy, name, textures, scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.image = self.__scale(image, scale)
        self.name = name
        try:
            self.animation = [self.__scale(image, scale) for image in random.choice(textures.animations_structures[name])]
        except Exception:
            pass
        self.rect = self.image.get_rect(center=xoy)

        self.second_animation = 0

    def __start_animation(self):
        self.second_animation += 1
        stage = self.second_animation // ANIMATION_SLOWDOWN_STRUCTURES
        if stage >= len(self.animation):
            self.second_animation = 0
            stage = 0
        self.image = self.animation[stage]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def __scale(self, image, scale):
        image = pygame.transform.scale(image, (image.get_rect()[2] * scale, image.get_rect()[3] * scale))
        return image

    def update(self, move, y_n):
        self.__start_animation()
        if y_n:
            self.rect.move_ip(move)


class MainStructure(ClassicStructure):
    def __init__(self, image, xoy, name, textures, scale):
        ClassicStructure.__init__(self, image, xoy, name, textures, scale)
        self.animation = [self.__scale(image, scale) for image in textures.animations_main_structures[name]]

    def __scale(self, image, scale):
        image = pygame.transform.scale(image, (image.get_rect()[2] * scale, image.get_rect()[3] * scale))
        return image
