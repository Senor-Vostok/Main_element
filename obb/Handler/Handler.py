import copy

import pygame.display
import math
import obb.Constants
from obb.Objects.Player import Player
from obb.Objects.Bot import Bot
from obb.Image_rendering.Textures import Textures
from obb.Sond_rendering.Sounds import Sounds
from obb.Image_rendering.Machine import World
from obb.Generation import Generation
from obb.Objects.Cam_class import Cam
from obb.Online import *
from obb.Image_rendering.Efffect import Effect
from win32api import GetSystemMetrics
from obb.Objects.Structures import *
from obb.Handler.Handler_show import *
from obb.Constants import *
from obb.Image_rendering.Efffect import Information
from obb.Handler.Handler_render import rendering
from datetime import datetime


class EventHandler:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = dict()
        self.about_structures = dict()
        self.rules = dict()
        self.read_rules()
        self.volumes_channels = [1] * 8
        with open('data/structures/about.txt', mode='rt', encoding='utf-8') as file:
            for inf in file.read().split('\n'):
                self.about_structures[inf.split(':')[0]] = inf.split(':')[1]
        with open('data/user/information', mode='rt') as file:
            self.me = Player(int(file.read()))
        with open('data/user/settings', mode='rt', encoding='utf-8') as file:
            for info in file.read().split('\n'):
                self.settings[info.split(':t:')[0]] = info.split(':t:')[1]
            self.me.nickname = self.settings['nickname']
            self.volumes_channels[0] = float(self.settings['volume'])
            pygame.mixer.Channel(0).set_volume(float(self.settings['volume']))
        self.size = GetSystemMetrics(0), GetSystemMetrics(1)
        self.centre = (self.size[0] // 2, self.size[1] // 2)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
        self.textures = Textures()
        self.screen.blit(self.textures.loading, (self.centre[0] - self.textures.loading.get_rect()[2] // 2, self.centre[1] - self.textures.loading.get_rect()[3] // 2))
        pygame.display.flip()
        self.sounds = Sounds()
        pygame.mouse.set_visible(False)
        pygame.mixer.Channel(0).play(self.sounds.menu, -1)
        self.matr, self.screen_world, self.name_save, self.timer, self.timer_backmusic, self.timer_attack, self.last_interface = None, None, None, None, None, None, None
        self.selected_cells = list()  # Начальная и конечная выбранные клетки
        self.selected_cell = [None, None]
        self.loaded_save = False
        self.world_coord = 0
        self.camera = Cam()
        self.open_some, self.flag = True, True
        self.fractions = ['water', 'fire', 'air', 'earth']
        self.info_players = list()
        self.contact = Unknown()
        self.interfaces = dict()
        self.bots = list()
        self.effects = list()  # Хранит объекты класса Effects
        self.effects_disappearance_resource = list()  # Хранит объекты класса Resources
        self.structures = [i for i in self.textures.animations_structures if 'support' not in i]
        self.supports_structure = [i for i in self.textures.animations_structures if 'support' in i]
        self.military_structure = [i for i in self.textures.animations_structures if i in self.rules['ArmyFromStructures'] and int(self.rules['ArmyFromStructures'][i][0]) > 0]
        self.now_structure = 0
        self.uid = self.textures.font.render(f'UID: {"0" * (len(str(obb.Constants.MAX_UID)) - len(str(self.me.id))) + str(self.me.id)}', False, DEFAULT_COLOR)
        self.version = self.textures.font.render(f'version: {self.settings["version"]}', False, DEFAULT_COLOR)
        self.__xoy_information = [self.centre[0] * 2, self.centre[1] * 2 - self.textures.land['barrier'][0].get_rect()[2]]
        self.__image_information = self.textures.effects['information'][0]

    def change_volume(self, object, channel):
        self.volumes_channels[channel] = object.now_sector / 100  # Проценты
        pygame.mixer.Channel(channel).set_volume(self.volumes_channels[channel])

    def save_settings(self, do='all'):
        if do == 'nickname':
            self.settings[do] = self.interfaces['setting'].nickname.text[:-1]
            self.me.nickname = self.settings[do]
        if do == 'all':
            self.settings['volume'] = str(self.volumes_channels[0])
        with open('data/user/settings', mode='w', encoding='utf-8') as file:
            settings = '\n'.join([':t:'.join([i, self.settings[i]]) for i in self.settings])
            file.write(settings)

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
        if self.camera.mouse_click[3] == obb.Constants.MOUSE_CLICK_RIGHT:
            if 'popup_menu' in self.interfaces:
                self.interfaces.pop('popup_menu')
            if ground.biome[0] != 'barrier':
                show_popup_menu(self, (ground.rect[0] + ground.rect[2], ground.rect[1] + ground.rect[3]), ground, self.me.fraction_name)
        if 'attack' not in self.interfaces:
            if self.camera.mouse_click[3] == 1:
                if self.camera.mouse_click[2] and not self.selected_cell[0]:
                    self.selected_cell[0] = ground.biome + [ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2]
                if self.camera.mouse_click[2] and self.selected_cell[0]:
                    self.selected_cell[1] = ground.biome + [ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2]
            elif self.camera.mouse_click[3] != 1 and self.selected_cell != [None, None]:
                if self.selected_cell[0] != self.selected_cell[1] and int(self.selected_cell[0][5]) > 0 and self.selected_cell[0][4] == self.me.fraction_name:
                    show_selectunions(self, self.centre, self.selected_cell)
                self.selected_cell = [None, None]

    def found_board(self, index, board, flag_centre=None, block_size=0):
        boards = list()
        if flag_centre:
            for i in range(flag_centre[0] - block_size, flag_centre[0] + block_size):
                for j in range(flag_centre[1] - block_size, flag_centre[1] + block_size):
                    if self.screen_world.biomes[i][j][index] in board:
                        boards.append(self.screen_world.biomes[i][j])
        else:
            for i in range(len(self.screen_world.biomes)):
                for j in range(len(self.screen_world.biomes)):
                    if self.screen_world.biomes[i][j][index] in board:
                        boards.append(self.screen_world.biomes[i][j])
        return boards

    def generation(self, size, barrier=BARRIER_SIZE):
        gen = Generation(size, self.screen, self.centre)
        self.world_coord = (size + barrier * 2) // 2
        gen.generation()
        self.matr = gen.add_barrier(barrier)

    def init_player(self, fraction, start_point, resource, potential_resource):
        self.me.fraction_name = fraction
        self.me.potential_resource = potential_resource
        self.me.resources = resource
        self.me.start_point = start_point

    def init_bot(self, fraction, start_point, resource, potential_resource):
        self.bots.append(Bot(len(self.bots), self.structures, self.rules))
        self.bots[-1].fraction_name = fraction
        self.bots[-1].resources = resource
        self.bots[-1].potential_resource = potential_resource
        self.bots[-1].start_point = start_point

    def init_players(self):
        # Эта часть кода для загруженной игры
        if self.loaded_save:
            nicks = f'nicks-0-{"|".join(":t:".join(i[:3]) for i in self.info_players)}-end-'
            for c in range(1, len(self.info_players)):
                uid = self.info_players[c][1]
                if 'bot' in uid:
                    self.init_bot(self.info_players[c][2], self.info_players[c][3], self.info_players[c][4], self.info_players[c][5])
                    self.bots[-1].my_ground = self.found_board(4, self.info_players[c][2])
                else:
                    i = self.contact.users.index(uid)
                    self.contact.send(f"uid-0-{self.info_players[c][2]}|{'_'.join(map(str, self.info_players[c][3]))}|{self.info_players[c][4]}|{self.info_players[c][5]}-end-{nicks}", self.contact.array_clients[i - 1])
            self.init_player(self.info_players[0][2], self.info_players[0][3], self.info_players[0][4], self.info_players[0][5])
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
            barrier = BARRIER_SIZE + 3
            start_point = [random.randint(barrier, len(self.screen_world.biomes) - barrier),
                           random.randint(barrier, len(self.screen_world.biomes) - barrier)]
            while (start_point in start_points) or (not self.check_start_point(start_point)):
                start_point = [random.randint(barrier, len(self.screen_world.biomes) - barrier),
                               random.randint(barrier, len(self.screen_world.biomes) - barrier)]
            start_points.append(start_point)
            self.info_players[c].append([start_point[0], start_point[1]])
            self.screen_world.biomes[start_point[0]][start_point[1]][1] = fraction
            self.info_players[c].append(FIRST_RESOURCES)
            self.info_players[c].append(0)
            message += f'change-0-structure|{fraction}|{start_point[0]}|{start_point[1]}-end-'
            if "bot" in self.info_players[c][1]:
                self.init_bot(self.info_players[c][2], self.info_players[c][3], self.info_players[c][4], 0)
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if "bot" in self.info_players[c][1]:
                        self.bots[-1].my_ground.append(self.screen_world.biomes[start_point[0] + i][start_point[1] + j])
                    self.screen_world.biomes[start_point[0] + i][start_point[1] + j][4] = fraction
                    count_army = f'{random.randint(0, 5)}'
                    self.screen_world.biomes[start_point[0] + i][start_point[1] + j][5] = count_army
                    message += f'change-0-army|{count_army}|{start_point[0] + i}|{start_point[1] + j}-end-'
                    message += f'change-0-fraction|{fraction}|{start_point[0] + i}|{start_point[1] + j}-end-'
        nicks = f'nicks-0-{"|".join(":t:".join(i[:3]) for i in self.info_players)}-end-'
        for c in range(1, len(self.info_players)):
            if 'bot' not in self.info_players[c][1]:
                print(self.info_players[c][2])
                self.contact.send(f"uid-0-{self.info_players[c][2]}|{'_'.join(map(str, self.info_players[c][3]))}|{self.info_players[c][4]}|{0}-end-{nicks}{message}", self.contact.array_clients[c - 1])
        self.init_player(self.info_players[0][2], self.info_players[0][3], self.info_players[0][4], 0)

    def check_start_point(self, start_point):
        for i in range(-2, 3):
            for j in range(-2, 3):
                if self.screen_world.biomes[start_point[0] + i][start_point[1] + j][1] != 'null':
                    return False
        return True

    def init_world(self, matr=None, name_save=None, info_players=None):
        if name_save:
            self.loaded_save = True
            self.name_save = name_save
            self.info_players = info_players
        self.open_some = False
        self.interfaces = dict()
        if not matr:
            self.generation(obb.Constants.SIZE_WORLD)
            matr = self.matr
        self.world_coord = BARRIER_SIZE
        self.screen_world = World(self.screen, self.centre, [self.world_coord, self.world_coord], matr, self)  # создание динамической сетки
        self.screen_world.create()
        if not self.loaded_save:
            self.info_players.append([self.me.nickname, self.me.uid])

    def decode_message(self, message):
        for message in message.split('-end-'):
            try:
                mess = message.split('-0-')
                if mess[0] == 'change':
                    mess = mess[1].split('|')
                    i, j = int(mess[2]), int(mess[3])
                    if mess[0] == 'structure':
                        self.place_structure((i, j), mess[1], False)
                    if mess[0] == 'fraction':
                        self.set_fraction((i, j), mess[1], False)
                    if mess[0] == 'army':
                        self.screen_world.biomes[i][j][5] = mess[1]
                    if mess[0] == 'update':
                        self.screen_world.biomes[i][j] = mess[1:]
                if mess[0] == 'join':
                    if self.contact.private and mess[1].split('|')[1] not in self.contact.whitelist:
                        if self.contact.protocol == 'host':
                            self.contact.array_clients.pop(-1).close()
                    elif mess[1].split('|')[1] != self.me.uid and mess[1].split('|')[1] not in self.contact.users:
                        self.contact.users.append(mess[1].split('|')[1])
                        if not self.loaded_save:
                            self.info_players.append(mess[1].split('|'))
                if mess[0] == 'nicks':
                    print([i.split(':t:') for i in mess[1].split('|')])
                    self.info_players = [i.split(':t:') for i in mess[1].split('|')]
                if mess[0] == 'uid':
                    fraction = mess[1].split('|')[0]
                    coord = [int(i) for i in (mess[1].split('|')[1]).split('_')]
                    resource = int(mess[1].split('|')[2])
                    potential_resource = int(mess[1].split('|')[3])
                    self.init_player(fraction, coord, resource, potential_resource)
                    self.contact.users.append(self.me.uid)
                if mess[0] == 'resource' and self.contact.protocol == 'host':
                    uid = mess[1].split('|')[0]
                    delta_resource = int(mess[1].split('|')[1])
                    self.update_resource(uid, delta_resource)
                if mess[0] == 'presource' and self.contact.protocol == 'host':
                    uid = mess[1].split('|')[0]
                    delta_presource = int(mess[1].split('|')[1])
                    self.update_presource(uid, delta_presource)
                if mess[0] == 'presource(looser)' and self.contact.protocol == 'host':
                    fraction = mess[1].split('|')[0]
                    delta_presource = int(mess[1].split('|')[1])
                    self.update_presourse_looser_edition(fraction, delta_presource)
                if mess[0] == 'host':
                    if mess[1] == 'timer':
                        self.update_resource(self.me.uid, self.me.potential_resource)
                        self.me.resources += self.me.potential_resource
                        show_resources(self, self.me.potential_resource)
                if mess[0] == 'game_over':
                    if mess[1] == self.me.fraction_name:
                        self.me.resources = 0
                        self.me.potential_resource = 0
                        show_end_game(self, self.centre, 'lose')
                    if self.contact.protocol == 'host':
                        self.info_players[[i[2] for i in self.info_players].index(mess[1])][5] = 0
                        self.info_players[[i[2] for i in self.info_players].index(mess[1])][6] = 0
                        for bot in self.bots:
                            if bot.fraction_name == mess[1]:
                                bot.potential_resource = 0
                                bot.resources = 0
            except Exception as e:
                print(e)
            # запрос от таймера

    def load_world(self):
        pygame.mixer.Channel(0).play(random.choice(self.sounds.background))
        self.timer_backmusic = datetime.now()
        self.timer_attack = datetime.now()
        if self.contact.protocol == 'unknown' or self.contact.protocol == 'host':
            self.timer = datetime.now()
            if not self.loaded_save:
                for i in range(len(self.fractions) - len(self.contact.users)):
                    self.info_players.append([random.choice(['Carl', 'Maxim', 'Aleksandr', 'BArber']), f'bot{i}'])
            print('innit_players')
            self.init_players()
        if not self.me.fraction_name:
            return
        self.screen_world.rendering = True
        show_ingame(self, self.centre)
        self.move_to_coord(self.me.start_point)
        if self.name_save:
            self.make_save()

    def machine(self):
        try:
            if self.contact.protocol == 'host': self.decode_message(self.contact.hosting())
            if self.contact.protocol == 'client': self.decode_message(self.contact.check_message())
        except Exception:
            pass
        if len(self.contact.users) + int(bool(self.contact.protocol == "client")) >= self.contact.maxclient + 1 or self.screen_world.rendering:
            if 'ingame' not in self.interfaces:
                self.load_world()
            if self.contact.protocol == 'unknown' or self.contact.protocol == 'host' and self.screen_world.rendering:
                self.get_resource()
                for bot in self.bots:
                    bot.think_smth_please(self)
            if (datetime.now() - self.timer_attack).seconds >= 0.5 and self.selected_cells:
                for cells in self.selected_cells:
                    self.attack(self.me, cells, False)
                self.timer_attack = datetime.now()
            if (datetime.now() - self.timer_backmusic).seconds >= COOLDOWN_MUSIC:
                pygame.mixer.Channel(0).play(random.choice(self.sounds.background))
                self.timer_backmusic = datetime.now()
            self.camera.speed = (self.camera.normal_fps + 1) / (self.clock.get_fps() + 1)
            self.camera.inter()
        else:
            self.screen_world.rendering = False
            self.screen.blit(self.textures.font.render(f'{len(self.contact.users) + int(bool(self.contact.protocol == "client"))}/{self.contact.maxclient + 1}', False, DEFAULT_COLOR), self.centre)
            if 'ingame' in self.interfaces: close(self, 'ingame', False)

    def go_back_to_menu(self, save=True):
        if save:
            self.make_save()
        self.matr, self.screen_world, self.name_save, self.timer, self.timer_backmusic, self.last_interface = None, None, None, None, None, None
        self.selected_cells = list()
        self.selected_cell = [None, None]
        self.loaded_save = False
        self.world_coord = 0
        self.open_some, self.flag = True, True
        self.info_players = list()
        self.contact = Unknown()
        self.interfaces = dict()
        self.bots = list()
        self.effects = list()  # Хранит объекты класса Effects
        self.effects_disappearance_resource = list()  # Хранит объекты класса Resources
        self.now_structure = 0
        pygame.mixer.Channel(0).play(self.sounds.menu, -1)
        show_menu(self, self.centre)

    def move_to_coord(self, coord):
        self.screen_world.world_coord = [coord[0] - self.screen_world.sq2 // 2,
                                         coord[1] - self.screen_world.sq1 // 2]
        self.screen_world.create('static')

    def next_struct(self, ind):
        self.now_structure = (self.now_structure + ind) % len(self.structures) if self.now_structure + ind >= 0 else len(self.structures) - 1
        fs1 = (self.now_structure + 1) % len(self.structures) if self.now_structure + 1 >= 0 else len(self.structures) - 1
        fs2 = (self.now_structure - 1) % len(self.structures) if self.now_structure - 1 >= 0 else len(self.structures) - 1
        self.interfaces['buildmenu'].structure.image = pygame.transform.scale(self.textures.animations_structures[self.structures[self.now_structure]][0][0], (240 * self.textures.resizer, 360 * self.textures.resizer))
        self.interfaces['buildmenu'].s2.image = self.textures.animations_structures[self.structures[fs1]][0][0]
        self.interfaces['buildmenu'].s1.image = self.textures.animations_structures[self.structures[fs2]][0][0]
        struct = self.structures[self.now_structure]
        about = "\n".join(self.about_structures[struct].split("|n|"))
        self.interfaces['buildmenu'].about.new_text(f'Цена: {self.rules["StructuresCosts"][struct][0]}\nДаёт: ресурс - {self.rules["ResourcesFromStructures"][struct][0]}, войско - {self.rules["ArmyFromStructures"][struct][0]}, защита - {self.rules["StructuresProtection"][struct][0]}\nИнформация: {about}')

    def host_game(self, matr):
        if not matr:
            self.generation(obb.Constants.SIZE_WORLD)
            matr = self.matr
        count = int(self.interfaces['online'].count.text[:-1])
        if count < obb.Constants.MIN_COUNT_USERS:
            count = obb.Constants.MIN_COUNT_USERS
        if count > obb.Constants.MAX_COUNT_USERS:
            count = obb.Constants.MAX_COUNT_USERS
        self.contact = Host('0.0.0.0', int(self.interfaces['online'].port.text[:-1]),
                            ':n:'.join(':t:'.join('|'.join(k) for k in i) for i in matr),
                            count - 1, self.loaded_save)
        self.contact.users.append(self.me.uid)
        self.contact.whitelist = [user[1] for user in self.info_players]
        self.init_world(matr)

    def connecting(self):
        self.screen.blit(self.textures.connecting, (self.centre[0] - self.textures.connecting.get_rect()[2] // 2, self.centre[1] - self.textures.connecting.get_rect()[3] // 2))
        pygame.display.update()
        host, port = (self.interfaces['online'].interact.text[:-1]).split(':')
        self.contact = Client(host, port, self.me.nickname)
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
        if not self.name_save:
            return
        with open(f'saves/{self.name_save}.maiso', mode='w') as file:
            massive = ':n:'.join(':t:'.join('|'.join(j) for j in i) for i in self.screen_world.biomes)
            info_fractions = ':n:'.join([f'{i[0]}|{i[1]}|{i[2]}|{"|".join(map(str, i[3]))}|{i[4]}|{i[5]}' for i in self.info_players])
            game = 'local'
            if self.contact.protocol != 'unknown':
                game = 'online'
            file.write(f"{game}:l:{info_fractions}:l:{massive}")

    def open_save(self):
        self.interfaces = dict()
        show_menu(self, self.centre)
        saves = Interfaces.Save_menu(self.centre, self.textures)
        files = [i for i in os.listdir('saves') if len(i.split('.maiso')) > 1]
        saves.handler = self
        saves.add_saves(files, self.init_world, show_online, self)
        self.interfaces['save_menu'] = saves

    def attack(self, attacker, selected, exist=True):
        if int(selected[0][5]) <= int(self.rules['StructuresProtection']['null'][0]):
            return
        prom = copy.deepcopy(selected[1])
        selected[1] = self.nearby_section(selected[0], selected[1])
        first_there = False
        if attacker == self.me and exist:
            count_units = self.interfaces['attack'].drag.now_sector
            delta_units_cnt = self.interfaces['attack'].drag.now_sector - int(selected[1][5])
            first_there = True
            self.interfaces.pop('attack')
        else:
            count_units = int(selected[0][5])
            delta_units_cnt = int(selected[0][5]) - int(selected[1][5])
        i_from = int(selected[0][2])
        j_from = int(selected[0][3])
        i_to = int(selected[1][2])
        j_to = int(selected[1][3])
        ground_from = self.screen_world.biomes[i_from][j_from]
        ground_to = self.screen_world.biomes[i_to][j_to]
        if ground_from[4] == attacker.fraction_name:
            units_from = int(ground_from[5])
            defending_ground_protection = int(self.rules['StructuresProtection'][ground_to[1]][0])
            if ground_to[4] == attacker.fraction_name:
                ground_to[5] = str(delta_units_cnt + int(selected[1][5]) + int(ground_to[5]))
                ground_from[5] = f'{int(ground_from[5]) - count_units}'
                self.contact.send(f'change-0-army|{ground_to[5]}|{ground_to[2]}|{ground_to[3]}-end-')
                self.contact.send(f'change-0-army|{ground_from[5]}|{ground_from[2]}|{ground_from[3]}-end-')
            elif delta_units_cnt > defending_ground_protection:
                if ground_to[1] == ground_to[4] and ground_to[1] != 'null':  # проверка уничтожения главной структуры
                    if attacker == self.me:
                        self.effects.append(Information(self.__xoy_information, f"{ground_from[4]} уничтожили империю {ground_to[4]}", self.textures.resizer, self.__image_information))
                    self.destroy_empire(ground_to[4], ground_from[4], attacker)
                    self.contact.send(f'change-0-army|{ground_to[5]}|{ground_to[2]}|{ground_to[3]}-end-')
                    self.contact.send(f'change-0-army|{ground_from[5]}|{ground_from[2]}|{ground_from[3]}-end-')
                elif ground_to[4] != 'null' and attacker == self.me:
                    self.effects.append(Information(self.__xoy_information, f"{ground_from[4]} успешно атакуют {ground_to[4]}", self.textures.resizer, self.__image_information))
                self.update_presource(attacker.uid, int(self.rules["ResourcesFromStructures"][ground_to[1]][0]))
                attacker.potential_resource += int(self.rules["ResourcesFromStructures"][ground_to[1]][0])
                self.update_presourse_looser_edition(ground_to[4], -int(self.rules["ResourcesFromStructures"][ground_to[1]][0])) if ground_to[4] != 'null' else None
                ground_to[4] = ground_from[4]
                self.set_fraction((int(ground_to[2]), int(ground_to[3])), ground_to[4], True, None)
                ground_from[5] = str(max(0, units_from - delta_units_cnt))
                ground_to[5] = str(max(0, delta_units_cnt))
                self.contact.send(f'change-0-army|{ground_to[5]}|{ground_to[2]}|{ground_to[3]}-end-')
                self.contact.send(f'change-0-army|{ground_from[5]}|{ground_from[2]}|{ground_from[3]}-end-')
            else:
                if ground_to[4] == 'null' and attacker == self.me:
                    self.effects.append(Information(self.__xoy_information, f"{ground_from[4]} не смогли расширить владения", self.textures.resizer, self.__image_information))
                elif attacker == self.me:
                    self.effects.append(Information(self.__xoy_information, f"{ground_from[4]} не смогли захватить клетку {ground_to[4]}", self.textures.resizer, self.__image_information))
                    ground_from[5] = f'{int(int(ground_from[5]) * 0.1)}'
        self.contact.send(f'change-0-fraction|{ground_to[4]}|{ground_to[2]}|{ground_to[3]}-end-')
        self.contact.send(f'change-0-fraction|{ground_from[4]}|{ground_from[2]}|{ground_from[3]}-end-')
        if attacker != self.me:
            for bot in self.bots:
                for ground in bot.my_ground:
                    if ground[2:4] == ground_to[2:4] and ground_to[5] != selected[1][5]:
                        bot.my_ground.remove(ground)
                    elif ground_to[5] == selected[1][5] and ground[2:4] == ground_to[2:4]:
                        bot.my_ground[bot.my_ground.index(ground)] = ground_to
                    elif ground[2:4] == ground_from[2:4]:
                        bot.my_ground[bot.my_ground.index(ground)] = ground_from
            if ground_to[5] != selected[1][5]:
                attacker.my_ground.append(ground_to)
        else:
            selected[0] = selected[1]
            selected[1] = prom
            if selected[0][2:4] == selected[1][2:4]:
                self.selected_cells.remove(selected)
            if first_there and selected not in self.selected_cells:
                self.timer_attack = datetime.now()
                self.selected_cells.append(selected)

    def destroy_empire(self, fraction_old, fraction_new, attacker):
        for i in range(len(self.screen_world.biomes)):
            for j in range(len(self.screen_world.biomes)):
                if self.screen_world.biomes[i][j][4] == fraction_old:
                    if self.screen_world.biomes[i][j][1] not in self.structures:
                        self.place_structure((i, j), 'null')
                    else:
                        attacker.potential_resource += int(self.rules["ResourcesFromStructures"][self.screen_world.biomes[i][j][1]][0])
                        self.update_presource(attacker.uid, int(self.rules["ResourcesFromStructures"][self.screen_world.biomes[i][j][1]][0]))
                    self.set_fraction((i, j), fraction_new, True, None, False)
                    sq_i, sq_j = i - self.screen_world.world_coord[0], j - self.screen_world.world_coord[1]
                    if 0 <= sq_i < self.screen_world.sq2 and 0 <= sq_j < self.screen_world.sq1:
                        ground = self.screen_world.great_world[sq_i][sq_j]  # Объект Ground
                        xoy = (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2)
                        self.effects.append(Effect(xoy, self.textures.effects['place'], True))
        self.contact.send(f'game_over-0-{fraction_old}-end-')
        if fraction_old == self.me.fraction_name:
            show_end_game(self, self.centre, 'lose')
        if self.contact.protocol == 'host' or self.contact.protocol == 'unknown':
            self.info_players[[i[2] for i in self.info_players].index(fraction_old)][4] = 0
            self.info_players[[i[2] for i in self.info_players].index(fraction_old)][5] = 0
            for bot in self.bots:
                if bot.fraction_name == fraction_old:
                    bot.resources = 0
                    bot.potential_resource = 0
        fractions = [0] * (len(self.fractions))
        for i in self.screen_world.biomes:
            for j in i:
                if j[4] != 'null':
                    fractions[self.fractions.index(j[4])] += 1
        if fractions.count(0) == len(self.fractions) - 1:
            show_end_game(self, self.centre, 'win')

    def area(self, ground, buyer):
        if "tower" in ground[1]:
            r = int(self.rules['RadiusAreaForStructures']['tower'][0])
            for i in range(-r, r + 1):
                for j in range(-r, r + 1):
                    x, y = int(ground[2]) + i, int(ground[3]) + j
                    if 'bot' in buyer.uid and self.screen_world.biomes[x][y] not in buyer.my_ground and buyer.fraction_name == self.screen_world.biomes[x][y][4]:
                        buyer.my_ground.append(self.screen_world.biomes[x][y])
                    self.set_fraction((x, y), buyer.fraction_name, True)

    def check_structure_placement(self, ground, structure, buyer):
        if ground[4] != buyer.fraction_name:
            if buyer == self.me:
                self.effects.append(Information(self.__xoy_information, "Эта клетка не принадлежит Вам", self.textures.resizer, self.__image_information))
            return False
        if ground[1] != 'null' and structure != 'null':
            if buyer == self.me:
                self.effects.append(Information(self.__xoy_information, "Здесь стоит другая структура", self.textures.resizer, self.__image_information))
            return False
        if ground[0] not in self.rules['StructuresPermissions'][structure]:
            if buyer == self.me:
                self.effects.append(Information(self.__xoy_information, "Вы не можете строить в этом биоме", self.textures.resizer, self.__image_information))
            return False
        struct_cost = int(self.rules['StructuresCosts'][self.structures[self.now_structure]][0])
        if buyer.resources < struct_cost:
            if buyer == self.me:
                self.effects.append(Information(self.__xoy_information, "Не хватает ресурсов", self.textures.resizer, self.__image_information))
            return False
        if buyer == self.me:
            pygame.mixer.Channel(1).play(self.sounds.draw)
        buyer.resources -= struct_cost
        self.update_resource(buyer.uid, -struct_cost)
        self.update_presource(buyer.uid, int(self.rules['ResourcesFromStructures'][structure][0]))
        buyer.potential_resource += int(self.rules['ResourcesFromStructures'][structure][0])
        return True

    def try_connect_structure(self, coord_ground, structure):
        i, j = coord_ground
        smez_structures = [self.screen_world.biomes[i - 1][j][1],
                           self.screen_world.biomes[i + 1][j][1],
                           self.screen_world.biomes[i][j + 1][1],
                           self.screen_world.biomes[i][j - 1][1]]
        if f'{structure}-support' in self.supports_structure and\
           (structure in smez_structures or f'{structure}-support' in smez_structures):
            return f'{structure}-support'
        return structure

    def place_structure(self, coord_ground, structure=None, info=True, buyer=None):
        i, j = coord_ground[0], coord_ground[1]
        sq_i, sq_j = i - self.screen_world.world_coord[0], j - self.screen_world.world_coord[1]
        in_matrix = 0 <= sq_i < self.screen_world.sq2 and 0 <= sq_j < self.screen_world.sq1
        if not structure:
            structure = self.structures[self.now_structure]
        if buyer and structure != 'null' and not self.check_structure_placement(self.screen_world.biomes[i][j], structure, buyer):
            return
        structure = self.try_connect_structure((i, j), structure)
        self.screen_world.biomes[i][j][1] = structure
        if structure != 'null' and in_matrix:
            pygame.mixer.Channel(2).play(self.sounds.place)
            ground = self.screen_world.great_world[sq_i][sq_j]  # Объект Ground
            xoy = (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2)
            self.effects.append(Effect(xoy, self.textures.effects['place'], True))
            if structure in self.structures + self.supports_structure:
                image = self.textures.animations_structures[structure][0][0]
                ground.structure = ClassicStructure(image, xoy, structure, self.textures)
            else:
                image = self.textures.animations_main_structures[structure][0][0]
                ground.structure = MainStructure(image, xoy, structure, self.textures)
        elif in_matrix and structure == 'null':
            ground = self.screen_world.great_world[sq_i][sq_j]
            if buyer and not isinstance(ground.structure, MainStructure) and buyer.fraction_name == ground.biome[4]:
                buyer.potential_resource -= int(self.rules["ResourcesFromStructures"][ground.biome[1]][0])
                self.update_presource(buyer.uid, -int(self.rules["ResourcesFromStructures"][ground.biome[1]][0]))
                ground.structure = None
            elif not buyer:
                ground.structure = None
            else:
                structure = ground.biome[1]
        if buyer:
            self.area(self.screen_world.biomes[i][j], buyer)
        if buyer == self.me:
            if 'buildmenu' in self.interfaces: close(self, 'buildmenu', False)
        if info:
            self.contact.send(f'change-0-structure|{structure}|{i}|{j}-end-')

    def set_fraction(self, coord_ground, fraction, info=True, buyer=None, stability=True):
        i, j = coord_ground[0], coord_ground[1]
        sq_i, sq_j = i - self.screen_world.world_coord[0], j - self.screen_world.world_coord[1]
        in_matrix = 0 <= sq_i < self.screen_world.sq2 and 0 <= sq_j < self.screen_world.sq1
        if self.screen_world.biomes[i][j][0] == 'barrier':
            return
        if self.screen_world.biomes[i][j][4] != 'null' and info and stability:
            return
        if in_matrix:
            ground = self.screen_world.great_world[sq_i][sq_j]  # Объект Ground
            xoy = (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2)
            self.effects.append(Effect(xoy, self.textures.effects['set'], True, 10))
        if buyer:
            ground_cost = int(self.rules['GroundsCosts'][self.screen_world.biomes[i][j][0]][0])
            if buyer.resources >= ground_cost:
                self.update_resource(buyer.uid, -ground_cost)  # Мы не можем заглянуть в me у другого игрока (ПРОБЛМЕА)
                buyer.resources -= ground_cost
                self.screen_world.biomes[i][j][4] = fraction  # А это решение этого (выше смотри строчку)
        else:
            self.screen_world.biomes[i][j][4] = fraction
        if info:
            self.contact.send(f'change-0-fraction|{fraction}|{i}|{j}-end-')

    def nearby_section(self, start, end):
        dx = int(end[2]) - int(start[2])
        dy = int(end[3]) - int(start[3])
        delta_x = 0
        delta_y = 0
        v1 = (int(end[2]) - int(start[2]), int(end[3]) - int(start[3]))
        if abs(dx) < abs(dy):
            helppoint = [int(end[2]), int(start[3])]
        else:
            helppoint = [int(start[2]), int(end[3])]
        v2 = (helppoint[0] - int(start[2]), helppoint[1] - int(start[3]))
        if v2 != (0, 0):
            cosl = (v1[0] * v2[0] + v1[1] * v2[1]) / (((v1[0] ** 2 + v1[1] ** 2) ** 0.5) * ((v2[0] ** 2 + v2[1] ** 2) ** 0.5))
            l = math.acos(cosl) * (180 / math.pi)
        else:
            l = 0
        if l > 73 or l == 0:
            if abs(dx) > abs(dy):
                delta_x = 1 if dx > 0 else -1
            else:
                delta_y = 1 if dy > 0 else -1
            return self.screen_world.biomes[int(start[2]) + delta_x][int(start[3]) + delta_y]
        else:
            delta_x = 1 if dx > 0 else -1
            delta_y = 1 if dy > 0 else -1
            return self.screen_world.biomes[int(start[2]) + delta_x][int(start[3]) + delta_y]

    def update_resource(self, uid, delta_resource):
        if self.contact.protocol == 'host' or self.contact.protocol == 'unknown':
            ind = [i[1] for i in self.info_players].index(uid)
            self.info_players[ind][4] += delta_resource
        else:
            self.contact.send(f'resource-0-{uid}|{delta_resource}-end-')

    def update_presource(self, uid, delta_presource):
        if self.contact.protocol == 'host' or self.contact.protocol == 'unknown':
            ind = [i[1] for i in self.info_players].index(uid)
            self.info_players[ind][5] += delta_presource
        else:
            self.contact.send(f'presource-0-{uid}|{delta_presource}-end-')

    def update_presourse_looser_edition(self, fraction, delta_presource):
        if self.contact.protocol == 'host' or self.contact.protocol == 'unknown':
            ind = [i[2] for i in self.info_players].index(fraction)
            self.info_players[ind][5] += delta_presource
        else:
            self.contact.send(f'presource(looser)-0-{fraction}|{delta_presource}-end-')

    def get_resource(self):
        if (datetime.now() - self.timer).seconds >= COOLDOWN:
            self.timer = datetime.now()
            self.contact.send(f'host-0-timer-end-')
            self.update_resource(self.me.uid, self.me.potential_resource)
            self.me.resources += self.me.potential_resource
            show_resources(self, self.me.potential_resource)
            for bot in self.bots:
                self.update_resource(bot.uid, bot.potential_resource)
                bot.resources += bot.potential_resource
            for board in self.found_board(1, self.military_structure):
                board[5] = f'{int(board[5]) + int(self.rules["ArmyFromStructures"][board[1]][0])}'
                self.contact.send(f'change-0-army|{int(board[5]) + int(self.rules["ArmyFromStructures"][board[1]][0])}|{board[2]}|{board[3]}-end-')

    def click_handler(self):
        c = None
        for i in pygame.event.get():
            self.camera.event(i)
            if i.type == pygame.KEYDOWN:
                c = i
                if i.key == pygame.K_ESCAPE:
                    if len(self.interfaces) > 1:
                        self.interfaces.pop([_ for _ in self.interfaces if self.interfaces[_] == self.last_interface][0])
                        continue
                    show_pause(self, self.centre) if 'pause' not in self.interfaces and not self.open_some else None
                if 'popup_menu' in self.interfaces: self.interfaces.pop('popup_menu')
                if 'buildmenu' in self.interfaces: self.interfaces.pop('buildmenu')
                if 'choicegame' in self.interfaces: self.interfaces.pop('choicegame')
            if i.type == pygame.QUIT:
                self.quit()
            if i.type == pygame.MOUSEWHEEL:
                self.next_struct(int(i.precise_y)) if 'buildmenu' in self.interfaces else None
        return c

    def update(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.clock.tick()
        rendering(self, self.screen_world)

    def quit(self):
        self.save_settings()
        if self.contact.sock:
            self.contact.sock.close()
        sys.exit()