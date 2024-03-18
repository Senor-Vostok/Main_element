import time

import pygame
from datetime import datetime
from Machine import World
from Generation import Generation
import sys
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
centre = (width // 2, height // 2)
pygame.init()

win = pygame.display.set_mode((width, height))
my_font = pygame.font.SysFont('Futura book C', 30)

win.blit(pygame.image.load('data/loading/logo.png').convert_alpha(), (0, 0))
pygame.display.update()
time.sleep(1)

normal_fps = 60
speed = 12
const_for_speed = normal_fps * speed  # Стабилизатор камеры константный

size_world = 20
gen = Generation(size_world)
world_pos_x = 10
world_pos_y = 10
matr_worls = gen.add_barier(15)
world = World(win, centre, [world_pos_x, world_pos_y], matr_worls)
world.create()

count_x = 0
count_y = 0
flag = False
open_some = False

move = [0, 0]

way = 'stay'


def action():
    if move[1] < 0:
        return 'back'
    elif move[1] > 0:
        return 'forward'
    elif move[0] < 0:
        return 'right'
    elif move[0] > 0:
        return 'left'
    else:
        return 'stay'


def stabilise_speed(speed):  # стабилизация перемещения камеры
    true_fps = 1000000 // (datetime.now().microsecond - a)
    if speed != const_for_speed // true_fps and true_fps > 0:
        speed = speed if 1.48 <= const_for_speed / true_fps <= 1.52 else const_for_speed / true_fps
        if move[0]: move[0] = speed * (abs(move[0]) // move[0])
        if move[1]: move[1] = speed * (abs(move[1]) // move[1])


while True:
    a = datetime.now().microsecond
    world.draw(move, action(), open_some)  # Вырисовываем наш мир
    for i in pygame.event.get():
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_w:
                move[1] = speed
            if i.key == pygame.K_s:
                move[1] = -speed
            if i.key == pygame.K_a:
                move[0] = speed
            if i.key == pygame.K_d:
                move[0] = -speed
        elif i.type == pygame.KEYUP:
            if i.key == pygame.K_w or i.key == pygame.K_s:
                move[1] = 0
            if i.key == pygame.K_a or i.key == pygame.K_d:
                move[0] = 0
        elif i.type == pygame.QUIT:
            sys.exit()
    stabilise_speed(speed)
    pygame.draw.circle(win, (255, 255, 0), centre, 5)
    pygame.display.update()
