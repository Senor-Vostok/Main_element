import random
from Constants import UPDATE_LIMIT, TILE_SIZE, OFFSET_X, OFFSET_Y
from Ground_class import Ground
from Textures import Textures


class World:
    def __init__(self, screen, center, coord, biomes, handler):
        self.handler = handler
        self.textures = Textures()
        self.land = self.textures.land
        self.biomes = biomes  # Получение данных о матрице мира
        self.gr_main = int(TILE_SIZE * self.textures.resizer)
        self.sq1 = center[0] * 2 // self.gr_main + OFFSET_X[0] if center[0] * 2 // self.gr_main % 2 == 0 else center[0] * 2 // self.gr_main + OFFSET_X[1]  # Разбиение экрана на секторы, с помощью которых строится динамическая сетка
        self.sq2 = center[1] * 2 // self.gr_main + OFFSET_Y[0] if center[1] * 2 // self.gr_main % 2 == 0 else center[1] * 2 // self.gr_main + OFFSET_Y[1]
        self.screen = screen
        self.center = center
        self.global_centre = [center[0], center[1]]
        self.start_dr = [self.center[0] - self.gr_main // 2 - (self.sq1 // 2) * self.gr_main,
                         self.center[1] - self.gr_main // 2 - (self.sq2 // 2) * self.gr_main]  # Стартовая установка динамической сетки
        self.now_dr = [self.center[0] - self.gr_main // 2 - (self.sq1 // 2) * self.gr_main,
                       self.center[1] - self.gr_main // 2 - (self.sq2 // 2) * self.gr_main]  # Пермещение динамической сетки
        self.great_world = [[None for _ in range(self.sq1)] for _ in range(self.sq2)]  # Создание массива динамической сетки
        self.world_coord = coord  # позиция курсора
        self.synchronous = 0  # Синхронизация анимации связных объектов

    def create(self, side='static'):  # Перестройка динамической сетки
        if side == 'up':  # Удаление нижней части сетки и вставка новой вверх
            self.great_world.pop(-1)
            self.great_world.insert(0, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                self.add_ground(0, i, self.biomes[self.world_coord[0]][self.world_coord[1] + i])
        elif side == 'down':  # По принципу Up
            self.great_world.pop(0)
            self.great_world.insert(self.sq1, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                self.add_ground(self.sq2 - 1, i, self.biomes[self.world_coord[0] + self.sq2 - 1][self.world_coord[1] + i])
        elif side == 'left':
            for i in range(self.sq2):
                self.great_world[i].pop(-1)
                self.great_world[i].insert(0, None)
            for i in range(self.sq2):
                self.add_ground(i, 0, self.biomes[self.world_coord[0] + i][self.world_coord[1]])
        elif side == 'right':
            for i in range(self.sq2):
                self.great_world[i].pop(0)
                self.great_world[i].insert(self.sq1 - 1, None)
            for i in range(self.sq2):
                self.add_ground(i, self.sq1 - 1, self.biomes[self.world_coord[0] + i][self.world_coord[1] + self.sq1 - 1])
        else:  # Заполнение динамической сетки если до этого её не было
            for i in range(self.sq2):
                for j in range(self.sq1):
                    self.add_ground(i, j, self.biomes[self.world_coord[0] + i][self.world_coord[1] + j])

    def draw(self, mouse_click, move=(0, 0), open_some=False):  # Отображение на экране спрайтов
        flag = self.check_barrier(move, self.center)
        self.update_object(move, flag, open_some)  # Обновление оставшихся спрайтов и динамической сетки
        sorted_by_priority = list()
        for i in range(len(self.great_world)):
            for j in range(len(self.great_world[i])):
                self.great_world[i][j].update(self.synchronous, move, flag and not open_some)  # Обновление спрайтов земли
                sorted_by_priority.append(self.great_world[i][j])
        for ground in sorted(sorted_by_priority, key=lambda x: x.structure != None):  # потом заменить на "если есть в клетке"
            ground.draw(self.screen, mouse_click, self.handler)  # Показ слайдов земли по приоритетам
        self.synchronous = self.synchronous + 1 if self.synchronous < UPDATE_LIMIT else 0

    def move_scene(self):  # Тут происходит проверка, когда нужно обновлять динамическую сетку
        if max(self.now_dr[0], self.start_dr[0]) - min(self.now_dr[0], self.start_dr[0]) > self.gr_main:
            res = self.now_dr[0] >= self.start_dr[0]
            self.now_dr[0] = self.now_dr[0] - self.gr_main if res else self.now_dr[0] + self.gr_main
            if res:
                self.world_coord[1] = self.world_coord[1] - 1 if self.world_coord[1] >= 1 else None
                self.create('left')
            else:
                self.world_coord[1] += 1
                self.create('right')
        elif max(self.now_dr[1], self.start_dr[1]) - min(self.now_dr[1], self.start_dr[1]) > self.gr_main:
            res = self.now_dr[1] >= self.start_dr[1]
            self.now_dr[1] = self.now_dr[1] - self.gr_main if res else self.now_dr[1] + self.gr_main
            if res:
                self.world_coord[0] = self.world_coord[0] - 1 if self.world_coord[0] >= 1 else None
                self.create('up')
            else:
                self.world_coord[0] += 1
                self.create('down')

    def check_barrier(self, move, point):  # проверка на препятствия (Работает не только с курсором, но и по координатам)
        for i in range(self.sq2 // 2 - 1, self.sq2 // 2 + 2):
            for j in range(self.sq1 // 2 - 1, self.sq1 // 2 + 2):
                res = self.now_dr[0] + j * self.gr_main <= point[0] - 2 * move[0] <= self.now_dr[0] + j * self.gr_main + self.gr_main and \
                      self.now_dr[1] + i * self.gr_main <= point[1] - 2 * move[1] <= self.now_dr[1] + i * self.gr_main + self.gr_main
                if res:
                    if self.biomes[self.world_coord[0] + i][self.world_coord[1] + j][0] == 'barrier':
                        move[0], move[1] = -move[0], -move[1]
                        return False
        return True

    def update_object(self, move, flag, open_some):
        if flag and not open_some:
            self.now_dr[0] = self.great_world[0][0].rect[0] + self.great_world[0][0].rect[2] / 2 - self.gr_main / 2
            self.now_dr[1] = self.great_world[0][0].rect[1] + self.great_world[0][0].rect[3] / 2 - self.gr_main / 2
            self.move_scene()

    def add_ground(self, i, j, biome):  # Вспомогательная функция для добавления спрайта земля на сетку
        sprite = Ground(random.choice(self.land[biome[0]]), (self.now_dr[0] + j * self.gr_main + self.gr_main / 2, self.now_dr[1] + i * self.gr_main + self.gr_main / 2), biome, self.textures)
        self.great_world[i][j] = sprite
