import pygame
from win32api import GetSystemMetrics

pygame.init()
screen = pygame.display.set_mode()


class Textures:
    def __init__(self):
        self.resizer = GetSystemMetrics(0) / 1920
        self.priority = ['water', 'sand', 'flower', 'ground', 'stone', 'snow', 'barrier']

        self.font = pygame.font.SysFont('progresspixel-bold', 30)

        self.loading = self.render('data/loading/logo.png', (1920, 1080))
        self.connecting = self.render('data/loading/connecting.png', (1920, 1080))

        self.label = self.render('data/ground/label.png', (400, 30))

        self.select = self.render('data/ground/ground_select.png', (60, 60))

        self.point = self.render('data/ground/test.png', (20, 20))

        self.animation_ground = {'water': [self.render(f'data/ground/water{i}.png', (60, 60)) for i in range(1, 4)]}

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

        self.popup_menu = {'button_information': [self.render('data/widgets/popupmenu/buttons/button1.png', (250, 50)),
                                                  self.render('data/widgets/popupmenu/buttons/button1t.png', (250, 50))],
                           'button_build': [self.render('data/widgets/popupmenu/buttons/button2.png', (250, 50)),
                                            self.render('data/widgets/popupmenu/buttons/button2t.png', (250, 50))],
                           'button_destroy': [self.render('data/widgets/popupmenu/buttons/button3.png', (250, 50)),
                                              self.render('data/widgets/popupmenu/buttons/button3t.png', (250, 50))],
                           'button_fight': [self.render('data/widgets/popupmenu/buttons/button4.png', (250, 50)),
                                            self.render('data/widgets/popupmenu/buttons/button4t.png', (250, 50))],
                           'button_cancel': [self.render('data/widgets/popupmenu/buttons/button5.png', (250, 50)),
                                             self.render('data/widgets/popupmenu/buttons/button5t.png', (250, 50))]}

        self.main_menu = {'background': [self.render(f'data/widgets/menu/background.png', (1920, 1080))],
                          'name': [self.render(f'data/widgets/menu/main element.png', (466, 194))],
                          'button_start': [self.render(f'data/widgets/menu/buttons/button.png', (500, 90)),
                                           self.render(f'data/widgets/menu/buttons/buttont.png', (500, 90))],
                          'button_loading': [self.render(f'data/widgets/menu/buttons/button2.png', (400, 70)),
                                             self.render(f'data/widgets/menu/buttons/button2t.png', (400, 70))],
                          'button_online': [self.render(f'data/widgets/menu/buttons/button3.png', (400, 70)),
                                            self.render(f'data/widgets/menu/buttons/button3t.png', (400, 70))],
                          'button_setting': [self.render(f'data/widgets/menu/buttons/button4.png', (400, 70)),
                                             self.render(f'data/widgets/menu/buttons/button4t.png', (400, 70))],
                          'button_exit': [self.render(f'data/widgets/menu/buttons/button5.png', (400, 70)),
                                          self.render(f'data/widgets/menu/buttons/button5t.png', (400, 70))],
                          'button_local': [self.render(f'data/widgets/menu/buttons/button8.png', (400, 70)),
                                           self.render(f'data/widgets/menu/buttons/button8t.png', (400, 70))],
                          'label_online': [self.render(f'data/widgets/menu/labels/ipv4_port.png', (1100, 66))],
                          'label_count_users': [self.render(f'data/widgets/menu/labels/count_player.png', (550, 66))],
                          'label_port': [self.render(f'data/widgets/menu/labels/port.png', (550, 66))]}
        self.pause = {'background': [self.render(f'data/widgets/menu/labels/background.png', (1920, 1080))],
                      'button_menu': [self.render(f'data/widgets/menu/buttons/button6.png', (400, 70)),
                                      self.render(f'data/widgets/menu/buttons/button6t.png', (400, 70))],
                      'button_setting': self.main_menu['button_setting']}

        self.ingame = {'button_end': [self.render(f'data/widgets/menu/buttons/button7.png', (400, 50)),
                                      self.render(f'data/widgets/menu/buttons/button7t.png', (400, 50))]}

        self.buildmenu = {'background': [self.render(f'data/widgets/buildmenu/labels/background.png', (500, 1000))],
                          'button_project': [self.render(f'data/widgets/buildmenu/buttons/button1.png', (400, 50)),
                                             self.render(f'data/widgets/buildmenu/buttons/button1t.png', (400, 50))],
                          'up': [self.render(f'data/widgets/buildmenu/buttons/up1.png', (304, 128)),
                                 self.render(f'data/widgets/buildmenu/buttons/up2.png', (304, 128))],
                          'down': [self.render(f'data/widgets/buildmenu/buttons/down1.png', (304, 128)),
                                   self.render(f'data/widgets/buildmenu/buttons/down2.png', (304, 128))]}

    def render(self, address, size):
        size = size[0] * self.resizer, size[1] * self.resizer
        return pygame.transform.scale(pygame.image.load(address), size).convert_alpha()
