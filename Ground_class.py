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
        self.tile_image = image #изначальная текстура клетки
        self.image = image      #текущая текстура клетки
        self.select_image = textures.select
        self.rect = self.image.get_rect(center=xoy)
        self.select = False

        #списки размещаемых структур для каждого биома
        self.biome_permissions = {'mill': ['sand', 'flower']}

        if biom[1] in textures.animations_structures:
            self.structure = ClassicStructure(textures.animations_structures[biom[1]][0], (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2), biom[1], self.textures)
        else:
            self.structure = None

        self.second_animation = 0
        self.speed_animation = 80

    def self_animation(self, stadia):
        self.image = self.animation[stadia - 1]

    def draw(self, screen, there):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.select = self.rect.colliderect(there[0], there[1], 1, 1)
        if self.select:
            self.check_event(there, 'mill')
        if self.select and self.name != 'barrier':
            screen.blit(self.select_image, (self.rect.x, self.rect.y))
        if self.structure:
            self.draw_structure(screen)

    def update(self, synchronous, move, y_n):  # synchronous - для синхронизации анимации у разных объектов земли
        if self.animation:
            stadia = (synchronous // self.speed_animation + 1) % len(self.animation)
            self.self_animation(stadia)

        if y_n:
            if self.structure: self.structure.update(move, y_n)
            self.rect.y += move[1]
            self.rect.x += move[0]

    def check_event(self, event, struct_name):
        if event[2]: #нажали (ТУДУ: добавить проверку на другие действия)
            if event[3] == 1: #лкм - разместить структуруw
                self.biom[1] = struct_name
                self.structure = ClassicStructure(self.textures.animations_structures[struct_name][0],
                                                 (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2), struct_name, self.textures)
            elif event[3] == 2: #центр
                pass
            elif event[3] == 3: #пкм - убрать структуру
                self.biom[1] = 'null'
                self.structure = None
                self.image = self.tile_image
        if not event[2]: #отпустили
            if event[3] == 1: #лкм
                pass
            elif event[3] == 2: #центр
                pass
            elif event[3] == 3: #пкм
                pass

    def draw_structure(self, screen):
        if self.biom[1] and self.biom[0] in self.biome_permissions[self.biom[1]]:
            self.image = self.textures.land['barrier'][0]
            self.structure.draw(screen)
