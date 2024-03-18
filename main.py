import pygame
from Textures import Textures
from Machine import World
from Generation import Generation
from Cam_class import Cam
import sys
import os
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
centre = (width // 2, height // 2)
pygame.init()
clock = pygame.time.Clock()
textures = Textures()

win = pygame.display.set_mode((width, height), pygame.FULLSCREEN, vsync=1)
pygame.mouse.set_visible(False)
my_font = pygame.font.SysFont('Futura book C', 30)

win.blit(textures.loading, (centre[0] - 960, centre[1] - 540))
pygame.display.update()

size_world = 200
barrier = 20
gen = Generation(size_world, win, centre)  # Получаем массив сгенерированной "земли"
world_pos_x = (size_world + barrier) // 2
world_pos_y = (size_world + barrier) // 2
gen.generation()
matr_world = gen.add_barier(barrier)
world = World(win, centre, [world_pos_x, world_pos_y], matr_world)  # Инициализация мира (его отображение)
world.create()  # заполнение динамической сетки

camera = Cam()  # Создание камеры

open_some = False
flag = True  # потом нормально сделаем

while True:
    normal = clock.tick(60)
    for i in pygame.event.get([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]):
        camera.event(i)
        if i.type == pygame.KEYDOWN:
            #  временно так
            if i.key == pygame.K_1:
                with open('Protocols', mode='w') as file:
                    w = '\n'.join('\t'.join('|'.join(k) for k in i) for i in gen.masbiom)
                    file.write(f'm-0-{w}')
            if i.key == pygame.K_2 and flag:
                flag = False
                os.startfile(rf'{os.getcwd()}\H.py')
            # временно так
        if i.type == pygame.QUIT:
            sys.exit()
    camera.inter()
    camera.speed = camera.const_for_speed / (clock.get_fps() + 1)
    world.draw(camera.i, camera.move, open_some)  # Вырисовываем картинку
    win.blit(textures.point, (camera.i[0] - 10, camera.i[1] - 10))
    win.blit(textures.font.render(f'fps: {clock.get_fps() // 1}', False, (99, 73, 47)), (30, 30))
    pygame.display.update()
