import pygame
import Textures
from Structures import ClassicStructure


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, xoy, name_biom, name_structure=None):
        pygame.sprite.Sprite.__init__(self)

        if name_biom in Textures.animation_ground:
            self.animation = Textures.animation_ground[name_biom]
        else:
            self.animation = None

        self.name = name_biom
        self.image = image
        self.select_image = Textures.select
        self.rect = self.image.get_rect(center=xoy)
        self.select = False

        if name_structure:
            self.structure = ClassicStructure(Textures.animations_structures[name_structure][0], (self.rect[0], self.rect[1]), name_structure)
        else:
            self.structure = None

        self.second_animation = 0
        self.speed_animation = 80

    def self_animation(self, stadia):
        self.image = self.animation[stadia - 1]

    def draw(self, screen, there):
        self.select = self.rect.colliderect(there[0], there[1], 1, 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.select:
            screen.blit(self.select_image, (self.rect.x, self.rect.y))

    def update(self, synchronous, move, y_n):  # synchronous - для синхронизации анимации у разных объектов земли
        if self.animation:
            stadia = (synchronous // self.speed_animation + 1) % len(self.animation)
            self.self_animation(stadia)

        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]
