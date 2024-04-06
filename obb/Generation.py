import random
import pygame
from obb.Image_rendering.Textures import Textures
from numpy import floor
from perlin_noise import PerlinNoise
from obb.Constants import DEFAULT_COLOR, OCTAVES_G, PERIOD_G, AMP_G, PERCENT_MOVE_Y, BARRIER_SIZE


class Generation:
    def __init__(self, massive, screen, centre):
        self.textures = Textures()
        self.translate = {0: 'water', 1: 'sand', 2: 'flower', 3: 'ground', 4: 'stone', 5: 'snow'}
        self.biome_massive = [[['null', 'null', '0', '0', 'null', '0'] for _ in range(massive)] for _ in range(massive)]  # Первый биом второй структура
        self.massive = massive
        self.win = screen
        self.centre = centre

    def add_barrier(self, size):
        for i in range(self.massive + size * 2):
            if i < size:
                self.biome_massive.insert(0, [['barrier', 'null', '0', '0', 'null', '0']] * (self.massive + size * 2))
            elif i >= self.massive + size:
                self.biome_massive.append([['barrier', 'null', '0', '0', 'null', '0']] * (self.massive + size * 2))
            else:
                self.biome_massive[i] = [['barrier', 'null', '0', '0', 'null', '0']] * size + self.biome_massive[i] + [['barrier', 'null', '0', '0', 'null', '0']] * size
        return self.biome_massive

    def __get_key(self, z):
        if z < -6:
            return 0
        elif z in range(-6, -5):
            return 1
        elif z in range(-5, 0):
            return 2
        elif z in range(0, 5):
            return 3
        elif z in range(5, 7):
            return 4
        return 5

    def generation(self):
        seed = random.randint(1000, 9000)
        noise = PerlinNoise(octaves=OCTAVES_G, seed=seed)
        landscale = [[0 for _ in range(self.massive)] for _ in range(self.massive)]
        for x in range(self.massive):
            for z in range(self.massive):
                y = floor(noise([x / PERIOD_G, z / PERIOD_G]) * AMP_G)
                landscale[int(x)][int(z)] = self.__get_key(int(y))

            procent = int(((x / self.massive) * 100) // 1)
            self.win.blit(self.textures.loading, (self.centre[0] - self.textures.loading.get_rect()[2] // 2, self.centre[1] - self.textures.loading.get_rect()[3] // 2))
            self.win.blit(self.textures.font.render(f'{procent}%', False, DEFAULT_COLOR), (self.centre[0], self.centre[1] + PERCENT_MOVE_Y * self.textures.resizer))
            pygame.display.update()

        for i in range(self.massive):
            for j in range(self.massive):
                self.biome_massive[i][j][0] = self.translate[landscale[i][j]]
                self.biome_massive[i][j][2] = str(i + BARRIER_SIZE)
                self.biome_massive[i][j][3] = str(j + BARRIER_SIZE)
