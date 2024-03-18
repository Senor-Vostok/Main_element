import pygame
from datetime import datetime

import Textures
from Machine import World
from Generation import Generation
from Cam_class import Cam
import sys
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
centre = (width // 2, height // 2)
pygame.init()

win = pygame.display.set_mode((width, height), pygame.FULLSCREEN, vsync=1)
pygame.mouse.set_visible(False)
my_font = pygame.font.SysFont('Futura book C', 30)

win.blit(pygame.image.load('data/loading/logo.png').convert_alpha(), (centre[0] - 960, centre[1] - 540))
pygame.display.update()

size_world = 200
barrier = 20
gen = Generation(size_world)  # Получаем массив сгенерированной "земли"
world_pos_x = (size_world + barrier) // 2
world_pos_y = (size_world + barrier) // 2
gen.generation()
matr_world = gen.add_barier(barrier)
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
    camera.inter()
    world.draw(camera.i, camera.move, open_some)  # Вырисовываем картинку
    win.blit(Textures.point, (camera.i[0] - 10, camera.i[1] - 10))
    pygame.display.update()
