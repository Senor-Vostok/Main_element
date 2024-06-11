import random
import pygame
from obb.Objects.Ground_class import Ground
from obb.Constants import TILE_SIZE, OFFSET_X, OFFSET_Y


class World:
    def __init__(self, win, centre, coord, biomes, handler, scale=1):
        self.handler = handler
        self.textures = handler.textures
        self.land = self.textures.land
        self.biomes = biomes  # Получение данных о матрице мира
        self.scale = scale
        self.gr_main = int(TILE_SIZE * self.textures.resizer * self.scale)
        self.sq1 = centre[0] * 2 // self.gr_main + OFFSET_X[0] if centre[0] * 2 // self.gr_main % 2 == 0 else centre[0] * 2 // self.gr_main + OFFSET_X[1]  # Разбиение экрана на секторы, с помощью которых строится динамическая сетка
        self.sq2 = centre[1] * 2 // self.gr_main + OFFSET_Y[0] if centre[1] * 2 // self.gr_main % 2 == 0 else centre[1] * 2 // self.gr_main + OFFSET_Y[1]
        self.win = win
        self.centre = centre
        self.global_centre = [centre[0], centre[1]]
        self.start_dr = [self.centre[0] - self.gr_main // 2 - (self.sq1 // 2) * self.gr_main,
                         self.centre[1] - self.gr_main // 2 - (self.sq2 // 2) * self.gr_main]  # Стартовая установка динамической сетки
        self.now_dr = [self.centre[0] - self.gr_main // 2 - (self.sq1 // 2) * self.gr_main,
                       self.centre[1] - self.gr_main // 2 - (self.sq2 // 2) * self.gr_main]  # Пермещение динамической сетки
        self.great_world = [[None for _ in range(self.sq1)] for _ in range(self.sq2)]  # Создание массива динамической сетки
        self.world_coord = coord  # позиция курсора
        self.synchronous = 0  # Синхронизация анимации связных объектов
        self.rendering = False

    def __destroy(self, sprites):
        for sprite in sprites:
            sprite.kill()

    def create(self, stor='static'):  # Перестройка динамической сетки
        if stor == 'up':  # Удаление нижней части сетки и вставка новой вверх
            self.__destroy(self.great_world.pop(-1))
            self.great_world.insert(0, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                self.add_ground(0, i, self.biomes[self.world_coord[0]][self.world_coord[1] + i])
        elif stor == 'down':  # По принципу Up
            self.__destroy(self.great_world.pop(0))
            self.great_world.insert(self.sq1, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                self.add_ground(self.sq2 - 1, i, self.biomes[self.world_coord[0] + self.sq2 - 1][self.world_coord[1] + i])
        elif stor == 'left':
            for i in range(self.sq2):
                self.__destroy([self.great_world[i].pop(-1)])
                self.great_world[i].insert(0, None)
            for i in range(self.sq2):
                self.add_ground(i, 0, self.biomes[self.world_coord[0] + i][self.world_coord[1]])
        elif stor == 'right':
            for i in range(self.sq2):
                self.__destroy([self.great_world[i].pop(0)])
                self.great_world[i].insert(self.sq1 - 1, None)
            for i in range(self.sq2):
                self.add_ground(i, self.sq1 - 1, self.biomes[self.world_coord[0] + i][self.world_coord[1] + self.sq1 - 1])
        else:  # Заполнение динамической сетки если до этого её не было
            for i in range(self.sq2):
                for j in range(self.sq1):
                    self.add_ground(i, j, self.biomes[self.world_coord[0] + i][self.world_coord[1] + j])

    def move_scene(self):  # Тут происходит проверка, когда нужно обновлять динамическую сетку
        if abs(self.now_dr[0] - self.start_dr[0]) > self.gr_main:
            if self.now_dr[0] >= self.start_dr[0]:
                self.now_dr[0] -= self.gr_main
                self.world_coord[1] = self.world_coord[1] - 1 if self.world_coord[1] >= 1 else None
                self.create('left')
            else:
                self.now_dr[0] += self.gr_main
                self.world_coord[1] += 1
                self.create('right')
        elif abs(self.now_dr[1] - self.start_dr[1]) > self.gr_main:
            if self.now_dr[1] >= self.start_dr[1]:
                self.now_dr[1] -= self.gr_main
                self.world_coord[0] = self.world_coord[0] - 1 if self.world_coord[0] >= 1 else None
                self.create('up')
            else:
                self.now_dr[1] += self.gr_main
                self.world_coord[0] += 1
                self.create('down')

    def check_barrier(self, move, point):  # проверка на препятствия (Работает не только с курсором, но и по координатам)
        for i in range(self.sq2 // 2 - 1, self.sq2 // 2 + 2):
            for j in range(self.sq1 // 2 - 1, self.sq1 // 2 + 2):
                res = self.now_dr[0] + j * self.gr_main <= point[0] - 2 * move[0] <= self.now_dr[0] + j * self.gr_main + self.gr_main and \
                      self.now_dr[1] + i * self.gr_main <= point[1] - 2 * move[1] <= self.now_dr[1] + i * self.gr_main + self.gr_main
                if res and self.biomes[self.world_coord[0] + i][self.world_coord[1] + j][0] == 'barrier':
                    return False
        return True

    def __choice_image(self, biome):
        ind = 0
        for i in range(10):
            if f'{i}' in biome:
                ind = i
        name = biome.split(f'{ind}')[0]
        return self.land[name][ind]

    def add_ground(self, i, j, biome):  # Вспомогательная функция для добавления спрайта земля на сетку
        image = self.__choice_image(biome[0])
        sprite = Ground(image, (self.now_dr[0] + j * self.gr_main + self.gr_main / 2, self.now_dr[1] + i * self.gr_main + self.gr_main / 2), biome, self.textures, self.scale)
        self.great_world[i][j] = sprite
