import random
import threading

import obb.Constants


class Bot:
    def __init__(self, id, structures, guides):
        self.id = id
        self.guides = guides
        self.uid = f'bot{id}'
        self.interval = 1
        self.fraction_name = None
        self.resources = 0
        self.fractions = ["water", "fire", "earth", "air"]
        self.exist_structers = structures
        self.potential_resource = 0
        self.my_ground = list()
        self.can_i_do_smth = True
        self.thread = None
        self.thread_attack = None
        self.can_i_monkey_attack = False
        self.monkeys = list()
        self.my_coord = []
        self.coord_to = []
        self.my_monkey_coord = []
        self.my_monkey_ground = []
        self.start_point = (None, None)  # точка спавна фракции

    def think_smth_please(self, handler):
        if self.can_i_do_smth:
            self.can_i_do_smth = False
            self.thread = threading.Timer(self.interval, self.cooldown)
            self.thread.start()
            self.outbuild_smth(handler)

    def cooldown(self):
        self.can_i_do_smth = True

    def go_to_attack(self, handler, coord):
        x, y = int(coord[0]), int(coord[1])
        ok = True
        for i in range(-obb.Constants.ATTACK_RANGE_BOT, obb.Constants.ATTACK_RANGE_BOT + 1):
            for j in range(-obb.Constants.ATTACK_RANGE_BOT, obb.Constants.ATTACK_RANGE_BOT + 1):
                if handler.screen_world.biomes[x + i][y + j][4] not in self.fractions:
                    handler.set_fraction((x + i, y + j), self.fraction_name, True, self)
                    a = random.choice(["tower1", "polygon1", "homes1"])
                    handler.place_structure((x + i, y + j), a, True, self)
                    ok = False
                    break
            if not ok:
                break

    def monkey_unite(self, handler):
        self.coord_to = self.my_coord
        coord = self.find_monkey(handler, self.my_coord)
        if coord == self.my_coord:
            self.can_i_monkey_attack = False
        else:
            self.my_coord = coord
            self.monkey_war(handler)

    def find_monkey(self, handler, ground):
        x, y = int(ground[2]), int(ground[3])
        minimum = obb.Constants.MAX
        maximum = obb.Constants.MIN
        monkey = list()
        for monkey_find in self.my_ground:
            a, b = int(monkey_find[2]), int(monkey_find[3])
            if abs(x - a) + abs(y - b) < minimum and int(monkey_find[5]) > maximum:
                maximum = int(monkey_find[5])
                minimum = abs(x - a) + abs(y - b)
                monkey = monkey_find
        if monkey == list():
            return ground
        else:
            return monkey

    def monkey_war(self, handler):
        if not self.my_coord:
            return
        if self.my_coord == self.coord_to:
            self.can_i_monkey_attack = False
            return
        if self.my_coord != self.coord_to:
            x, y = int(self.my_coord[2]), int(self.my_coord[3])
            z, w = int(self.coord_to[2]), int(self.coord_to[3])
            if z > x and w > y:
                go = [self.my_coord, handler.screen_world.biomes[x + 1][y + 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x + 1][y + 1]
                return
            elif z < x and w > y:
                go = [self.my_coord, handler.screen_world.biomes[x - 1][y + 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x - 1][y + 1]
                return
            elif z > x and w < y:
                go = [self.my_coord, handler.screen_world.biomes[x + 1][y - 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x + 1][y - 1]
                return
            elif z < x and w < y:
                go = [self.my_coord, handler.screen_world.biomes[x - 1][y - 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x - 1][y - 1]
                return
            elif z == x and w > y:
                go = [self.my_coord, handler.screen_world.biomes[x][y + 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x][y + 1]
                return
            elif z == x and w < y:
                go = [self.my_coord, handler.screen_world.biomes[x][y - 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x][y - 1]
                return
            elif z > x and w == y:
                go = [self.my_coord, handler.screen_world.biomes[x + 1][y]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x + 1][y]
                return
            elif z < x and w == y:
                go = [self.my_coord, handler.screen_world.biomes[x - 1][y]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x - 1][y]
                return

    def attack_fraction(self, handler):
        if not self.coord_to:
            return
        for i in range(obb.Constants.SEARCH_CELL):
            ground = random.choice(self.my_ground)
            if int(ground[5]) <= int(self.coord_to[5]) and self.can_i_monkey_attack:
                self.monkey_unite(handler)
                break
            else:
                self.my_coord = ground
                self.monkey_war(handler)
                break

    def goto_fraction(self, handler, attack=False, destroy=False):
        minimum = obb.Constants.MAX
        coord = list()
        coord.append(0)
        coord.append(0)
        cell = list()
        my_place = []
        for i in range(len(handler.fractions)):
            if self.fraction_name != self.fractions[i]:
                board = handler.found_board(4, self.fractions[i])
                for bord in board:
                    for place in self.my_ground:
                        x_bord, y_bord = int(bord[2]), int(bord[3])
                        x_place, y_place = int(place[2]), int(place[3])
                        if minimum > abs(x_bord - x_place) + abs(y_bord - y_place):
                            minimum = abs(x_bord - x_place) + abs(y_bord - y_place)
                            coord[0] = x_bord
                            coord[1] = y_bord
                            cell = bord
                            my_place = place
        if destroy:
            return my_place, cell
        if not attack:
            self.go_to_attack(handler, coord)
        else:
            self.coord_to = cell
            self.attack_fraction(handler)
        return cell

    def monkey_scouts(self, handler):
        monkey_map = self.goto_fraction(handler, False, True)
        self.my_coord = monkey_map[0]
        self.coord_to = monkey_map[1]
        self.monkey_war(handler)

    def __get_event(self, y):
        if y < 5 or self.resources <= obb.Constants.RESORCE_CONST:  # строим фарм строения
            return 1
        elif 5 < y < 8:  # Дарим врагу свои строения
            return 2
        elif 8 < y < 10:  # Строим любое здание
            return 3
        elif 10 < y < 14:  # Атакуем ближайшего врага
            return 4
        elif 14 < y < 17:  # Пытаемся захватить ближайшую клетку врага к войску
            return 5
        else:  # Обновляем наши данные карты
            return 6

    def check_place_structure(self, handler, flag_money=False):
        try:
            while True:
                if flag_money:
                    field = random.choice(self.my_ground)
                    x, y = int(field[2]), int(field[3])
                    structure = random.choice(self.exist_structers)
                    if self.guides["ResourcesFromStructures"][structure[:-1]][0] != '0':
                        handler.place_structure((x, y), structure, True, self)
                        break
                else:
                    field = random.choice(self.my_ground)
                    x, y = int(field[2]), int(field[3])
                    structure = random.choice(self.exist_structers)
                    handler.place_structure((x, y), structure, True, self)
                    break
        except Exception:
            pass

    def outbuild_smth(self, handler):
        y = random.randint(1, 20)
        key = self.__get_event(int(y))
        if self.can_i_monkey_attack:
            self.monkey_war(handler)
        else:
            if key == 1:
                self.check_place_structure(handler, True)
            elif key == 2:
                self.goto_fraction(handler)
            elif key == 3:
                self.check_place_structure(handler)
            elif key == 4:
                self.goto_fraction(handler, True)
                self.can_i_monkey_attack = True
            elif key == 5:
                self.monkey_scouts(handler)
            elif key == 6:
                self.my_coord = handler.found_board(4, self.fraction_name)