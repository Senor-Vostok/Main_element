import pygame

pygame.init()
screen = pygame.display.set_mode()


class Textures:
    def __init__(self):
        self.priority = ['water', 'sand', 'flower', 'ground', 'stone', 'snow', 'barrier']

        self.font = pygame.font.SysFont('Futura book C', 30)

        self.loading = pygame.image.load('data/loading/logo.png').convert_alpha()

        self.label = self.render('data/ground/label.png', (400, 30))

        self.select = self.render('data/ground/ground_select.png', (60, 60))

        self.point = self.render('data/ground/test.png', (20, 20))

        self.animation_ground = {
            'water': [self.render(f'data/ground/water{i}.png', (60, 60)) for i in range(1, 4)]}

        self.land = {'ground': [self.render(f'data/ground/ground{i}.png', (60, 60)) for i in range(1, 5)],
                     'stone': [self.render('data/ground/stone.png', (60, 60))],
                     'barrier': [self.render('data/ground/barrier.png', (60, 60))],
                     'flower': [self.render('data/ground/flower.png', (60, 60))],
                     'water': [self.render(f'data/ground/water1.png', (60, 60))],
                     'sand': [self.render('data/ground/sand.png', (60, 60))],
                     'snow': [self.render('data/ground/snow.png', (60, 60))]}

        self.animations_structures = {
            'tower': [self.render(f'data/structures/tower/anim{i}.png', (120, 180)) for i in range(1, 6)],
            'mill': [self.render(f'data/structures/mill/anim{i}.png', (120, 180)) for i in range(1, 4)],
            'mine': [self.render(f'data/structures/mine/anim{i}.png', (120, 180)) for i in range(1, 8)]}

        self.popup_menu = {'label': self.render(f'data/widgets/surfaces/surface1.png', (120, 180))}

    def render(self, address, size):
        return pygame.transform.scale(pygame.image.load(address), size).convert_alpha()
