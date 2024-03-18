import pygame
import Player
import Interfaces
from Textures import Textures
from Machine import World
from Generation import Generation
from Cam_class import Cam
import sys
import os
from win32api import GetSystemMetrics

import Widgets


class EventHandler:
    def __init__(self):
        pygame.init()
        self.textures = Textures()
        self.size = GetSystemMetrics(0), GetSystemMetrics(1)
        self.centre = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN, vsync=1)
        pygame.mouse.set_visible(False)

        self.matr = None
        self.world_coord = 0
        self.screen_world = None

        self.camera = Cam()

        self.open_some = True
        self.flag = True

        self.player = None

        self.interfaces = dict()

    def generation(self, size=200, barrier=20):
        gen = Generation(size, self.screen, self.centre)
        self.world_coord = (size + barrier) // 2
        gen.generation()
        self.matr = gen.add_barrier(barrier)

    def player(self, id):
        self.player = Player.Player(id)
        self.player.start_point = (self.screen_world.sq2 // 2, self.screen_world.sq1 // 2)
        self.player.setup(self.screen_world.great_world[self.player.start_point[0]][self.player.start_point[1]])

    def init_world(self):
        self.generation(200)
        self.screen_world = World(self.screen, self.centre, [self.world_coord, self.world_coord], self.matr)
        self.screen_world.create()

    def machine(self):
        self.camera.inter()
        self.camera.speed = self.camera.const_for_speed / (self.clock.get_fps() + 1)
        self.screen_world.draw(self.camera.i, self.camera.move, self.open_some)  # Вырисовываем картинку

    def close(self, data=['menu', False, init_world]):
        self.open_some = data[1]
        self.interfaces.pop(data[0])
        data[2]()

    def show_menu(self):
        menu = Interfaces.Menu(self.centre, self.textures)
        menu.button_start.connect(self.close, 'menu', False, self.init_world)
        self.interfaces['menu'] = menu.create_surface()

    def update(self):
        self.clock.tick()
        c = None
        for i in pygame.event.get():
            self.camera.event(i)
            if i.type == pygame.KEYDOWN:
                c = i
            if i.type == pygame.QUIT:
                sys.exit()
        if self.screen_world:
            self.machine()
        try:
            for i in self.interfaces:
                self.interfaces[i].update(self.camera.i, self.screen, c)
        except Exception:
            pass
        self.screen.blit(self.textures.point, (self.camera.i[0] - 10, self.camera.i[1] - 10))
        self.screen.blit(self.textures.font.render(f'fps: {self.clock.get_fps() // 1}', False, (99, 73, 47)), (30, 30))


if __name__ == '__main__':
    pygame.init()
    handler = EventHandler()
    handler.show_menu()
    while True:
        handler.update()
        pygame.display.flip()
