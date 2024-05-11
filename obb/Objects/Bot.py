import random
import threading
import time

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
        self.start_point = (None, None)  # точка спавна фракции

    def think_smth_please(self, handler):
        if self.can_i_do_smth:
            self.can_i_do_smth = False
            self.thread = threading.Timer(self.interval, self.cooldown)
            self.thread.start()
            self.outbuild_smth(handler)

    def cooldown(self):
        self.can_i_do_smth = True

    def destroy(self, handler):
        monkeys_enemy = list()
        war = [[], []]
        t = 0
        end_war = False
        for monkey in self.monkeys:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    monkeys_enemy = handler.screen_world.biomes[int(monkey[2]) + i][int(monkey[3]) + j]
                    if monkeys_enemy[4] != self.fraction_name and monkeys_enemy in self.fractions:
                        war = [monkey, monkeys_enemy]
                        handler.attack(self, war)
                        self.monkeys[t] = monkeys_enemy
                        end_war = True
                        break
            if end_war:
                break
            t += 1

    def go_to_attack(self, handler, coord):
        x, y = int(coord[0]), int(coord[1])
        ok = True
        a = str()
        for i in range(-3, 6):
            for j in range(-3, 6):
                if handler.screen_world.biomes[x + i][y + j][4] not in self.fractions:
                    handler.set_fraction((x + i, y + j), self.fraction_name, True, self)
                    a = random.choice(["tower", "homes"])
                    handler.place_structure((x + i, y + j), a, True, self)
                    ok = False
                    break
            if not ok:
                break

    def monkey_stregth(self, handler, monkey, ground):
        ans = [[], []]
        for i in range(7):
            if monkey == ground:
                break
            x, y = int(monkey[2]), int(monkey[3])
            z, w = int(ground[2]), int(ground[3])
            if z > x and w > y:
                ans = [monkey, handler.screen_world.biomes[x + 1][y + 1]]
                handler.attack(self, ans)
                monkey = handler.screen_world.biomes[x + 1][y + 1]
            if z < x and w > y:
                ans = [monkey, handler.screen_world.biomes[x - 1][y + 1]]
                handler.attack(self, ans)
                monkey = handler.screen_world.biomes[x - 1][y + 1]
            if z > x and w < y:
                ans = [monkey, handler.screen_world.biomes[x + 1][y - 1]]
                handler.attack(self, ans)
                monkey = handler.screen_world.biomes[x + 1][y - 1]
            if z < x and w < y:
                ans = [monkey, handler.screen_world.biomes[x - 1][y - 1]]
                handler.attack(self, ans)
                monkey = handler.screen_world.biomes[x - 1][y - 1]
            if x == z and w < y:
                ans = [monkey, handler.screen_world.biomes[x][y - 1]]
                handler.attack(self, ans)
                monkey = handler.screen_world.biomes[x][y - 1]
            if x == z and w > y:
                ans = [monkey, handler.screen_world.biomes[x][y + 1]]
                handler.attack(self, ans)
                monkey = handler.screen_world.biomes[x][y + 1]
            if z < x and y == w:
                ans = [monkey, handler.screen_world.biomes[x - 1][y]]
                handler.attack(self, ans)
                monkey = handler.screen_world.biomes[x - 1][y]
            if z > x and y == w:
                ans = [monkey, handler.screen_world.biomes[x + 1][y]]
                handler.attack(self, ans)
                monkey = handler.screen_world.biomes[x + 1][y]

    def find_monkey(self, handler, ground):
        for i in range(-5, 6):
            for j in range(-5, 6):
                monkey = handler.screen_world.biomes[int(ground[2]) + i][int(ground[3]) + j]
                if monkey[5] != '0' and monkey[4] == self.fraction_name:
                    self.monkey_stregth(handler, monkey, ground)
                    return

    def monkey_war(self, handler):
        go = [[], []]
        if self.my_coord == []:
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
            if z < x and w > y:
                go = [self.my_coord, handler.screen_world.biomes[x - 1][y + 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x - 1][y + 1]
            if z > x and w < y:
                go = [self.my_coord, handler.screen_world.biomes[x + 1][y - 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x + 1][y - 1]
            if z < x and w < y:
                go = [self.my_coord, handler.screen_world.biomes[x - 1][y - 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x - 1][y - 1]
            if z == x and w > y:
                go = [self.my_coord, handler.screen_world.biomes[x][y + 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x][y + 1]
            if z == x and w < y:
                go = [self.my_coord, handler.screen_world.biomes[x][y - 1]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x][y - 1]
            if z > x and w == y:
                go = [self.my_coord, handler.screen_world.biomes[x + 1][y]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x + 1][y]
            if z < x and w == y:
                go = [self.my_coord, handler.screen_world.biomes[x - 1][y]]
                handler.attack(self, go)
                self.my_coord = handler.screen_world.biomes[x - 1][y]

    def attack_fraction(self, handler):
        if not self.coord_to:
            return
        for ground in self.my_ground:
            if int(ground[5]) <= int(self.coord_to[5]):
                self.find_monkey(handler, ground)
            else:
                self.my_coord = ground
                self.monkey_war(handler)

    def goto_fraction(self, handler, attack=False, destroy=False):
        min = 1e7
        coord = list()
        coord.append(0)
        coord.append(0)
        cell = list()
        for i in range(0, 4):
            if self.fraction_name != self.fractions[i]:
                board = handler.found_board(4, self.fractions[i])
                for bord in board:
                    for place in self.my_ground:
                        if not destroy:
                            x_bord, y_bord = int(bord[2]), int(bord[3])
                            x_place, y_place = int(place[2]), int(place[3])
                            if min > abs(x_bord - x_place) + abs(y_bord - y_place):
                                min = abs(x_bord - x_place) + abs(y_bord - y_place)
                                coord[0] = x_bord
                                coord[1] = y_bord
                                cell = bord
                        elif destroy and bord[1] in self.fractions:
                            x_bord, y_bord = int(bord[2]), int(bord[3])
                            x_place, y_place = int(place[2]), int(place[3])
                            if min > abs(x_bord - x_place) + abs(y_bord - y_place):
                                min = abs(x_bord - x_place) + abs(y_bord - y_place)
                                coord[0] = x_bord
                                coord[1] = y_bord
                                cell = bord
        if not attack:
            self.go_to_attack(handler, coord)
        else:
            self.coord_to = cell
            self.attack_fraction(handler)

    def __get_event(self, y):
        if y < 4 or self.resources <= obb.Constants.RESORCE_CONST:  # строим фарм строения Todo 50 20 300 не константы
            return 1
        elif 7 < y < 9:  # строимся к врагам
            return 2
        elif 9 < y < 11:  # пупупу
            return 3
        elif 11 < y < 14 or y == 6:  # атакуем врагов
            return 4
        else:
            return 5

    def check_place_structure(self, handler, flag_money=False):  # пофиКСЬ ДВЕ ТАВЕРКИ
        try:
            while True:
                if flag_money:
                    field = random.choice(self.my_ground)
                    x, y = int(field[2]), int(field[3])
                    structure = random.choice(self.exist_structers)
                    if self.guides["ResourcesFromStructures"][structure][0] != '0':
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
        y = random.randint(1, 17)
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
                self.destroy(handler)  # сделать функцию где бот вдалеке около выгодного места(снег, вода) строит башню и добывающие здания
