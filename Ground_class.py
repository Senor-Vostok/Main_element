import pygame
from Constants import ANIMATION_SLOWDOWN
from Structures import ClassicStructure


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, xoy, biome, textures):
        pygame.sprite.Sprite.__init__(self)
        self.textures = textures
        if biome[0] in textures.animation_ground:
            self.animation = textures.animation_ground[biome[0]]
        else:
            self.animation = None
        self.biome = biome
        self.name = biome[0]
        self.name_struct = biome[1]
        self.units_count = 0
        self.fraction = None
        self.tile_image = image  # изначальная текстура клетки
        self.image = image  # текущая текстура клетки
        self.select_image = textures.select
        self.rect = self.image.get_rect(center=xoy)
        self.select = False
        # списки размещаемых структур для каждого биома
        self.biome_permissions = {'tower': ['sand', 'flower', 'ground'],
                                  'mill': ['sand', 'flower'],
                                  'mine': ['stone', 'snow']}
        if biome[1] in textures.animations_structures:
            self.structure = ClassicStructure(textures.animations_structures[biome[1]][0], (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2), biome[1], self.textures)
        else:
            self.structure = None
        self.second_animation = 0

    def __self_animation(self, stage):
        self.image = self.animation[stage - 1]

    def draw(self, screen, mouse_click, handler):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and self.name != 'barrier':
            screen.blit(self.select_image, (self.rect.x, self.rect.y))
        if self.structure:
            self.__draw_structure(screen)
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1):
            handler.check_ground_please(self)

    def update(self, synchronous, move, y_n):  # synchronous - для синхронизации анимации у разных объектов земли
        if self.animation:
            stage = (synchronous // ANIMATION_SLOWDOWN + 1) % len(self.animation)
            self.__self_animation(stage)

        if y_n:
            if self.structure: self.structure.update(move, y_n)
            self.rect.y += move[1]
            self.rect.x += move[0]

    def __draw_structure(self, screen):
        if self.biome[1] and self.biome[0] in self.biome_permissions[self.biome[1]]:
            self.image = self.textures.land['barrier'][0]
            self.structure.draw(screen)
