import random
import threading

class Bot:
    def __init__(self, id, structures, guides):
        self.id = id
        self.guides = guides
        self.uid = f'bot{id}'
        self.interval = 1
        self.fraction_name = None
        self.resources = 0
        self.fractions = ["water", "fire", "earth", "wind"]
        self.exist_structers = structures
        self.potential_resource = 0
        self.my_ground = list()
        self.can_i_do_smth = True
        self.thread = None
        self.people = 0
        self.start_point = (None, None)  # точка спавна фракции

    def think_smth_please(self, handler):
        if self.can_i_do_smth:
            self.can_i_do_smth = False
            self.thread = threading.Timer(self.interval, self.cooldown)
            self.thread.start()
            dodo = random.choice([self.outbuild_smth, self.buy_smth])
            dodo(handler)

    def cooldown(self):
        self.can_i_do_smth = True

    def buy_smth(self, handler):
        pass

    def attack_fraction(self):
        pass

    def go_to_attack(self, handler, coord):
        x, y = coord[0], coord[1]
        ok = True
        for i in range(-3, 6):
            for j in range(-3, 6):
                if handler.screen_world.biomes[x + i][y + j][4] not in self.fractions:
                    handler.set_fraction((x + i, y + j), self.fraction_name, True, self)
                    handler.place_structure((x + i, y + j), "tower", True, self)
                    ok = False
                    break
            if not ok:
                break

    def goto_fraction(self, handler):
        min = 1e7
        coord = list()
        coord.append(0)
        coord.append(0)
        for i in range(0, 3):
            if self.fraction_name != self.fractions[i]:
                board = handler.found_board(4, self.fractions[i])
                for bord in board:
                    for place in self.my_ground:
                        x_bord, y_bord = int(bord[2]), int(bord[3])
                        x_place, y_place = int(place[2]), int(place[3])
                        if min > abs(x_bord - x_place) + abs(y_bord - y_place):
                            min = abs(x_bord - x_place) + abs(y_bord - y_place)
                            coord[0] = x_bord
                            coord[1] = y_bord
        self.go_to_attack(handler, coord)

    def __get_event(self, y):
        if y < 5 or self.resources <= (int(self.guides["StructuresCosts"]['tower'][0]) * 2) : # строим фарм строения Todo 50 20 300 не константы
            return 1
        elif 5 < y < 8 and self.resources >= 200:  # строимся к врагам
            return 2
        elif 8 < y < 12:  # пупупу
            return 3
        elif 12 < y < 14 or self.people >= 300:  # атакуем врагов
            return 4
        else:
            return 5  # строим провинцию

    def check_place_structure(self, handler, flag_money=False): # пофиКСЬ ДВЕ ТАВЕРКИ
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
        y = random.randint(1, 15)
        key = self.__get_event(int(y))
        if key == 1:
            self.check_place_structure(handler, True)
        elif key == 2:
            self.goto_fraction(handler)
        elif key == 3:
            self.check_place_structure(handler)
        elif key == 4:
            self.attack_fraction()
        elif key == 5:
            pass  # сделать функцию где бот вдалеке около выгодного места(снег, вода) строит башню и добывающие здания
