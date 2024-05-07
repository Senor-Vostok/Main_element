import random
from obb.Handler.Handler import EventHandler
from obb.Handler.Handler_show import show_menu
import pygame


if __name__ == '__main__':
    pygame.init()
    with open('data/user/information', mode='rt') as file:
        if file.read() == 'UID':
            uid = random.randint(4, 100000000)
            with open('data/user/information', mode='w') as file:
                file.write('0' * (9 - len(str(uid))) + str(uid))
    handler = EventHandler()
    show_menu(handler, handler.centre)
    while 1:
        handler.update()
