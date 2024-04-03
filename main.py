from obb.Handler.Handler import EventHandler
from obb.Handler.Handler_show import show_menu
import pygame


if __name__ == '__main__':
    pygame.init()
    handler = EventHandler(0, 1, "water", "fire", (210, 30), (30, 30))
    show_menu(handler, handler.centre)
    while True:
        handler.update()
        pygame.display.flip()
