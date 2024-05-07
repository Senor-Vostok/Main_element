import pygame.sprite
from obb.Objects.Structures import ClassicStructure, MainStructure
from obb.Constants import ANIMATION_SLOWDOWN, TILE_SIZE


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, xoy, biome, textures):
        pygame.sprite.Sprite.__init__(self)
        self.textures = textures
        if biome[0] in textures.animation_ground:
            self.animation = textures.animation_ground[biome[0]]
        else:
            self.animation = None
        self.biome = biome #0-биом 1-структура 2,3-координаты 4-фракция 5-кол-во юнитов
        self.units_count = 0
        self.tile_image = image  # изначальная текстура клетки
        self.image = image  # текущая текстура клетки
        self.select_image = textures.select
        self.rect = self.image.get_rect(center=xoy)
        self.select = False
        if biome[1] in textures.animations_structures:
            self.structure = ClassicStructure(textures.animations_structures[biome[1]][0][0], (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2), biome[1], self.textures)
        elif biome[1] in textures.animations_main_structures:
            self.structure = MainStructure(textures.animations_main_structures[biome[1]][0], (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2), biome[1], self.textures)
        else:
            self.structure = None
        self.second_animation = 0

    def __self_animation(self, stadia):
        self.image = self.animation[stadia - 1]

    def connect_border(self, all_screen):
        border = 0
        i, j = int(self.biome[2]), int(self.biome[3])
        around = [all_screen[i - 1][j], all_screen[i][j - 1], all_screen[i + 1][j], all_screen[i][j + 1]]
        indexes = [5, 2, 3, 4]
        flag = False
        for board in around + around:
            if self.biome[4] != board[4]:
                if flag and border != 0:
                    break
                flag = True
            elif self.biome[4] == board[4] and flag:
                border = border + indexes[around.index(board)] if border == 0 else border + 4
        if border == 0 and flag:
            border = 1
        elif not flag:
            border = 0
        if border in range(2, 6) and self.biome[4] == around[0][4] and self.biome[4] == around[2][4]:
            border = 14
        elif border in range(2, 6) and self.biome[4] == around[1][4] and self.biome[4] == around[3][4]:
            border = 15
        return border

    def draw(self, screen, mouse_click, handler):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.biome[4] != 'null':
            screen.blit(self.textures.border_fractions[self.biome[4]][self.connect_border(handler.screen_world.biomes)], (self.rect.x, self.rect.y))
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and self.biome[0] != 'barrier':
            screen.blit(self.select_image, (self.rect.x, self.rect.y))
        if self.structure:
            self.__draw_structure(screen)
        elif self.biome[5] != '0':
            category = 'small' if int(self.biome[5]) < 30 else 'middle' if int(self.biome[5]) < 80 else 'large'
            screen.blit(self.textures.army[category][0], (self.rect.x, self.rect.y))
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1):
            handler.check_ground_please(self)

    def update(self, synchronous, move, y_n):  # synchronous - для синхронизации анимации у разных объектов земли
        if self.animation:
            stage = (synchronous // ANIMATION_SLOWDOWN + 1) % len(self.animation)
            self.__self_animation(stage)
        if y_n:
            if self.structure: self.structure.update(move, y_n)
            self.rect.move_ip(move)
        #обновить текстуру если разрушена фракция
        # if self.biome[4] == 'null':
        #     self.structure.image = self.textures.destroyed_structures[self.structure][0] или [0][0]

    def __draw_structure(self, screen):
        self.structure.draw(screen)
