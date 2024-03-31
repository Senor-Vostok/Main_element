class Player:
    def __init__(self, id):
        self.id = id
        self.is_bot = False

        self.fraction_name = None
        self.units_count = 0
        self.action_pts = 0 #кол-во ходов
        self.resources = 0
        self.structures_list = [] #структуры во владении

        self.debuffs = []
        self.start_point = (None, None) #точка спавна фракции
