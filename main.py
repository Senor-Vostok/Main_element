import pygame.display
from tkinter.filedialog import askopenfilename
import Player
import Interfaces
from Textures import Textures
from Machine import World
from Generation import Generation
from Cam_class import Cam
import sys
import os
import time
from win32api import GetSystemMetrics
from Structures import *


class EventHandler:
    def __init__(self):
        pygame.init()
        self.textures = Textures()
        self.size = GetSystemMetrics(0), GetSystemMetrics(1)
        self.centre = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        pygame.mouse.set_visible(False)

        self.matr = None
        self.world_coord = 0
        self.screen_world = None

        self.camera = Cam()

        self.open_some = True
        self.flag = True

        self.player = None

        self.interfaces = dict()

        self.structures = [i for i in self.textures.animations_structures]
        self.now_str = 0

    def check_ground_please(self, ground):
        if self.camera.i[3] == 3:
            if 'popup_menu' in self.interfaces:
                self.interfaces.pop('popup_menu')
            self.show_popup_menu((ground.rect[0] + ground.rect[2], ground.rect[1] + ground.rect[3]), ground)

    def generation(self, size=200, barrier=20):
        gen = Generation(size, self.screen, self.centre)
        self.world_coord = (size + barrier * 2) // 2
        gen.generation()
        self.matr = gen.add_barrier(barrier)

    def player(self, id):
        self.player = Player.Player(id)
        self.player.start_point = (self.screen_world.sq2 // 2, self.screen_world.sq1 // 2)
        self.player.setup(self.screen_world.great_world[self.player.start_point[0]][self.player.start_point[1]])

    def init_world(self, matr=None):
        self.open_some = False
        self.interfaces = dict()
        if not matr:
            self.generation(200)
            matr = self.matr
        self.screen_world = World(self.screen, self.centre, [self.world_coord, self.world_coord], matr, self)  # создание динамической сетки
        self.screen_world.create()
        self.show_ingame(self.centre)

    def decode_message(self, message):
        message = message.split('-0-')
        if message[0] == 'change':
            i, j = int(message[1].split('|')[2]), int(message[1].split('|')[3])
            if self.screen_world.biomes[i][j][1] != message[1].split('|')[1]:
                self.place_structure(self.screen_world.great_world[i - self.screen_world.world_cord[0]][j - self.screen_world.world_cord[1]], message[1].split('|')[1], False)
            self.screen_world.biomes[i][j][1] = message[1].split('|')[1]

    def machine(self):
        try:
            with open('online/Cache', mode='rt') as file:
                self.decode_message(file.read())
        except Exception:
            pass
        self.camera.inter()
        self.camera.speed = self.camera.const_for_speed / (self.clock.get_fps() + 1)
        self.screen_world.draw(self.camera.i, self.camera.move, self.open_some)  # Вырисовываем картинку

    def close(self, name, open_some, func=None):
        self.open_some = open_some
        self.interfaces.pop(name)
        if func: func()

    def go_back_to_menu(self):
        self.close('pause', True)
        self.show_menu(self.centre)
        self.screen_world = None

    def next_struct(self, ind):
        self.now_str = (self.now_str + ind) % len(self.structures) if self.now_str + ind >= 0 else len(
            self.structures) - 1
        self.interfaces['buildmenu'].structure.image = pygame.transform.scale(
            self.textures.animations_structures[self.structures[self.now_str]][0],
            (360 * self.textures.resizer, 540 * self.textures.resizer))

    def show_ingame(self, centre):
        game = Interfaces.InGame(centre, self.textures)
        self.interfaces['ingame'] = game

    def show_menu(self, centre):
        menu = Interfaces.Menu(centre, self.textures)
        menu.button_start.connect(self.show_choicegame, self.centre)
        menu.button_load.connect(self.open_save)
        menu.button_online.connect(self.show_online, self.centre)
        menu.button_exit.connect(sys.exit)
        self.interfaces['menu'] = menu

    def show_buildmenu(self, centre, ground=None):
        build = Interfaces.BuildMenu(centre, self.textures)
        build.down.connect(self.next_struct, -1)
        build.up.connect(self.next_struct, 1)
        self.now_str = 0
        build.button_project.connect(self.place_structure, ground)
        if 'popup_menu' in self.interfaces: self.interfaces.pop('popup_menu')
        self.interfaces['buildmenu'] = build

    def show_online(self, centre):
        label = Interfaces.Online(centre, self.textures)
        label.interact.connect(self.connecting)
        self.interfaces['online'] = label

    def show_pause(self, centre):
        pause = Interfaces.Pause(centre, self.textures)
        pause.button_menu.connect(self.go_back_to_menu)
        self.interfaces['pause'] = pause

    def show_popup_menu(self, centre, ground=None):
        popup = Interfaces.PopupMenu(centre, self.textures)
        popup.button_build.connect(self.show_buildmenu, self.centre, ground)
        self.interfaces['popup_menu'] = popup

    def show_choicegame(self, centre, matr=None):
        choice = Interfaces.ChoiceGame(centre, self.textures)
        choice.button_local.connect(self.init_world, matr)
        choice.button_online.connect(self.host_game, matr)
        self.interfaces['choicegame'] = choice

    def host_game(self, matr):
        if not matr:
            self.generation(200)
            matr = self.matr
        with open(rf'{os.getcwd()}\online\Protocols', mode='w') as file:
            w = '\n'.join('\t'.join('|'.join(k) for k in i) for i in matr)
            file.write(f'm-0-{w}')
        os.startfile(rf'{os.getcwd()}\online\H.py')
        self.init_world(matr)

    def connecting(self):
        self.screen.blit(self.textures.connecting, (0, 0))
        pygame.display.flip()
        adress = self.interfaces['online'].interact.text[:-1]
        with open('online/Connect', mode='w') as file:
            file.write(adress)
        os.startfile(rf'{os.getcwd()}\online\C.py')
        time.sleep(5)
        self.close('online', False, None)
        with open('online/Save', mode='rt') as file:
            file = [[k.split('|') for k in i.split('\t')] for i in file.read().split('\n')]
            self.world_coord = len(file) // 2
            if file:
                self.init_world(file)

    def open_save(self):
        filename = askopenfilename()
        with open(filename, mode='rt') as file:
            file = [[k.split('|') for k in i.split('\t')] for i in file.read().split('\n')]
            self.world_coord = (len(file) + 20) // 2
            try:
                if file[0][0][0] == 'barrier':
                    self.show_choicegame(self.centre, file)
            except:
                pass

    def place_structure(self, ground, structure=None, info=True):
        if not structure:
            structure = self.structures[self.now_str]
        ground.structure = ClassicStructure(self.textures.animations_structures[structure][0], (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2), structure, self.textures)
        ground.biom[1] = structure
        if 'buildmenu' in self.interfaces: self.interfaces.pop('buildmenu')
        if info:
            with open('online/Protocols', mode='w') as file:
                file.write(f'change-0-' + '|'.join(ground.biom))
                print(f'change-0-' + '|'.join(ground.biom))

    def update(self):
        self.screen.fill((233, 217, 202))
        self.clock.tick()
        c = None
        for i in pygame.event.get():
            self.camera.event(i)
            if i.type == pygame.KEYDOWN:
                c = i
                if i.key == pygame.K_ESCAPE and not self.open_some:
                    self.show_pause(self.centre) if 'pause' not in self.interfaces else self.close('pause', False, None)
                if 'popup_menu' in self.interfaces: self.interfaces.pop('popup_menu')
                if 'buildmenu' in self.interfaces: self.interfaces.pop('buildmenu')
                if 'choicegame' in self.interfaces: self.interfaces.pop('choicegame')
            if i.type == pygame.QUIT:
                sys.exit()
        if self.screen_world:
            self.machine()
        try:
            for i in self.interfaces:
                self.interfaces[i].create_surface().update(self.camera.i, self.screen, c)
        except Exception:
            pass
        self.screen.blit(self.textures.point, (self.camera.i[0] - 10, self.camera.i[1] - 10))
        self.screen.blit(self.textures.font.render(f'fps: {self.clock.get_fps() // 1}', False, (99, 73, 47)), (30, 30))


if __name__ == '__main__':
    pygame.init()
    handler = EventHandler()
    handler.show_menu(handler.centre)
    while True:
        handler.update()
        pygame.display.flip()
