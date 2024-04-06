from obb.Handler.Handler import EventHandler
from obb.Handler.Handler_show import show_menu
import pygame


if __name__ == '__main__':
    pygame.init()
    with open('data/user/information', mode='rt') as file:
        file = file.read()
        id = int(file)
    handler = EventHandler(0, 1, "water", "fire", (210, 30), (30, 30))
    show_menu(handler, handler.centre)
    while 1:
        handler.update()
