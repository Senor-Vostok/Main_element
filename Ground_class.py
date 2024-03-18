import pygame
import Textures
from Structures import ClassicStructure


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, xoy, biom):
        pygame.sprite.Sprite.__init__(self)

        if biom[0] in Textures.animation_ground:
            self.animation = Textures.animation_ground[biom[0]]
        else:
            self.animation = None

        self.biom = biom
        self.name = biom[0]
        self.name_struct = biom[1]
        self.image = image
        self.select_image = Textures.select
        self.rect = self.image.get_rect(center=xoy)
        self.select = False

        if biom[1] in Textures.animations_structures:
            self.structure = ClassicStructure(Textures.animations_structures[biom[1]][0], (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2), biom[1])
        else:
            self.structure = None

        self.second_animation = 0
        self.speed_animation = 80

    def self_animation(self, stadia):
        self.image = self.animation[stadia - 1]

    def draw(self, screen, there):
        self.select = self.rect.colliderect(there[0], there[1], 1, 1)
        if self.select:
            pass  # Обработчик событий можно передавать - there, self.biom, self.rect крч всё что есть в классе
        # P.s. в there храниться x, y и flag(None - просто навелись на клетку, True - нажали, False - отпустили)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.select and self.name != 'barrier':
            screen.blit(self.select_image, (self.rect.x, self.rect.y))
        if self.structure:
            self.structure.draw(screen)

    def update(self, synchronous, move, y_n):  # synchronous - для синхронизации анимации у разных объектов земли
        if self.animation:
            stadia = (synchronous // self.speed_animation + 1) % len(self.animation)
            self.self_animation(stadia)

        if y_n:
            if self.structure: self.structure.update(move, y_n)
            self.rect.y += move[1]
            self.rect.x += move[0]
