import time
import pygame
from datetime import datetime
from Machine import World
from Generation import Generation
from Cam_class import Cam
import sys
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
centre = (width // 2, height // 2)
pygame.init()

win = pygame.display.set_mode((width, height))
my_font = pygame.font.SysFont('Futura book C', 30)

win.blit(pygame.image.load('data/loading/logo.png').convert_alpha(), (centre[0] - 960, centre[1] - 540))
pygame.display.update()
time.sleep(1)  # Стабилизатор камеры константный(не допускать значения степени 3!!!!)

size_world = 50
gen = Generation(size_world)  # Получаем массив сгенерированной "земли"
world_pos_x = size_world // 2
world_pos_y = size_world // 2
gen.generation()
matr_world = gen.add_barier(20)
world = World(win, centre, [world_pos_x, world_pos_y], matr_world)  # Инициализация мира (его отображение)
world.create()  # заполнение динамической сетки

camera = Cam()  # Создание камеры

open_some = False

while True:
    a = datetime.now().microsecond
    for i in pygame.event.get():
        camera.event(i)
        if i.type == pygame.QUIT:
            sys.exit()
    world.draw(camera.i, camera.move, open_some)  # Вырисовываем картинку
    camera.stabilise_speed(a)  # Стабилизируем камеру
    pygame.draw.circle(win, (255, 255, 0), centre, 5)
    pygame.display.update()
