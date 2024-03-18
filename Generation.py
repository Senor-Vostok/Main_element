import random
from numpy import floor
from perlin_noise import PerlinNoise


class Generation:
    def __init__(self, massive):
        self.translate = {0: 'water', 1: 'sand', 2: 'flower', 3: 'ground', 4: 'stone', 5: 'snow'}
        self.masbiom = [[['\0', '\0'] for _ in range(massive)] for _ in range(massive)]  # Первый биом второй структура
        self.masive = massive
        self.coord_objects = list()
        self.select_cord_objects = list()

    def add_barier(self, size):
        for i in range(self.masive + size * 2):
            if i < size:
                self.masbiom.insert(0, [['barrier', '\0']] * (self.masive + size * 2))
            elif i >= self.masive + size:
                self.masbiom.append([['barrier', '\0']] * (self.masive + size * 2))
            else:
                self.masbiom[i] = [['barrier', '\0']] * size + self.masbiom[i] + [['barrier', '\0']] * size
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

    def generation(self):  # пока отключено
        seed = random.randint(1000, 9000)
        noise = PerlinNoise(octaves=7, seed=seed)
        amp = 14
        period = 100
        landscale = [[0 for _ in range(self.masive)] for _ in range(self.masive)]
        for position in range(self.masive ** 2):
            x = floor(position / self.masive)
            z = floor(position % self.masive)
            y = floor(noise([x / period, z / period]) * amp)
            landscale[int(x)][int(z)] = self.get_key(int(y))
        for i in range(self.masive):
            for j in range(self.masive):
                self.masbiom[i][j][0] = self.translate[landscale[i][j]]
        return self.masbiom
