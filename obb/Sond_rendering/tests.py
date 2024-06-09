import random

import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

def generate_perlin_noise_map(N, scale=50, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
    height_map = np.zeros((N, N))
    if seed is not None:
        np.random.seed(seed)
        base = np.random.randint(0, 100)
    else:
        base = 0

    for i in range(N):
        for j in range(N):
            height_map[i][j] = pnoise2(i / scale,
                                       j / scale,
                                       octaves=octaves,
                                       persistence=persistence,
                                       lacunarity=lacunarity,
                                       repeatx=N,
                                       repeaty=N,
                                       base=base)
    return height_map

def normalize_height_map(height_map, min_height=-7, max_height=7):
    # Нормализация в диапазон [0, 1]
    height_map = (height_map - height_map.min()) / (height_map.max() - height_map.min())
    # Масштабирование в диапазон [min_height, max_height]
    height_map = height_map * (max_height - min_height) + min_height
    return height_map

def plot_height_map(height_map):
    plt.imshow(height_map, cmap='terrain', vmin=-7, vmax=7)
    plt.colorbar()
    plt.title("Realistic Terrain Height Map with Perlin Noise")
    plt.show()

# Размер карты
N = 100

# Ключ генерации
seed = random.randint(1, 100000)

# Генерация карты высот с шумом Перлина
height_map = generate_perlin_noise_map(N, seed=seed)

# Нормализация карты высот в диапазон [-7, 7]
height_map = normalize_height_map(height_map)

# Отображение карты высот
plot_height_map(height_map)
