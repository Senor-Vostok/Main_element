from Handler import EventHandler
import pygame


if __name__ == '__main__':
    pygame.init()
    handler = EventHandler()
    handler.show_menu(handler.centre)
    while True:
        handler.update()
        pygame.display.update()
