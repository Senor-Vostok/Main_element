class Bot():
    def __init__(self, id):
        self.id = id
        self.fraction_name = None
        self.units_count = 0
        self.action_pts = 0
        self.resources = 0
        self.structures_list = []
        self.debuffs = []
        self.start_point = (None, None) #точка спавна фракции

    def buy_smth(self, handler):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if handler.screen_world.biomes[self.start_point[0] + i][self.start_point[1] + j][4] != self.fraction_name:
                    handler.buy_ground((self.start_point[0] + i, self.start_point[1] + j), self.fraction_name, self)

    def build_smth(self, handler, structure_id):
        structures = list(handler.rules['StructuresList'])
        built_cnt = 0
        while built_cnt != 1:
            if self.check_structure_placement(handler.screen_world.biomes[self.start_point[0] + 1][self.start_point[1]], structures[structure_id], handler):
                handler.screen_world.biomes[self.start_point[0] + 1][self.start_point[1]][1] = structures[structure_id]
                built_cnt += 1
            else:
                structure_id += 1

        if info:
            contact.send(f'change-0-' + '|'.join(ground.biom))

    def check_structure_placement(self, ground, structure, handler):
        if ground[0] not in handler.rules['StructuresPermissions'][structure]:
            print('bot nelza tut stroit', structure, ', potomuchto tut ', ground[0])
            return False
        struct_cost = int(handler.rules['StructuresCosts'][structure][0])
        struct_action_pts = int(handler.rules['StructuresActionPoints'][structure][0])
        if self.action_pts < struct_action_pts:
            print("bot no points((9(")
            return False
        if self.resources < struct_cost:
            print('bot malo denyak, vzuh, and ti bezdomni (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
            return False
        self.update_placement_state(ground, structure, struct_cost, struct_action_pts)
        return True

    def update_placement_state(self, ground, structure, struct_cost, struct_action_pts):
        ground[1] = structure
        self.action_pts -= struct_action_pts
        self.resources -= struct_cost

