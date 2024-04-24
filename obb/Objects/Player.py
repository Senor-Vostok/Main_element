class Player:
    def __init__(self, id):
        self.id = id
        self.nickname = 'ABOBA'
        self.uid = "0" * (9 - len(str(id))) + str(id)
        self.fraction_name = None
        self.resources = 0
        self.potential_resource = 0
        self.start_point = (None, None)  # точка спавна фракции
