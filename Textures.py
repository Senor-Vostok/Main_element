import pygame

pygame.init()
screen = pygame.display.set_mode()

priority = ['ground', 'barrier', 'stone']

select = pygame.image.load('data/ground/ground_select.png').convert_alpha()

animation_ground = {'ground': None, None: None}

land = {'ground': pygame.image.load('data/ground/ground.png').convert_alpha(),
        'stone': pygame.image.load('data/ground/stone.png').convert_alpha(),
        'barrier': pygame.image.load('data/ground/barrier.png').convert_alpha()}

animations_structures = {'lol': 'This LMAO XD image, HAHAHAHAHA'}