import random
import time
import threading


class Bot:
    def __init__(self, id):
        self.id = id
        self.uid = "0" * (9 - len(str(id))) + str(id)
        self.fraction_name = None
        self.resources = 0
        self.exist_structers = []
        self.structures_list = dict()
        self.my_ground = list()
        self.can_i_do_smth = True
        self.thread = None
        self.start_point = (None, None)  # точка спавна фракции

    def think_smth_please(self, handler):
        if self.can_i_do_smth:
            self.thread = threading.Thread(target=self.cooldown)
            self.thread.start()
            dodo = random.choice([self.build_smth, self.buy_smth])
            dodo(handler)

    def cooldown(self):
        self.can_i_do_smth = False
        time.sleep(random.randint(2, 18))
        self.can_i_do_smth = True

    def buy_smth(self, handler):
        pass

    def build_smth(self, handler):
        field = random.choice(self.my_ground)
        i, j = int(field[2]), int(field[3])
        structure = random.choice(handler.exist_structers)
        handler.screen_world.biomes[i][j][1] = structure
        i, j = i - handler.screen_world.world_coord[0], j - handler.screen_world.world_coord[1]
        if handler.screen_world.sq2 > i >= 0 and handler.screen_world.sq1 > j >= 0:
            handler.place_structure(handler.screen_world.great_world[i][j], structure, handler.screen_world.biomes[1], True, False)