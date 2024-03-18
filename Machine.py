import pygame
import random
from Ground_class import Ground
from Textures import Textures


class World:
    def __init__(self, win, centre, cord, bioms):
        self.textures = Textures()
        self.land = self.textures.land

        self.my_font = pygame.font.SysFont('Futura book C', 30)

        self.priority = self.textures.priority  # Приоритеты текстур

        self.bioms = bioms  # Получение данных о матрице мира
        self.gr_main = 60
        self.sq1 = centre[0] * 2 // self.gr_main + 3 if centre[0] * 2 // self.gr_main % 2 == 0 else centre[0] * 2 // self.gr_main + 2  # Разбиение экрана на секторы, с помощью которых строится динамическая сетка
        self.sq2 = centre[1] * 2 // self.gr_main + 5 if centre[1] * 2 // self.gr_main % 2 == 0 else centre[1] * 2 // self.gr_main + 4

        self.win = win

        self.centre = centre
        self.global_centre = [centre[0], centre[1]]

        self.start_dr = [self.centre[0] - self.gr_main // 2 - (self.sq1 // 2) * self.gr_main,
                         self.centre[1] - self.gr_main // 2 - (self.sq2 // 2) * self.gr_main]  # Стартовая установка динамической сетки
        self.now_dr = [self.centre[0] - self.gr_main // 2 - (self.sq1 // 2) * self.gr_main,
                       self.centre[1] - self.gr_main // 2 - (self.sq2 // 2) * self.gr_main]  # Пермещение динамической сетки

        self.great_world = [[None for _ in range(self.sq1)] for _ in range(self.sq2)]  # Создание массива динамической сетки

        self.world_cord = cord  # позиция курсора

        self.synchronous = 0  # Синхронизация анимации связных объектов

    def create(self, stor='static'):  # Перестройка динамической сетки
        if stor == 'up':  # Удаление нижней части сетки и вставка новой вверх
            self.great_world.pop(-1)
            self.great_world.insert(0, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                self.add_ground(0, i, self.bioms[self.world_cord[0]][self.world_cord[1] + i])
        elif stor == 'down':  # По принципу Up
            self.great_world.pop(0)
            self.great_world.insert(self.sq1, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                self.add_ground(self.sq2 - 1, i, self.bioms[self.world_cord[0] + self.sq2 - 1][self.world_cord[1] + i])
        elif stor == 'left':
            for i in range(self.sq2):
                self.great_world[i].pop(-1)
                self.great_world[i].insert(0, None)
            for i in range(self.sq2):
                self.add_ground(i, 0, self.bioms[self.world_cord[0] + i][self.world_cord[1]])
        elif stor == 'right':
            for i in range(self.sq2):
                self.great_world[i].pop(0)
                self.great_world[i].insert(self.sq1 - 1, None)
            for i in range(self.sq2):
                self.add_ground(i, self.sq1 - 1, self.bioms[self.world_cord[0] + i][self.world_cord[1] + self.sq1 - 1])
        else:  # Заполнение динамической сетки если до этого её не было
            for i in range(self.sq2):
                for j in range(self.sq1):
                    self.add_ground(i, j, self.bioms[self.world_cord[0] + i][self.world_cord[1] + j])

    def draw(self, there, move=(0, 0), open_some=False):  # Отображение на экране спрайтов
        flag = self.check_barrier(move, self.centre)
        self.update_object(move, flag, open_some)  # Обновление оставшихся спрайтов и динамической сетки
        sorted_by_priority = list()
        for i in range(len(self.great_world)):
            for j in range(len(self.great_world[i])):
                self.great_world[i][j].update(self.synchronous, move, flag and not open_some)  # Обновление спрайтов земли
                sorted_by_priority.append(self.great_world[i][j])
        for i in sorted(sorted_by_priority, key=lambda x: x.structure != None):  # потом заменить на "если есть в клетке"
            i.draw(self.win, there)  # Показ слайдов земли по приоритетам
        self.synchronous = self.synchronous + 1 if self.synchronous < 1000000 else 0  # Задел на будущее если будет анимированная земля

    def move_scene(self):  # Тут происходит проверка, когда нужно обновлять динамическую сетку
        if max(self.now_dr[0], self.start_dr[0]) - min(self.now_dr[0], self.start_dr[0]) > self.gr_main:
            res = self.now_dr[0] >= self.start_dr[0]
            self.now_dr[0] = self.now_dr[0] - self.gr_main if res else self.now_dr[0] + self.gr_main
            if res:
                self.world_cord[1] = self.world_cord[1] - 1 if self.world_cord[1] >= 1 else None
                self.create('left')
            else:
                self.world_cord[1] += 1
                self.create('right')
        elif max(self.now_dr[1], self.start_dr[1]) - min(self.now_dr[1], self.start_dr[1]) > self.gr_main:
            res = self.now_dr[1] >= self.start_dr[1]
            self.now_dr[1] = self.now_dr[1] - self.gr_main if res else self.now_dr[1] + self.gr_main
            if res:
                self.world_cord[0] = self.world_cord[0] - 1 if self.world_cord[0] >= 1 else None
                self.create('up')
            else:
                self.world_cord[0] += 1
                self.create('down')

    def check_barrier(self, move, point):  # проверка на препятствия (Работает не только с курсором, но и по координатам)
        for i in range(self.sq2 // 2 - 1, self.sq2 // 2 + 2):
            for j in range(self.sq1 // 2 - 1, self.sq1 // 2 + 2):
                res = self.now_dr[0] + j * self.gr_main <= point[0] - 2 * move[0] <= self.now_dr[0] + j * self.gr_main + self.gr_main and \
                      self.now_dr[1] + i * self.gr_main <= point[1] - 2 * move[1] <= self.now_dr[1] + i * self.gr_main + self.gr_main
                if res:
                    if self.bioms[self.world_cord[0] + i][self.world_cord[1] + j][0] == 'barrier':
                        return False
        return True

    def update_object(self, move, flag, open_some):
        if flag and not open_some:
            self.now_dr[0] = self.great_world[0][0].rect[0] + self.great_world[0][0].rect[2] / 2 - self.gr_main / 2
            self.now_dr[1] = self.great_world[0][0].rect[1] + self.great_world[0][0].rect[3] / 2 - self.gr_main / 2
            self.move_scene()

    def add_ground(self, i, j, biom):  # Вспомогательная функция для добавления спрайта земля на сетку
        sprite = Ground(random.choice(self.land[biom[0]]), (self.now_dr[0] + j * self.gr_main + self.gr_main / 2, self.now_dr[1] + i * self.gr_main + self.gr_main / 2), biom, self.textures)
        self.great_world[i][j] = sprite
