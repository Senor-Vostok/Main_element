import pygame
from Structures import ClassicStructure


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, xoy, biom, textures):
        pygame.sprite.Sprite.__init__(self)
        self.textures = textures
        if biom[0] in textures.animation_ground:
            self.animation = textures.animation_ground[biom[0]]
        else:
            self.animation = None

        self.biom = biom
        self.name = biom[0]
        self.name_struct = biom[1]

        self.units_count = 0
        self.fraction = None

        self.border_fraction = None

        self.tile_image = image  # изначальная текстура клетки
        self.image = image  # текущая текстура клетки

        self.select_image = textures.select
        self.rect = self.image.get_rect(center=xoy)
        self.select = False

        # списки размещаемых структур для каждого биома
        self.biome_permissions = {'tower': ['sand', 'flower'],
                                  'mill': ['sand', 'flower'],
                                  'mine': ['stone', 'snow']}

        if biom[1] in textures.animations_structures:
            self.structure = ClassicStructure(textures.animations_structures[biom[1]][0], (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2), biom[1], self.textures)
        else:
            self.structure = None

        self.second_animation = 0
        self.speed_animation = 80

    def self_animation(self, stadia):
        self.image = self.animation[stadia - 1]

    def draw(self, screen, there, handler):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.colliderect(there[0], there[1], 1, 1) and self.name != 'barrier':
            screen.blit(self.select_image, (self.rect.x, self.rect.y))
        if self.structure:
            self.draw_structure(screen)
        if self.rect.colliderect(there[0], there[1], 1, 1):
            handler.check_ground_please(self)

    def update(self, synchronous, move, y_n):  # synchronous - для синхронизации анимации у разных объектов земли
        if self.animation:
            stadia = (synchronous // self.speed_animation + 1) % len(self.animation)
            self.self_animation(stadia)

        if y_n:
            if self.structure: self.structure.update(move, y_n)
            self.rect.y += move[1]
            self.rect.x += move[0]

    def draw_structure(self, screen):
        if self.biom[1] and self.biom[0] in self.biome_permissions[self.biom[1]]:
            self.image = self.textures.land['barrier'][0]
            self.structure.draw(screen)
