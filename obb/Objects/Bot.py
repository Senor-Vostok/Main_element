import random
import threading


class Bot:
    def __init__(self, id):
        self.id = id
        self.uid = "0" * (9 - len(str(id))) + str(id)
        self.interval = id + 1
        self.fraction_name = None
        self.resources = 0
        self.exist_structers = ["tower", "mill", "mine", "homes"]
        self.potential_resource = 0
        self.my_ground = list()
        self.can_i_do_smth = True
        self.thread = None
        self.start_point = (None, None)  # точка спавна фракции

    def think_smth_please(self, handler):
        if self.can_i_do_smth:
            self.can_i_do_smth = False
            self.thread = threading.Timer(self.interval, self.cooldown)
            self.thread.start()
            dodo = random.choice([self.build_smth, self.buy_smth])
            dodo(handler)

    def cooldown(self):
        self.can_i_do_smth = True

    def buy_smth(self, handler):
        pass

    def build_smth(self, handler):
        field = random.choice(self.my_ground)
        i, j = int(field[2]), int(field[3])
        structure = random.choice(self.exist_structers)
        handler.place_structure((i, j), structure, True, self)