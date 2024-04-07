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
from obb.Handler.Handler_show import *
from obb.Constants import DEFAULT_COLOR, BACKGROUND_COLOR, BARRIER_SIZE
from obb.Handler.Handler_render import rendering


class EventHandler:
    def __init__(self):  # TODO: исправить присваивание bot_id и id
        pygame.init()
        with open('data/user/information', mode='rt') as file:
            self.me = Player.Player(int(file.read()))
        self.textures = Textures()
        self.size = GetSystemMetrics(0), GetSystemMetrics(1)
        self.centre = (self.size[0] // 2, self.size[1] // 2)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        pygame.mouse.set_visible(False)
        self.matr, self.screen_world, self.name_save = None, None, None
        self.loaded_save, self.pressed = False, False
        self.world_coord = 0
        self.camera = Cam()
        self.open_some, self.flag = True, True
        self.fractions = ['water', 'fire', 'air', 'earth']
        self.start_points = list()
        self.info_players = list()
        self.turn = None  # Чей ход
        self.contact = Unknown()
        self.interfaces = dict()
        self.effects = list()
        self.structures = [i for i in self.textures.animations_structures]
        self.now_structure = 0
        self.rules = dict()
        self.read_rules()
        self.uid = self.textures.font.render(f'UID: {"0" * (9 - len(str(self.me.id))) + str(self.me.id)}', False, DEFAULT_COLOR)

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
        if self.camera.mouse_click[3] == 3:
            if 'popup_menu' in self.interfaces:
                self.interfaces.pop('popup_menu')
            if ground.biome[0] != 'barrier':
                show_popup_menu(self, (ground.rect[0] + ground.rect[2], ground.rect[1] + ground.rect[3]), ground, self.me.fraction_name)

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

    # def init_bot(self, fraction, start_point):
    #     self.bot.fraction_name = fraction
    #     self.bot.units_count = 100
    #     self.bot.action_pts = 2e10
    #     self.bot.resources = 15e10
    #     self.bot.start_point = start_point
    #     self.run_bot()
    #
    # def run_bot(self):
    #     self.bot.buy_smth(self)
    #     # self.bot.build_smth(self, 0)

    def init_players(self):
        if len(self.info_players[0]) > 1:
            print(self.info_players)
            for c in range(1, len(self.info_players)):
                i = self.contact.users.index(self.info_players[c][0])
                self.contact.send(f"uid-0-{self.info_players[c][1]}|{'_'.join(map(str, self.info_players[c][2]))}-end-", self.contact.array_clients[i - 1])
            self.init_player(self.info_players[0][1], self.info_players[0][2])
            return
        whitelist = list()
        for c in range(len(self.info_players)):
            fraction = random.choice(self.fractions)  # создание фракции
            while fraction in whitelist:
                fraction = random.choice(self.fractions)
            whitelist.append(fraction)
            self.info_players[c].append(fraction)
            start_point = [random.randint(BARRIER_SIZE, len(self.screen_world.biomes) - BARRIER_SIZE),
                           random.randint(BARRIER_SIZE, len(self.screen_world.biomes) - BARRIER_SIZE)]
            while start_point in self.start_points:
                start_point = [random.randint(BARRIER_SIZE, len(self.screen_world.biomes) - BARRIER_SIZE),
                               random.randint(BARRIER_SIZE, len(self.screen_world.biomes) - BARRIER_SIZE)]
            self.start_points.append(start_point)
            self.info_players[c].append([start_point[0], start_point[1]])
            self.screen_world.biomes[start_point[0]][start_point[1]][1] = fraction
            for i in range(-2, 3):
                for j in range(-2, 3):
                    self.screen_world.biomes[start_point[0] + i][start_point[1] + j][4] = fraction
                    if self.contact.protocol == 'host':
                        self.contact.send(f'change-0-{"|".join(self.screen_world.biomes[start_point[0] + i][start_point[1] + j])}-end-')
            if c > 0 and self.contact.protocol == 'host':
                self.contact.send(f"uid-0-{fraction}|{'_'.join(map(str, start_point))}-end-", self.contact.array_clients[c - 1])
        self.init_player(self.info_players[0][1], self.info_players[0][2])

    def init_world(self, matr=None):
        self.open_some = False
        self.interfaces = dict()
        if not matr:
            self.generation(200)
            matr = self.matr
        self.world_coord = 0
        self.screen_world = World(self.screen, self.centre, [self.world_coord, self.world_coord], matr, self)  # создание динамической сетки
        self.screen_world.create()
        if not self.loaded_save:
            self.info_players.append([self.me.uid])

    def decode_message(self, message):
        for message in message.split('-end-'):
            mess = message.split('-0-')
            if mess[0] == 'change':
                i, j = int(mess[1].split('|')[2]), int(mess[1].split('|')[3])
                self.screen_world.biomes[i][j] = mess[1].split('|')
                i, j = i - self.screen_world.world_coord[0], j - self.screen_world.world_coord[1]
                if self.screen_world.sq1 > i >= 0 and self.screen_world.sq2 > j >= 0:
                    self.screen_world.great_world[i][j].fraction = mess[1].split('|')[4]
                    self.place_structure(self.screen_world.great_world[i][j], mess[1].split('|')[1], False)
            if mess[0] == 'join':
                if self.contact.private and mess[1].split('|')[1] not in self.contact.whitelist:
                    if self.contact.protocol == 'host':
                        self.contact.array_clients.pop(-1).close()
                else:
                    self.contact.users.append(mess[1].split('|')[1])
                    if not self.loaded_save:
                        self.info_players.append([mess[1].split('|')[1]])
            if mess[0] == 'uid':
                fraction = mess[1].split('|')[0]
                coord = [int(i) for i in (mess[1].split('|')[1]).split('_')]
                self.init_player(fraction, coord)

    def machine(self):
        try:
            if self.contact.protocol == 'host': self.decode_message(self.contact.hosting())
            if self.contact.protocol == 'client': self.decode_message(self.contact.check_message())
        except Exception:
            pass
        if len(self.contact.users) == self.contact.maxclient + 1:
            if not self.screen_world.rendering:
                if self.contact.protocol == 'unknown' or self.contact.protocol == 'host':
                    self.init_players()
                show_ingame(self, self.centre)
                self.move_to_coord(self.me.start_point)
                if self.name_save:
                    self.make_save()
            self.screen_world.rendering = True
            self.camera.speed = (self.camera.normal_fps + 1) / (self.clock.get_fps() + 1)
            self.camera.inter()
        else:
            self.screen_world.rendering = False
            self.screen.blit(self.textures.font.render(f'{len(self.contact.users)}/{self.contact.maxclient + 1}', False, DEFAULT_COLOR), self.centre)
            if 'ingame' in self.interfaces: close(self, 'ingame', False)

    def go_back_to_menu(self, save=True):
        if save:
            self.make_save()
        self.matr, self.screen_world, self.name_save = None, None, None
        self.world_coord = 0
        self.open_some, self.flag = True, True
        self.turn = None
        self.contact = Unknown()
        self.info_players = list()
        self.loaded_save = False
        self.start_points = list()
        self.interfaces = dict()
        show_menu(self, self.centre)

    def move_to_coord(self, coord):
        self.screen_world.world_coord = [coord[0] - self.screen_world.sq2 // 2,
                                         coord[1] - self.screen_world.sq1 // 2]
        self.screen_world.create('static')

    def next_struct(self, ind):
        self.now_structure = (self.now_structure + ind) % len(self.structures) if self.now_structure + ind >= 0 else len(
            self.structures) - 1
        self.interfaces['buildmenu'].structure.image = pygame.transform.scale(self.textures.animations_structures[self.structures[self.now_structure]][0][0], (360 * self.textures.resizer, 540 * self.textures.resizer))

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
        count = int(self.interfaces['online'].count.text[:-1])
        if count < 2:
            count = 2
        if count > 4:
            count = 4
        self.contact = Host('0.0.0.0', int(self.interfaces['online'].port.text[:-1]),
                            '\n'.join('\t'.join('|'.join(k) for k in i) for i in matr),
                            count - 1, self.loaded_save)
        self.contact.users.append(self.me.uid)
        self.contact.whitelist = [user[0] for user in self.info_players]
        self.init_world(matr)

    def connecting(self):
        self.screen.blit(self.textures.connecting, (self.centre[0] - self.textures.connecting.get_rect()[2] // 2, self.centre[1] - self.textures.connecting.get_rect()[3] // 2))
        pygame.display.update()
        host, port = (self.interfaces['online'].interact.text[:-1]).split(':')
        self.contact = Client(host, port)
        close(self, 'online', False, None)
        if self.contact.connecting():
            users = ''
            while not self.contact.loaded_map:
                users = self.contact.check_message()
            if users == 'close':
                self.go_back_to_menu(False)
                return
            self.contact.users = users.split('|')
            self.world_coord = len(self.contact.gen.split('\n')) // 2
            self.init_world([[k.split('|') for k in i.split('\t')] for i in self.contact.gen.split('\n')])

    def make_save(self):
        with open(f'saves/{self.name_save}.maiso', mode='w') as file:
            massive = '\n'.join('\t'.join('|'.join(j) for j in i) for i in self.screen_world.biomes)
            info_fractions = '\n'.join([f'{"|".join([i[0], i[1]])}|{"|".join(map(str, i[2]))}' for i in self.info_players])
            file.write(f"{info_fractions}:{massive}")

    def open_save(self):
        self.interfaces = dict()
        show_menu(self, self.centre)
        saves = Interfaces.Save_menu(self.centre, self.textures)
        files = [i for i in os.listdir('saves') if len(i.split('.maiso')) > 1]
        saves.handler = self
        saves.add_saves(files, show_choicegame, self)
        self.interfaces['save_menu'] = saves

    # def check_structure_placement(self, ground, structure):
    #     if ground.biome[0] not in self.rules['StructuresPermissions'][structure]:
    #         print('nelza tut stroit')
    #         # сообщить во всплывающем окошке, что нельзя строить
    #         return False
    #     struct_cost = int(self.rules['StructuresCosts'][self.structures[self.now_structure]][0])
    #     struct_action_pts = int(self.rules['StructuresActionPoints'][self.structures[self.now_structure]][0])
    #     if self.me.action_pts < struct_action_pts:
    #         print("no points((9(")
    #         return False
    #     if self.me.resources < struct_cost:
    #         print('malo denyak, vzuh, and ti bezdomni (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
    #         return False
    #     self.update_placement_state(ground, structure, struct_cost, struct_action_pts)
    #     return True

    def update_placement_state(self, ground, structure, struct_cost, struct_action_pts):
        ground.biome[1] = structure
        self.me.action_pts -= struct_action_pts
        self.me.resources -= struct_cost

    def place_structure(self, ground, structure=None, info=True, me=False):
        if not structure:
            structure = self.structures[self.now_structure]
        if structure != 'null': # я могу строить?
            if (self.me.fraction_name == ground.fraction and me) or not me:
                ground.biome[1] = structure
                try:
                    ground.structure = ClassicStructure(self.textures.animations_structures[structure][0][0], (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2), structure, self.textures)
                except Exception:
                    ground.structure = MainStructure(self.textures.animations_structures[structure][0], (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2), structure, self.textures)
        else:
            ground.structure = None
            ground.biome[1] = "null"
        if 'buildmenu' in self.interfaces:
            self.interfaces.pop('buildmenu')
        if info:
            self.contact.send(f'change-0-' + '|'.join(ground.biome) + '-end-')

    def buy_ground(self, xoy, fraction, buyer):
        biome = self.screen_world.biomes[xoy[0]][xoy[1]]
        ground_cost = int(self.rules['GroundsCosts'][biome[0]][0])
        if buyer.resources >= ground_cost and biome[4] == 'null':
            x = xoy[0] - self.screen_world.world_coord[0]
            y = xoy[1] - self.screen_world.world_coord[1]
            if self.screen_world.sq1 > x >= 0 and self.screen_world.sq2 > y >= 0:
                self.screen_world.great_world[x][y].fraction = fraction
            self.screen_world.biomes[xoy[0]][xoy[1]][4] = fraction
            buyer.resources -= ground_cost
            self.contact.send(f'change-0-' + '|'.join(self.screen_world.biomes[xoy[0]][xoy[1]]) + '-end-')
        elif biome[4] == 'null':
            print('no mani')
        else:
            print('chuzoy rayon')

    def click_handler(self):
        c = None
        for i in pygame.event.get():
            self.camera.event(i)
            if i.type == pygame.QUIT:
                sys.exit()
            if i.type == pygame.KEYDOWN:
                c = i
                if i.key == pygame.K_ESCAPE and not self.open_some:
                    show_pause(self, self.centre) if 'pause' not in self.interfaces else close(self, 'pause', False, None)
                if 'popup_menu' in self.interfaces: self.interfaces.pop('popup_menu')
                if 'buildmenu' in self.interfaces: self.interfaces.pop('buildmenu')
                if 'choicegame' in self.interfaces: self.interfaces.pop('choicegame')
            if i.type == pygame.QUIT:
                sys.exit()
        return c

    def update(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.clock.tick()
        rendering(self, self.screen_world)

    def complete(self):
        pass

    def decoding(self):  # возвращает название протокола и массив
        return [1]