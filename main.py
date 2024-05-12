import random

import obb.Constants
from obb.Handler.Handler import EventHandler
from obb.Handler.Handler_show import show_menu, show_hello_menu
import pygame


if __name__ == '__main__':
    pygame.init()
    first_play = False
    with open('data/user/information', mode='rt') as file:
        if file.read() == 'UID':
            first_play = True
            uid = random.randint(obb.Constants.MIN_UID, obb.Constants.MAX_UID)
            with open('data/user/information', mode='w') as file:
                file.write('0' * (len(str(obb.Constants.MAX_UID)) - len(str(uid))) + str(uid))
    handler = EventHandler()
    show_menu(handler, handler.centre)
    if first_play:
        show_hello_menu(handler, handler.centre)
    while 1:
        handler.update()
