import random

from obb.Handler.Handler import EventHandler
from obb.Handler.Handler_show import show_menu
import pygame


if __name__ == '__main__':
    pygame.init()
    file = open('data/user/information', mode='rt')
    if file.read() == 'UID':
        file.close()
        file = open('data/user/information', mode='w')
        id = random.randint(4, 100000000)
        file.write('0' * (9 - len(str(id))) + str(id))
        file.close()
    handler = EventHandler()
    show_menu(handler, handler.centre)
    while 1:
        handler.update()
