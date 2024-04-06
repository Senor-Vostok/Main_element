import os
import pygame.display
import obb.Objects.Player as Player
import obb.Objects.Bot as Bot
from obb.Image_rendering.Textures import Textures
from obb.Image_rendering.Machine import World
from obb.Generation import Generation
from obb.Objects.Cam_class import Cam
from obb.Online import *
from win32api import GetSystemMetrics, EnumDisplaySettings, EnumDisplayDevices
from obb.Objects.Structures import *
from obb.Handler.Handler_show import *
from obb.Constants import DEFAULT_COLOR, BACKGROUND_COLOR
from obb.Handler.Handler_render import rendering


class EventHandler:
    def __init__(self, bot_id, id, bot_fraction, fraction, bot_start_point, start_point):  # TODO: исправить присваивание bot_id и id
        pygame.init()
        settings = EnumDisplaySettings(EnumDisplayDevices().DeviceName, -1)
        self.vsync_fps = int(getattr(settings, 'DisplayFrequency'))
        self.bot = Bot.Bot(bot_id)  # TODO: убрать
        self.me = Player.Player(id)
        self.textures = Textures()
        self.size = GetSystemMetrics(0), GetSystemMetrics(1)
        self.centre = (self.size[0] // 2, self.size[1] // 2)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        self.screen.set_alpha(None)
        pygame.mouse.set_visible(False)
        self.matr, self.screen_world, self.name_save = None, None, None
        self.bot_fraction = bot_fraction  # TODO: убрать
        self.bot_start_point = bot_start_point  # TODO: убрать
        self.world_coord = 0
        self.camera = Cam()
        self.open_some, self.flag = True, True
        self.ids = [3, 4]  # id игроков
        self.players = []
        self.fractions = ['water', 'fire']  # TODO: добавить выбор фракций  # TODO: убрать
        self.start_points = [(210, 30), (30, 30)]
        self.turn = None  # Чей ход
        self.contact = Unknown()
        self.player = None
        self.end = None
        self.interfaces = dict()
        self.effects = list()
        self.pressed = False
        self.structures = [i for i in self.textures.animations_structures]
        self.now_structure = 0
        self.rules = dict()
        self.read_rules()
        self.init_player(fraction, start_point)

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

    def init_bot(self, fraction, start_point):
        self.bot.fraction_name = fraction
        self.bot.units_count = 100
        self.bot.action_pts = 2e10
        self.bot.resources = 15e10
        self.bot.start_point = start_point
        self.run_bot()

    def run_bot(self):
        self.bot.buy_smth(self)
        # self.bot.build_smth(self, 0)

    def init_players(self):
        for i in range(len(self.fractions)):
            # (soon) перенести в серверную часть:
            # new_player = Player.Player(id)
            # fraction = random.choice(self.fractions)  # назначение фракции игроку
            # new_player.fraction_name = fraction
            # self.fractions.remove(new_player.fraction_name)
            # new_player.units_count = 100  # стартовое кол-во людей в поселении
            # new_player.resources = 15  # стартовый капитал
            # new_player.action_pts = 2
            # new_player.start_point = random.choice(self.start_points)  # спавн в угле мира
            # self.start_points.remove(new_player.start_point)
            # self.players.append(new_player)
            self.matr[self.start_points[i][0]][self.start_points[i][1]][1] = self.fractions[i]  # спавн центральной структуры

    def init_world(self, matr=None):
        self.open_some = False
        self.interfaces = dict()
        if not matr:
            self.generation(200)
            matr = self.matr
        if self.name_save:
            with open(f'saves/{self.name_save}.maiso', mode='w') as file:
                file.write('\n'.join('\t'.join('|'.join(j) for j in i) for i in matr))
        self.world_coord = len(matr) // 2
        self.screen_world = World(self.screen, self.centre, [self.world_coord, self.world_coord], matr, self)  # создание динамической сетки
        self.screen_world.create()
        show_ingame(self, self.centre)
        self.init_players()
        if self.contact.protocol == 'unknown':
            self.init_bot(self.bot_fraction, self.bot_start_point)

    def decode_message(self, message):
        message = message.split('-0-')
        if message[0] == 'change':
            i, j = int(message[1].split('|')[2]), int(message[1].split('|')[3])
            self.screen_world.biomes[i][j][1] = message[1].split('|')[1]
            self.place_structure(self.screen_world.great_world[i - self.screen_world.world_cord[0]][j - self.screen_world.world_cord[1]], message[1].split('|')[1], False)
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
            self.screen_world.rendering = True
            self.camera.inter()
        else:
            self.screen.blit(self.textures.font.render(f'{len(self.contact.users)}/{self.contact.maxclient + 1}', False, DEFAULT_COLOR), self.centre)
            if 'ingame' in self.interfaces: close(self, 'ingame', False)

    def go_back_to_menu(self):
        self.make_save()
        self.open_some = True
        self.interfaces = dict()
        show_menu(self, self.centre)
        self.screen_world = None

    def next_struct(self, ind):
        self.now_structure = (self.now_structure + ind) % len(self.structures) if self.now_structure + ind >= 0 else len(
            self.structures) - 1
        self.interfaces['buildmenu'].structure.image = pygame.transform.scale(self.textures.animations_structures[self.structures[self.now_structure]][0], (360 * self.textures.resizer, 540 * self.textures.resizer))

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
        self.screen.blit(self.textures.connecting, (self.centre[0] - self.textures.connecting.get_rect()[2] // 2, self.centre[1] - self.textures.connecting.get_rect()[3] // 2))
        pygame.display.update()
        host, port = (self.interfaces['online'].interact.text[:-1]).split(':')
        self.contact = Client(host, port)
        close(self, 'online', False, None)
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

    def check_structure_placement(self, ground, structure):
        if ground.biome[0] not in self.rules['StructuresPermissions'][structure]:
            print('nelza tut stroit')
            # сообщить во всплывающем окошке, что нельзя строить
            return False
        struct_cost = int(self.rules['StructuresCosts'][self.structures[self.now_structure]][0])
        struct_action_pts = int(self.rules['StructuresActionPoints'][self.structures[self.now_structure]][0])
        if self.me.action_pts < struct_action_pts:
            print("no points((9(")
            return False
        if self.me.resources < struct_cost:
            print('malo denyak, vzuh, and ti bezdomni (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
            return False
        self.update_placement_state(ground, structure, struct_cost, struct_action_pts)
        return True

    def update_placement_state(self, ground, structure, struct_cost, struct_action_pts):
        ground.biome[1] = structure
        self.me.action_pts -= struct_action_pts
        self.me.resources -= struct_cost

    def place_structure(self, ground, structure=None, info=True):
        if not structure:
            structure = self.structures[self.now_structure]
        if structure != 'null':
            ground.structure = ClassicStructure(self.textures.animations_structures[structure][0], (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2), structure, self.textures)
        else:
            ground.structure = None
        ground.biome[1] = structure
        if 'buildmenu' in self.interfaces:
            self.interfaces.pop('buildmenu')
        if info:
            self.contact.send(f'change-0-' + '|'.join(ground.biome))

    def check_resources(self, ground_cost, buyer):  # TODO убрать
        return buyer.resources >= ground_cost

    def buy_ground(self, xoy, fraction, buyer):
        biome = self.screen_world.biomes[xoy[0]][xoy[1]][0]
        ground_cost = int(self.rules['GroundsCosts'][biome][0])
        if self.check_resources(ground_cost, buyer):
            self.screen_world.biomes[xoy[0]][xoy[1]][4] = fraction
            buyer.resources -= ground_cost
        else:
            print('no mani')

    def click_handler(self):
        c = None
        for i in pygame.event.get():
            self.camera.event(i)
            if i.type == pygame.QUIT:
                sys.exit()
            if i.type == pygame.KEYDOWN and self.decoding()[0] == self.me.id:
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
        self.clock.tick()
        rendering(self, self.screen_world)

    def complete(self):
        pass

    def decoding(self):  # возвращает название протокола и массив
        return [1]