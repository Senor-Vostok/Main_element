import random
import pygame
from Textures import Textures
from numpy import floor
from perlin_noise import PerlinNoise
from Constants import DEFAULT_COLOR, OCTAVES_G, AMP_G, PERIOD_G, PERCENT_MOVE_Y, BARRIER_SIZE


class Generation:
    def __init__(self, massive, screen, center):
        self.textures = Textures()
        self.translate = {0: 'water', 1: 'sand', 2: 'flower', 3: 'ground', 4: 'stone', 5: 'snow'}
        self.biome_massive = [[['null', 'null', '0', '0'] for _ in range(massive)] for _ in range(massive)]  # Первый биом второй структура
        self.massive = massive
        self.screen = screen
        self.center = center

    def add_barrier(self, size):
        for i in range(self.massive + size * 2):
            if i < size:
                self.biome_massive.insert(0, [['barrier', 'null', '0', '0']] * (self.massive + size * 2))
            elif i >= self.massive + size:
                self.biome_massive.append([['barrier', 'null', '0', '0']] * (self.massive + size * 2))
            else:
                self.biome_massive[i] = [['barrier', 'null', '0', '0']] * size + self.biome_massive[i] + [['barrier', 'null', '0', '0']] * size
        return self.biome_massive

    def __get_key(self, z):
        if z < -6:
            return 0
        elif z in range(-6, -5):
            return 1
        elif z in range(-5, -2):
            return 2
        elif z in range(-2, 5):
            return 3
        elif z in range(5, 7):
            return 4
        return 5

    def generation(self):
        seed = random.randint(1000, 9000)
        noise = PerlinNoise(octaves=OCTAVES_G, seed=seed)
        landscape = [[0 for _ in range(self.massive)] for _ in range(self.massive)]
        for x in range(self.massive):
            for y in range(self.massive):
                z = floor(noise([x / PERIOD_G, y / PERIOD_G]) * AMP_G)
                landscape[int(x)][int(y)] = self.__get_key(int(z))

            percent = int(((x / self.massive) * 100) // 1)
            self.screen.blit(self.textures.loading, (self.center[0] - self.textures.loading.get_rect()[2] // 2, self.center[1] - self.textures.loading.get_rect()[3] // 2))
            self.screen.blit(self.textures.font.render(f'{percent}%', False, DEFAULT_COLOR), (self.center[0], self.center[1] + PERCENT_MOVE_Y))
            pygame.display.update()

        for i in range(self.massive):
            for j in range(self.massive):
                self.biome_massive[i][j][0] = self.translate[landscape[i][j]]
                self.biome_massive[i][j][2] = str(i + BARRIER_SIZE)
                self.biome_massive[i][j][3] = str(j + BARRIER_SIZE)
