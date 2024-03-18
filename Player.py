import pygame
import Ground_class


class Player:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.is_bot = False

        self.fraction_type = 1 #random.randint(1, 4)
        self.units_count = 0
        self.action_pts = 0 #очки действий
        self.money = 0 #денюжки
        self.resources = 0
        self.structures_list = [] #структуры во владении

        self.debuffs = []
        self.start_point = (None, None) #точка спавна фракции

    def setup(self, start_ground: Ground_class.Ground):
        self.units_count = 100
        start_ground.fraction = self.fraction_type
        start_ground.units_count = self.units_count
        # start_ground.image = pygame.image.load('data/ground/barrier.png').convert_alpha()
