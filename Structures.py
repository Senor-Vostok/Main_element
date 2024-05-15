import pygame
from Constants import ANIMATION_SLOWDOWN_STRUCTURES


class ClassicStructure(pygame.sprite.Sprite):
    def __init__(self, image, xoy, name, textures):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.name = name
        self.animation = textures.animations_structures[name]
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

    def update(self, move, y_n):
        self.__start_animation()
        if y_n:
            self.rect.x += move[0]
            self.rect.y += move[1]
