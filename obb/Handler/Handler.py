import pygame.display
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
from obb.Constants import DEFAULT_COLOR, BACKGROUND_COLOR, BARRIER_SIZE, FIRST_RESOURCES, COOLDOWN, COOLDOWN_MUSIC
from obb.Image_rendering.Efffect import Information
from obb.Handler.Handler_render import rendering
from datetime import datetime


class EventHandler:
    def __init__(self):  # TODO: исправить присваивание bot_id и id
        pygame.init()
        pygame.mixer.init()
        with open('data/user/information', mode='rt') as file:
            self.me = Player(int(file.read()))
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
        self.matr, self.screen_world, self.name_save, self.timer, self.timer_backmusic = None, None, None, None, None
        self.selected_cells = [None, None]  # Начальная и конечная выбранные клетки
        self.loaded_save, self.pressed = False, False
        self.world_coord = 0
        self.camera = Cam()
        self.open_some, self.flag = True, True
        self.fractions = ['water', 'fire', 'air', 'earth']
        self.info_players = list()
        self.contact = Unknown()
        self.interfaces = dict()
        self.bots = list()
        self.effects = list()  # Обрабатывает объекты класса Effects
        self.effects_disappearance_resource = list()  # Обрабатывает объекты класса Resources
        self.structures = [i for i in self.textures.animations_structures if 'support' not in i]
        self.supports_structure = [i for i in self.textures.animations_structures if 'support' in i]
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
        elif self.camera.mouse_click[3] == 1:
            if self.camera.mouse_click[2] and not self.selected_cells[0]:
                self.selected_cells[0] = ground.biome
            if self.camera.mouse_click[2] and self.selected_cells[0]:
                self.selected_cells[1] = ground.biome
        elif self.camera.mouse_click[3] != 1 and self.selected_cells != [None, None]:  # вызывается если выделили клетки
            #если режим атаки:
            self.attack(self.me) #исправить attacker для ботов
            print(self.selected_cells)   # тут делать чёта 0 индекс начальная клетка, 1 индекс конечная
            self.selected_cells = [None, None]

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

    def init_player(self, fraction, start_point, resource, potential_resource):
        self.me.fraction_name = fraction
        self.me.potential_resource = potential_resource
        self.me.resources = resource
        self.me.start_point = start_point

    def init_bot(self, fraction, start_point, resource, potential_resource):
        self.bots.append(Bot(len(self.bots), self.structures))
        self.bots[-1].fraction_name = fraction
        self.bots[-1].resources = resource
        self.bots[-1].potential_resource = potential_resource
        self.bots[-1].start_point = start_point

    def init_players(self):
        # Эта часть кода для загруженной игры
        if len(self.info_players[0]) > 1:
            for c in range(1, len(self.info_players)):
                uid = self.info_players[c][0]
                if 'bot' in uid:
                    self.init_bot(self.info_players[c][1], self.info_players[c][2], self.info_players[c][3], self.info_players[c][4])
                    self.bots[-1].my_ground = self.found_fractions_board(self.info_players[c][1])
                else:
                    i = self.contact.users.index(uid)
                    self.contact.send(f"uid-0-{self.info_players[c][1]}|{'_'.join(map(str, self.info_players[c][2]))}|{self.info_players[c][3]}|{self.info_players[c][4]}-end-", self.contact.array_clients[i - 1])
            self.init_player(self.info_players[0][1], self.info_players[0][2], self.info_players[0][3], self.info_players[0][4])
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
            barrier = BARRIER_SIZE + 5
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
            if "bot" in self.info_players[c][0]:
                self.init_bot(self.info_players[c][1], self.info_players[c][2], self.info_players[c][3], 0)
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if "bot" in self.info_players[c][0]:
                        self.bots[-1].my_ground.append(self.screen_world.biomes[start_point[0] + i][start_point[1] + j])
                    self.screen_world.biomes[start_point[0] + i][start_point[1] + j][4] = fraction
                    if "bot" in self.info_players[c][0]: # 1 человек в каждую клетку для теста
                        self.screen_world.biomes[start_point[0] + i][start_point[1] + j][5] = '1'
                    else:
                        self.screen_world.biomes[start_point[0] + i][start_point[1] + j][5] = '10'
                    message += f'change-0-fraction|{fraction}|{start_point[0] + i}|{start_point[1] + j}-end-'
        for c in range(1, len(self.info_players)):
            if 'bot' not in self.info_players[c][0]:
                self.contact.send(f"uid-0-{self.info_players[c][1]}|{'_'.join(map(str, self.info_players[c][2]))}|{self.info_players[c][3]}|{0}-end-{message}", self.contact.array_clients[c - 1])
        self.init_player(self.info_players[0][1], self.info_players[0][2], self.info_players[0][3], 0)

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
            if mess[0] == 'host':
                if mess[1] == 'timer':
                    self.update_resource(self.me.uid, self.me.potential_resource)
                    self.me.resources += self.me.potential_resource
            # запрос от таймера

    def load_world(self):
        pygame.mixer.Channel(0).play(random.choice(self.sounds.background))
        self.timer_backmusic = datetime.now()
        if self.contact.protocol == 'unknown' or self.contact.protocol == 'host':
            self.timer = datetime.now()
            if not self.loaded_save:
                for i in range(len(self.fractions) - len(self.contact.users)):
                    self.info_players.append([f'bot{i}'])
            self.init_players()
        if not self.me.fraction_name:
            return
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
        if len(self.contact.users) + int(bool(self.contact.protocol == "client")) >= self.contact.maxclient + 1:
            if not self.screen_world.rendering:
                self.load_world()
            if self.contact.protocol == 'unknown' or self.contact.protocol == 'host':
                self.get_resource()
            for bot in self.bots:
                bot.think_smth_please(self)
            if (datetime.now() - self.timer_backmusic).seconds >= COOLDOWN_MUSIC:
                pygame.mixer.Channel(0).play(random.choice(self.sounds.background))
                self.timer_backmusic = datetime.now()
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
        self.matr, self.screen_world, self.name_save, self.timer = None, None, None, None
        self.loaded_save, self.pressed = False, False
        self.world_coord = 0
        self.open_some, self.flag = True, True
        self.info_players = list()
        self.contact = Unknown()
        self.interfaces = dict()
        self.bots = list()
        self.effects = list()  # Обрабатывает объекты класса Effects
        self.effects_disappearance_resource = list()  # Обрабатывает объекты класса Resources
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
            info_fractions = ':n:'.join([f'{"|".join([i[0], i[1]])}|{"|".join(map(str, i[2]))}|{i[3]}|{i[4]}' for i in self.info_players])
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

    def attack(self, attacker):
        y = self.centre[1] * 2 - 60 * self.textures.resizer

        i_from = int(self.selected_cells[0][2])
        j_from = int(self.selected_cells[0][3])

        i_to = int(self.selected_cells[1][2])
        j_to = int(self.selected_cells[1][3])

        if (abs(i_to - i_from) > 1) or ((abs(j_to - j_from) > 1)):
            self.effects.append(Information(y, "Атаковать можно только соседнюю клетку", self.textures.resizer))
            return

        ground_from = self.screen_world.biomes[i_from][j_from]
        ground_to = self.screen_world.biomes[i_to][j_to]

        if ground_from[4] == attacker.fraction_name:
            if ground_to[4] == attacker.fraction_name:
                print('Это ваша клетка') # Добавить сюда перемещение войск по своим клеткам (выбор кол-ва)
                return
            units_from = int(ground_from[5]) - 1 # оставляем одного человека в атакующей клетке (для теста)
            units_to = int(ground_to[5])
            delta_units_cnt = units_from - units_to

            # defending_ground_protection = int(self.rules['StructuresProtection'][ground_to[1]][0])
            if delta_units_cnt > 0:
                if ground_to[1] == ground_to[4] and ground_to[1] != 'null': #проверка уничтожения главной структуры
                    self.effects.append(Information(y, f"{ground_from[4]} уничтожили империю {ground_to[4]}", self.textures.resizer))
                    ground_to[1] = 'null'
                    self.destroy_empire(ground_to[4])
                    return
                if ground_to[4] == 'null':
                    self.effects.append(Information(y, f"{ground_from[4]} успешно захватили новую клетку", self.textures.resizer))
                else:
                    self.effects.append(Information(y, f"{ground_from[4]} успешно атакуют {ground_to[4]}", self.textures.resizer))
                ground_to[4] = ground_from[4]
                ground_from[5] = str(max(0, units_from - delta_units_cnt + 1))
                ground_to[5] = str(max(0, delta_units_cnt))
            else:
                if ground_to[4] == 'null':
                    self.effects.append(Information(y, f"{ground_from[4]} не смогли расширить владения", self.textures.resizer))
                else:
                    self.effects.append(Information(y, f"{ground_from[4]} не смогли захватить клетку {ground_to[4]}", self.textures.resizer))

    def destroy_empire(self, fraction):
        for i in range(len(self.screen_world.biomes)):
            for j in range(len(self.screen_world.biomes)):
                if self.screen_world.biomes[i][j][4] == fraction:
                    self.screen_world.biomes[i][j][4] = 'null'

                    sq_i, sq_j = i - self.screen_world.world_coord[0], j - self.screen_world.world_coord[1]
                    ground = self.screen_world.great_world[sq_i][sq_j]  # Объект Ground
                    xoy = (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2)
                    self.effects.append(Effect(xoy, self.textures.effects['place'], True)) #сделать эффект постройки, но в обратную сторону

    def area(self, ground, buyer):
        if "tower" in ground[1]:
            for i in range(-2, 3):
                for j in range(-2, 3):
                    x, y = int(ground[2]) + i, int(ground[3]) + j
                    if 'bot' in buyer.uid and self.screen_world.biomes[x][y] not in buyer.my_ground and buyer.fraction_name == self.screen_world.biomes[x][y][4]:
                        buyer.my_ground.append(self.screen_world.biomes[x][y])
                    self.set_fraction((x, y), buyer.fraction_name, True)

    def check_structure_placement(self, ground, structure, buyer):
        y = self.centre[1] * 2 - 60 * self.textures.resizer
        if ground[4] != buyer.fraction_name:
            if buyer == self.me:
                self.effects.append(Information(y, "Эта клетка не принадлежит Вам", self.textures.resizer))
            return False
        if ground[1] != 'null':
            if buyer == self.me:
                self.effects.append(Information(y, "Здесь стоит другая структура", self.textures.resizer))
            return False
        if ground[0] not in self.rules['StructuresPermissions'][structure]:
            if buyer == self.me:
                self.effects.append(Information(y, "Вы не можете строить в этом биоме", self.textures.resizer))
            return False
        struct_cost = int(self.rules['StructuresCosts'][self.structures[self.now_structure]][0])
        if buyer.resources < struct_cost:
            if buyer == self.me:
                self.effects.append(Information(y, "Не хватает ресурсов", self.textures.resizer))
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
        if f'{structure}_support' in self.supports_structure and\
           (structure in smez_structures or f'{structure}_support' in smez_structures):
            return f'{structure}_support'
        return structure

    def place_structure(self, coord_ground, structure=None, info=True, buyer=None):
        i, j = coord_ground[0], coord_ground[1]
        sq_i, sq_j = i - self.screen_world.world_coord[0], j - self.screen_world.world_coord[1]
        in_matrix = 0 <= sq_i < self.screen_world.sq2 and 0 <= sq_j < self.screen_world.sq1
        if not structure:
            structure = self.structures[self.now_structure]
        if buyer and not self.check_structure_placement(self.screen_world.biomes[i][j], structure, buyer):
            return
        structure = self.try_connect_structure((i, j), structure)
        self.screen_world.biomes[i][j][1] = structure
        if structure != 'null' and in_matrix:
            pygame.mixer.Channel(2).play(self.sounds.place)
            ground = self.screen_world.great_world[sq_i][sq_j]  # Объект Ground
            xoy = (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2)
            self.effects.append(Effect(xoy, self.textures.effects['place'], True))
            image = self.textures.animations_structures[structure][0][0]
            if structure in self.structures + self.supports_structure:
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
        sq_i, sq_j = i - self.screen_world.world_coord[0], j - self.screen_world.world_coord[1]
        in_matrix = 0 <= sq_i < self.screen_world.sq2 and 0 <= sq_j < self.screen_world.sq1
        if self.screen_world.biomes[i][j][4] != 'null':
            return
        self.screen_world.biomes[i][j][4] = fraction
        if in_matrix:
            ground = self.screen_world.great_world[sq_i][sq_j]  # Объект Ground
            xoy = (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2)
            self.effects.append(Effect(xoy, self.textures.effects['set'], True, 10))
        if buyer:
            ground_cost = int(self.rules['GroundsCosts'][self.screen_world.biomes[i][j][0]][0])
            if buyer.resources >= ground_cost:
                self.update_resource(buyer.uid, -ground_cost)  # Мы не можем заглянуть в me у другого игрока (ПРОБЛМЕА)
                buyer.resources -= ground_cost                 # А это решение этого (выше смотри строчку)
        if info:
            self.contact.send(f'change-0-fraction|{fraction}|{i}|{j}-end-')

    def update_resource(self, uid, delta_resource):
        if self.contact.protocol == 'host' or self.contact.protocol == 'unknown':
            ind = [i[0] for i in self.info_players].index(uid)
            self.info_players[ind][3] += delta_resource
        else:
            self.contact.send(f'resource-0-{uid}|{delta_resource}-end-')

    def update_presource(self, uid, delta_presource):
        if self.contact.protocol == 'host' or self.contact.protocol == 'unknown':
            ind = [i[0] for i in self.info_players].index(uid)
            self.info_players[ind][4] += delta_presource
        else:
            self.contact.send(f'presource-0-{uid}|{delta_presource}-end-')


    def get_resource(self):
        if (datetime.now() - self.timer).seconds >= COOLDOWN:
            self.timer = datetime.now()
            self.contact.send(f'host-0-timer-end-')
            self.update_resource(self.me.uid, self.me.potential_resource)
            self.me.resources += self.me.potential_resource
            show_resources(self, self.me.potential_resource)
            if self.contact.protocol == 'host' or self.contact.protocol == 'unknown':
                for bot in self.bots:
                    self.update_resource(bot.uid, bot.potential_resource)
                    bot.resources += bot.potential_resource

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
                self.contact.sock.close()
                sys.exit()
            if i.type == pygame.MOUSEWHEEL:
                self.next_struct(int(i.precise_y)) if 'buildmenu' in self.interfaces else None
        return c

    def update(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.clock.tick()
        rendering(self, self.screen_world)