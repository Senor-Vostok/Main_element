import pygame

pygame.init()
screen = pygame.display.set_mode()

priority = ['water', 'sand', 'flower', 'ground', 'stone', 'snow', 'barrier']

select = pygame.image.load('data/ground/ground_select.png').convert_alpha()

point = pygame.image.load('data/ground/test.png').convert_alpha()

animation_ground = {'water': [pygame.image.load(f'data/ground/water{i}.png').convert_alpha() for i in range(1, 4)]}

land = {'ground': [pygame.image.load(f'data/ground/ground{i}.png').convert_alpha() for i in range(1, 5)],
        'stone': [pygame.image.load('data/ground/stone.png').convert_alpha()],
        'barrier': [pygame.image.load('data/ground/barrier.png').convert_alpha()],
        'flower': [pygame.image.load('data/ground/flower.png').convert_alpha()],
        'water': [pygame.image.load(f'data/ground/water.png')],
        'sand': [pygame.image.load('data/ground/sand.png').convert_alpha()],
        'snow': [pygame.image.load('data/ground/snow.png').convert_alpha()]}

animations_structures = {'f': [pygame.image.load('data/ground/test.png').convert_alpha()]}