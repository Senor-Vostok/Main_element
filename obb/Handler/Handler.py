import os
import pygame.display
from obb.Objects.Player import Player
from obb.Objects.Bot import Bot
from obb.Image_rendering.Textures import Textures
from obb.Image_rendering.Machine import World
from obb.Generation import Generation
from obb.Objects.Cam_class import Cam
from obb.Online import *
from win32api import GetSystemMetrics
from obb.Objects.Structures import *
from obb.Handler.Handler_show import *
from obb.Constants import DEFAULT_COLOR, BACKGROUND_COLOR, BARRIER_SIZE, Y_TEXT_INFORMATION, FIRST_RESOURCES
from obb.Image_rendering.Efffect import Information
from obb.Handler.Handler_render import rendering


class EventHandler:
    def __init__(self):  # TODO: исправить присваивание bot_id и id
        pygame.init()
        with open('data/user/information', mode='rt') as file:
            self.me = Player(int(file.read()))
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
        self.info_players = list()
        self.contact = Unknown()
        self.interfaces = dict()
        self.bots = list()

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

    def found_fractions_board(self, fraction):
        boards = list()
        for i in range(len(self.screen_world.biomes)):
            for j in range(len(self.screen_world.biomes)):
                if self.screen_world.biomes[i][j][4] == fraction:
                    boards.append(self.screen_world.biomes[i][j])
        return boards

    def generation(self, size=200, barrier=BARRIER_SIZE):
        gen = Generation(size, self.screen, self.centre)
        self.world_coord = (size + barrier * 2) // 2
        gen.generation()
        self.matr = gen.add_barrier(barrier)

    def init_player(self, fraction, start_point, resource):
        self.me.fraction_name = fraction
        self.me.resources = resource
        self.me.start_point = start_point

    def init_bot(self, fraction, start_point, resource):
        self.bots.append(Bot(len(self.bots)))
        self.bots[-1].fraction_name = fraction
        self.bots[-1].resources = resource
        self.bots[-1].start_point = start_point

    def init_players(self):
        # Эта часть кода для загруженной игры
        if len(self.info_players[0]) > 1:
            print(self.info_players)
            for c in range(1, len(self.info_players)):
                uid = self.info_players[c][0]
                if 'bot' in uid:
                    self.init_bot(self.info_players[c][1], self.info_players[c][2], self.info_players[c][3])
                    self.bots[-1].my_ground = self.found_fractions_board(self.info_players[c][1])
                else:
                    i = self.contact.users.index(uid)
                    self.contact.send(f"uid-0-{self.info_players[c][1]}|{'_'.join(map(str, self.info_players[c][2]))}|{str(self.info_players[c][3])}-end-", self.contact.array_clients[i - 1])
            self.init_player(self.info_players[0][1], self.info_players[0][2], self.info_players[0][3])
            return
        # Эта часть кода для новой игры
        whitelist = list()
        start_points = list()
        message = ''
        for c in range(len(self.info_players)):
            fraction = random.choice(self.fractions)  # создание фракции
            while fraction in whitelist:
                fraction = random.choice(self.fractions)
            whitelist.append(fraction)
            self.info_players[c].append(fraction)
            start_point = [random.randint(BARRIER_SIZE, len(self.screen_world.biomes) - BARRIER_SIZE),
                           random.randint(BARRIER_SIZE, len(self.screen_world.biomes) - BARRIER_SIZE)]
            while start_point in start_points:
                start_point = [random.randint(BARRIER_SIZE, len(self.screen_world.biomes) - BARRIER_SIZE),
                               random.randint(BARRIER_SIZE, len(self.screen_world.biomes) - BARRIER_SIZE)]
            start_points.append(start_point)
            self.info_players[c].append([start_point[0], start_point[1]])
            self.screen_world.biomes[start_point[0]][start_point[1]][1] = fraction
            self.info_players[c].append(FIRST_RESOURCES)
            message += f'change-0-structure|{fraction}|{start_point[0]}|{start_point[1]}-end-'
            if "bot" in self.info_players[c][0]:
                self.init_bot(self.info_players[c][1], self.info_players[c][2], self.info_players[c][3])
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if "bot" in self.info_players[c][0]:
                        self.bots[-1].my_ground.append(self.screen_world.biomes[start_point[0] + i][start_point[1] + j])
                    self.screen_world.biomes[start_point[0] + i][start_point[1] + j][4] = fraction
                    message += f'change-0-fraction|{fraction}|{start_point[0] + i}|{start_point[1] + j}-end-'
        for c in range(1, len(self.info_players)):
            if 'bot' not in self.info_players[c][0]:
                self.contact.send(f"uid-0-{self.info_players[c][1]}|{'_'.join(map(str, self.info_players[c][2]))}|{str(self.info_players[c][3])}-end-{message}", self.contact.array_clients[c - 1])
        self.init_player(self.info_players[0][1], self.info_players[0][2], self.info_players[0][3])

    def init_world(self, matr=None):
        self.open_some = False
        self.interfaces = dict()
        if not matr:
            self.generation(100)
            matr = self.matr
        self.world_coord = BARRIER_SIZE
        self.screen_world = World(self.screen, self.centre, [self.world_coord, self.world_coord], matr, self)  # создание динамической сетки
        self.screen_world.create()
        if not self.loaded_save:
            self.info_players.append([self.me.uid])

    def decode_message(self, message):
        for message in message.split('-end-'):
            mess = message.split('-0-')
            print(mess)
            if mess[0] == 'change':
                mess = mess[1].split('|')
                i, j = int(mess[2]), int(mess[3])
                if mess[0] == 'structure':
                    self.place_structure((i, j), mess[1], False)
                if mess[0] == 'fraction':
                    self.set_fraction((i, j), mess[1], False)
            if mess[0] == 'join':
                if self.contact.private and mess[1].split('|')[1] not in self.contact.whitelist:
                    if self.contact.protocol == 'host':
                        self.contact.array_clients.pop(-1).close()
                elif mess[1].split('|')[1] != self.me.uid and mess[1].split('|')[1] not in self.contact.users:
                    self.contact.users.append(mess[1].split('|')[1])
                    if not self.loaded_save:
                        self.info_players.append([mess[1].split('|')[1]])
            if mess[0] == 'uid':
                fraction = mess[1].split('|')[0]
                coord = [int(i) for i in (mess[1].split('|')[1]).split('_')]
                resource = int(mess[1].split('|')[2])
                self.init_player(fraction, coord, resource)
                self.contact.users.append(self.me.uid)

    def machine(self):
        try:
            if self.contact.protocol == 'host': self.decode_message(self.contact.hosting())
            if self.contact.protocol == 'client': self.decode_message(self.contact.check_message())
        except Exception:
            pass
        if len(self.contact.users) + int(bool(self.contact.protocol == "client")) >= self.contact.maxclient + 1:

            if not self.screen_world.rendering:
                if self.contact.protocol == 'unknown' or self.contact.protocol == 'host':
                    if not self.loaded_save:
                        for i in range(4 - len(self.contact.users)):
                            self.info_players.append([f'bot{i}'])
                    self.init_players()
                if not self.me.fraction_name:
                    return
                show_ingame(self, self.centre)
                self.move_to_coord(self.me.start_point)
                if self.name_save:
                    self.make_save()

            for bot in self.bots:
                bot.think_smth_please(self)
            self.screen_world.rendering = True
            self.camera.speed = (self.camera.normal_fps + 1) / (self.clock.get_fps() + 1)
            self.camera.inter()
        else:
            self.screen_world.rendering = False
            self.screen.blit(self.textures.font.render(f'{len(self.contact.users) + int(bool(self.contact.protocol == "client"))}/{self.contact.maxclient + 1}', False, DEFAULT_COLOR), self.centre)
            if 'ingame' in self.interfaces: close(self, 'ingame', False)

    def go_back_to_menu(self, save=True):
        if save:
            self.make_save()
        self.matr, self.screen_world, self.name_save = None, None, None
        self.world_coord = 0
        self.open_some, self.flag = True, True
        self.contact = Unknown()
        self.info_players = list()
        self.loaded_save = False
        self.interfaces = dict()
        self.effects = list()
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
        pass

    def host_game(self, matr):
        if not matr:
            self.generation(100)
            matr = self.matr
        count = int(self.interfaces['online'].count.text[:-1])
        if count < 2:
            count = 2
        if count > 4:
            count = 4
        self.contact = Host('0.0.0.0', int(self.interfaces['online'].port.text[:-1]),
                            ':n:'.join(':t:'.join('|'.join(k) for k in i) for i in matr),
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
            self.world_coord = len(self.contact.gen.split(':n:')) // 2
            self.init_world([[k.split('|') for k in i.split(':t:')] for i in self.contact.gen.split(':n:')])

    def make_save(self):
        with open(f'saves/{self.name_save}.maiso', mode='w') as file:
            massive = ':n:'.join(':t:'.join('|'.join(j) for j in i) for i in self.screen_world.biomes)
            info_fractions = ':n:'.join([f'{"|".join([i[0], i[1]])}|{"|".join(map(str, i[2]))}|{str(i[3])}' for i in self.info_players])
            file.write(f"{info_fractions}:l:{massive}")

    def open_save(self):
        self.interfaces = dict()
        show_menu(self, self.centre)
        saves = Interfaces.Save_menu(self.centre, self.textures)
        files = [i for i in os.listdir('saves') if len(i.split('.maiso')) > 1]
        saves.handler = self
        saves.add_saves(files, show_choicegame, self)
        self.interfaces['save_menu'] = saves

    def update_placement_state(self, ground, structure, struct_cost, struct_action_pts):
        ground.biome[1] = structure
        self.me.resources -= struct_cost

    def area(self, ground, buyer):
        if ground[1] == "tower":
            for i in range(-2, 3):
                for j in range(-2, 3):
                    x, y = int(ground[2]) + i, int(ground[3]) + j
                    if 0 <= buyer.id <= 3 and self.screen_world.biomes[x][y] not in buyer.my_ground:
                        buyer.my_ground.append(self.screen_world.biomes[x][y])
                    self.set_fraction((x, y), buyer.fraction_name, True)

    def place_structure(self, coord_ground, structure=None, info=True, buyer=None):
        i, j = coord_ground[0], coord_ground[1]
        sq_i, sq_j = i - self.screen_world.world_coord[0], j - self.screen_world.world_coord[1]
        in_matrix = 0 <= sq_i < self.screen_world.sq2 and 0 <= sq_j < self.screen_world.sq1
        if not structure:
            structure = self.structures[self.now_structure]
        if self.screen_world.biomes[i][j][1] != 'null':
            return
        self.screen_world.biomes[i][j][1] = structure
        if structure != 'null' and in_matrix:
            ground = self.screen_world.great_world[sq_i][sq_j]  # Объект Ground
            xoy = (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2)
            image = self.textures.animations_structures[structure][0][0]
            if structure in self.structures:
                ground.structure = ClassicStructure(image, xoy, structure, self.textures)
            else:
                ground.structure = MainStructure(image, xoy, structure, self.textures)
        elif in_matrix and structure == 'null':
            ground = self.screen_world.great_world[sq_i][sq_j]
            ground.structure = None
        if buyer:
            self.area(self.screen_world.biomes[i][j], buyer)
        if buyer == self.me:
            if 'buildmenu' in self.interfaces: close(self, 'buildmenu', False)
        if info:
            self.contact.send(f'change-0-structure|{structure}|{i}|{j}-end-')

    def set_fraction(self, coord_ground, fraction, info=True, buyer=None):
        i, j = coord_ground[0], coord_ground[1]
        if self.screen_world.biomes[i][j][4] != 'null':
            return
        self.screen_world.biomes[i][j][4] = fraction
        if buyer:
            ground_cost = int(self.rules['GroundsCosts'][self.screen_world.biomes[i][j][0]][0])
            if buyer.resources >= ground_cost:
                buyer.resources -= ground_cost
        if info:
            self.contact.send(f'change-0-fraction|{fraction}|{i}|{j}-end-')

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
            if i.type == pygame.MOUSEWHEEL:
                self.next_struct(int(i.precise_y)) if 'buildmenu' in self.interfaces else None
        return c

    def update(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.clock.tick()
        rendering(self, self.screen_world)