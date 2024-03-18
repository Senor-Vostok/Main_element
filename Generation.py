import random
import pygame
from Textures import Textures
from numpy import floor
from perlin_noise import PerlinNoise
from functools import cache


class Generation:
    def __init__(self, massive, screen, centre):
        self.textures = Textures()
        self.font = pygame.font.SysFont('Futura book C', 30)
        self.translate = {0: 'water', 1: 'sand', 2: 'flower', 3: 'ground', 4: 'stone', 5: 'snow'}
        self.masbiom = [[['null', 'null', (0, 0)] for _ in range(massive)] for _ in range(massive)]  # Первый биом второй структура
        self.masive = massive
        self.win = screen
        self.centre = centre

    def add_barier(self, size):
        for i in range(self.masive + size * 2):
            if i < size:
                self.masbiom.insert(0, [['barrier', 'null']] * (self.masive + size * 2))
            elif i >= self.masive + size:
                self.masbiom.append([['barrier', 'null']] * (self.masive + size * 2))
            else:
                self.masbiom[i] = [['barrier', 'null']] * size + self.masbiom[i] + [['barrier', 'null']] * size
        return self.masbiom

    def get_key(self, z):
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
        noise = PerlinNoise(octaves=7, seed=seed)
        amp = 14
        period = 100
        landscale = [[0 for _ in range(self.masive)] for _ in range(self.masive)]
        for x in range(self.masive):
            for z in range(self.masive):
                y = floor(noise([x / period, z / period]) * amp)
                landscale[int(x)][int(z)] = self.get_key(int(y))

            procent = int(((x / self.masive) * 100) // 1)
            self.win.blit(self.textures.loading, (self.centre[0] - 960, self.centre[1] - 540))
            self.win.blit(self.font.render(f'{procent}%', False, (99, 73, 47)), (self.centre[0], self.centre[1] + 200))
            pygame.display.update()

        for i in range(self.masive):
            for j in range(self.masive):
                self.masbiom[i][j][0] = self.translate[landscale[i][j]]
                self.masbiom[i][j][2] = (i, j)
        return self.masbiom
