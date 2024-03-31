import os
import pygame.display
import obb.Objects.Player as Player
from obb.Image_rendering.Textures import Textures
from obb.Image_rendering.Machine import World
from obb.Generation import Generation
from obb.Objects.Cam_class import Cam
from obb.Online import *
from win32api import GetSystemMetrics
from obb.Objects.Structures import *
from pygame.locals import *
from obb.Image_rendering.Efffect import Effect
from obb.Interface.Handler_show import *


class EventHandler:
    def __init__(self, id, fraction, start_point):
        pygame.init()
        self.me = Player.Player(id)
        self.init_player(fraction, start_point)
        self.textures = Textures()
        self.size = GetSystemMetrics(0), GetSystemMetrics(1)
        self.centre = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, flags=FULLSCREEN | DOUBLEBUF, vsync=1)
        self.screen.set_alpha(None)
        pygame.mouse.set_visible(False)
        self.matr, self.screen_world, self.name_save = None, None, None
        self.world_coord = 0
        self.camera = Cam()
        self.open_some, self.flag = True, True
        self.ids = [1, 2, 3, 4]  # id игроков
        self.players = []
        self.fractions = ['fire', 'water', 'air', 'earth']  # TODO: добавить выбор фракций
        self.start_points = [(30, 30), (210, 30), (30, 210), (210, 210)]  # TODO: добавить выбор стартовой позиции
        self.turn = None  # Чей ход
        self.contact = Unknown()
        self.player = None
        self.end = None
        self.interfaces = dict()
        self.effects = list()
        self.pressed = False
        self.structures = [i for i in self.textures.animations_structures]
        self.now_str = 0
        self.rules = dict()
        self.read_rules()

    def read_rules(self):
        with open('game_rules', 'rt') as file:
            for rule in file.read().split('\n'):
                props = rule.split(':')
                self.rules[props[0]] = dict()
                for arg in props[1].split(','):
                    x = arg.split('_')
                    self.rules[props[0]][x[0]] = []
                    for i in x[1:]:
                        self.rules[props[0]][x[0]].append(i)

    def check_ground_please(self, ground):
        if self.camera.i[3] == 3:
            if 'popup_menu' in self.interfaces:
                self.interfaces.pop('popup_menu')
            show_popup_menu(self, (ground.rect[0] + ground.rect[2], ground.rect[1] + ground.rect[3]), ground)

    def generation(self, size=200, barrier=20):
        gen = Generation(size, self.screen, self.centre)
        self.world_coord = (size + barrier * 2) // 2
        gen.generation()
        self.matr = gen.add_barrier(barrier)

    def init_player(self, fraction, start_point):
        self.me.fraction_name = fraction
        self.me.units_count = 100
        self.me.action_pts = 2
        self.me.resources = 15
        self.me.start_point = start_point

    def init_players(self, ids):  # перенести в серверную часть (???)
        for id in ids:
            new_player = Player.Player(id)
            fraction = random.choice(self.fractions)  # назначение фракции игроку
            new_player.fraction_name = fraction
            self.fractions.remove(new_player.fraction_name)
            new_player.units_count = 100  # стартовое кол-во людей в поселении
            new_player.resources = 15  # стартовый капитал
            new_player.action_pts = 2
            new_player.start_point = random.choice(self.start_points)  # спавн в угле мира
            self.start_points.remove(new_player.start_point)
            self.players.append(new_player)
            self.matr[new_player.start_point[0]][new_player.start_point[1]][1] = fraction  # спавн центральной структуры

    def init_world(self, matr=None):
        self.open_some = False
        self.interfaces = dict()
        if not matr:
            self.generation(500)
            matr = self.matr
        if self.name_save:
            with open(f'saves/{self.name_save}.maiso', mode='w') as file:
                file.write('\n'.join('\t'.join('|'.join(j) for j in i) for i in matr))
        self.world_coord = len(matr) // 2
        self.screen_world = World(self.screen, self.centre, [self.world_coord, self.world_coord], matr,
                                  self)  # создание динамической сетки
        self.screen_world.create()
        show_ingame(self, self.centre)
        self.init_players(self.ids)

    def decode_message(self, message):
        message = message.split('-0-')
        if message[0] == 'change':
            i, j = int(message[1].split('|')[2]), int(message[1].split('|')[3])
            self.screen_world.biomes[i][j][1] = message[1].split('|')[1]
            self.place_structure(
                self.screen_world.great_world[i - self.screen_world.world_cord[0]][j - self.screen_world.world_cord[1]],
                message[1].split('|')[1], True)
        if message[0] == 'join':
            self.contact.users += message[1].split('|')

    def machine(self):
        try:
            if self.contact.protocol == 'host': self.decode_message(self.contact.hosting())
            if self.contact.protocol == 'client': self.decode_message(self.contact.check_message())
        except Exception:
            pass
        if len(self.contact.users) == self.contact.maxclient + 1:
            if 'ingame' not in self.interfaces: show_ingame(self, self.centre)
            self.camera.inter()
            self.camera.speed = self.camera.const_for_speed / (self.clock.get_fps() + 1)
            self.screen_world.draw(self.camera.i, self.camera.move, self.open_some)  # Вырисовываем картинку
        else:
            self.screen.blit(self.textures.font.render(f'{len(self.contact.users)}/{self.contact.maxclient + 1}', False,
                                                       (99, 73, 47)), self.centre)
            if 'ingame' in self.interfaces: self.close('ingame', False)

    def close(self, name, open_some, func=None):
        self.open_some = open_some
        self.interfaces.pop(name)
        if func: func()

    def go_back_to_menu(self):
        self.make_save()
        self.open_some = True
        self.interfaces = dict()
        show_menu(self, self.centre)
        self.screen_world = None

    def next_struct(self, ind):
        self.now_str = (self.now_str + ind) % len(self.structures) if self.now_str + ind >= 0 else len(
            self.structures) - 1
        self.interfaces['buildmenu'].structure.image = pygame.transform.scale(
            self.textures.animations_structures[self.structures[self.now_str]][0],
            (360 * self.textures.resizer, 540 * self.textures.resizer))

    def attack(self, ground):
        if self.me.action_pts > 1:
            pass
        else:
            # написать, что мало очков действий
            pass

    def host_game(self, matr):
        if not matr:
            self.generation(200)
            matr = self.matr
        self.contact = Host('0.0.0.0', int(self.interfaces['online'].port.text[:-1]),
                            '\n'.join('\t'.join('|'.join(k) for k in i) for i in matr),
                            int(self.interfaces['online'].count.text[:-1]) - 1)
        self.init_world(matr)

    def connecting(self):
        self.screen.blit(self.textures.connecting,
                         (self.centre[0] - 960 * self.textures.resizer, self.centre[1] - 540 * self.textures.resizer))
        pygame.display.flip()
        host, port = (self.interfaces['online'].interact.text[:-1]).split(':')
        self.contact = Client(host, port)
        self.close('online', False, None)
        if self.contact.connecting():
            users = ''
            while not self.contact.loaded_map:
                users = self.contact.check_message()
            self.contact.users = users.split('|')
            self.world_coord = len(self.contact.gen.split('\n')) // 2
            self.init_world([[k.split('|') for k in i.split('\t')] for i in self.contact.gen.split('\n')])

    def make_save(self):
        with open(f'saves/{self.name_save}.maiso', mode='w') as file:
            file.write('\n'.join('\t'.join('|'.join(j) for j in i) for i in self.screen_world.biomes))

    def open_save(self):
        self.interfaces = dict()
        show_menu(self, self.centre)
        saves = Interfaces.Save_menu(self.centre, self.textures)
        files = [i for i in os.listdir('saves') if len(i.split('.maiso')) > 1]
        saves.handler = self
        saves.add_saves(files, show_choicegame, self)
        self.interfaces['save_menu'] = saves

    def place_structure(self, ground, structure=None, info=True):
        if not structure:
            structure = self.structures[self.now_str]
        if structure != 'null':
            ground.structure = ClassicStructure(self.textures.animations_structures[structure][0], (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2), structure, self.textures)
        else:
            ground.structure = None
        ground.biom[1] = structure
        if 'buildmenu' in self.interfaces:
            self.interfaces.pop('buildmenu')
        if info:
            self.contact.send(f'change-0-' + '|'.join(ground.biom))

    def update_efffects(self):
        if self.camera.i[2] and int(self.camera.i[3]) == 1:
            if not self.pressed:
                self.pressed = True
                self.effects.append(Effect((self.camera.i[0], self.camera.i[1]), self.textures.effects['mouse1']))
        else:
            self.pressed = False
        for i in self.effects:
            i.draw(self.screen)
            if not i.update():
                self.effects.remove(i)

    def click_handler(self):
        c = None
        for i in pygame.event.get():
            self.camera.event(i)
            if i.type == pygame.QUIT:
                sys.exit()
            if i.type == pygame.KEYDOWN and self.decoding()[0] == self.me.id:
                c = i
                if i.key == pygame.K_ESCAPE and len(self.interfaces) >= 2:
                    try:
                        self.interfaces.pop(self.end)
                    except Exception:
                        pass
                elif i.key == pygame.K_ESCAPE and not self.open_some:
                    show_pause(self, self.centre) if 'pause' not in self.interfaces else self.close('pause', False, None)
                if 'popup_menu' in self.interfaces: self.interfaces.pop('popup_menu')
                if 'buildmenu' in self.interfaces: self.interfaces.pop('buildmenu')
                if 'choicegame' in self.interfaces: self.interfaces.pop('choicegame')
            if i.type == pygame.QUIT:
                sys.exit()
        return c

    def update(self):
        self.screen.fill((233, 217, 202))
        self.clock.tick()
        c = self.click_handler()
        if self.screen_world:
            self.machine()
        try:
            for i in self.interfaces:
                self.end = i
                self.interfaces[i].surface.update(self.camera.i, self.screen, c)
        except Exception:
            pass
        self.screen.blit(self.textures.point, (self.camera.i[0] - 10, self.camera.i[1] - 10))
        self.screen.blit(self.textures.font.render(f'fps: {int(self.clock.get_fps())}', False, (99, 73, 47)), (30, 30))
        self.update_efffects()

    def complete(self):
        pass

    def decoding(self):  # возвращает название протокола и массив
        return [1]


if __name__ == '__main__':
    pygame.init()
    handler = EventHandler(1, "fire", (30, 30))
    show_menu(handler, handler.centre)
    while True:
        handler.update()
        pygame.display.flip()
