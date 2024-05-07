import pygame
from win32api import GetSystemMetrics


pygame.init()
screen = pygame.display.set_mode()


class Textures:
    def __init__(self):
        self.loaded_textures = dict()
        self.resizer = GetSystemMetrics(0) / 1920
        self.priority = ['water', 'sand', 'flower', 'ground', 'stone', 'snow', 'barrier']

        self.font = pygame.font.Font('19363.ttf', int(20 * self.resizer))

        self.loading = self.render('data/loading/logo.png', (1920, 1080))
        self.connecting = self.render('data/loading/connecting.png', (1920, 1080))

        self.select = self.render('data/ground/ground_select.png', (60, 60))

        self.point = self.render('data/ground/test.png', (20, 20))

        self.effects = {'mouse1': [self.render(f'data/effects/mouse1/anim{i}.png', (60, 60)) for i in range(1, 6)],
                        'place': [self.render(f'data/effects/place/smog{i}.png', (120, 180)) for i in range(1, 5)],
                        'set': [self.render(f'data/effects/set/anim{i}.png', (60, 60)) for i in range(1, 4)],
                        'information': [self.render('data/effects/information/back_information.png', (90, 90))]}

        self.animation_ground = {'water': [self.render(f'data/ground/water{i}.png', (60, 60)) for i in range(1, 4)]}

        self.land = {'ground': [self.render(f'data/ground/ground{i}.png', (60, 60)) for i in range(1, 5)],
                     'stone': [self.render('data/ground/stone.png', (60, 60))],
                     'barrier': [self.render('data/ground/barrier.png', (60, 60))],
                     'flower': [self.render('data/ground/flower.png', (60, 60))],
                     'water': [self.render(f'data/ground/water1.png', (60, 60))],
                     'sand': [self.render('data/ground/sand.png', (60, 60))],
                     'snow': [self.render('data/ground/snow.png', (60, 60))]}

        self.border_fractions = {'water': [self.render('data/border_fractions/blue.png', (60, 60)),
                                           self.render('data/border_fractions/blue_circle.png', (60, 60)),
                                           self.render('data/border_fractions/blue_left.png', (60, 60)),
                                           self.render('data/border_fractions/blue_down.png', (60, 60)),
                                           self.render('data/border_fractions/blue_right.png', (60, 60)),
                                           self.render('data/border_fractions/blue_up.png', (60, 60)),
                                           self.render('data/border_fractions/blue_left_down.png', (60, 60)),
                                           self.render('data/border_fractions/blue_down_right.png', (60, 60)),
                                           self.render('data/border_fractions/blue_right_up.png', (60, 60)),
                                           self.render('data/border_fractions/blue_up_left.png', (60, 60)),
                                           self.render('data/border_fractions/blue_left_down_right.png', (60, 60)),
                                           self.render('data/border_fractions/blue_down_right_up.png', (60, 60)),
                                           self.render('data/border_fractions/blue_right_up_left.png', (60, 60)),
                                           self.render('data/border_fractions/blue_up_left_down.png', (60, 60)),
                                           self.render('data/border_fractions/blue_up_down.png', (60, 60)),
                                           self.render('data/border_fractions/blue_left_right.png', (60, 60))],
                                 'earth': [self.render('data/border_fractions/green.png', (60, 60)),
                                           self.render('data/border_fractions/green_circle.png', (60, 60)),
                                           self.render('data/border_fractions/green_left.png', (60, 60)),
                                           self.render('data/border_fractions/green_down.png', (60, 60)),
                                           self.render('data/border_fractions/green_right.png', (60, 60)),
                                           self.render('data/border_fractions/green_up.png', (60, 60)),
                                           self.render('data/border_fractions/green_left_down.png', (60, 60)),
                                           self.render('data/border_fractions/green_down_right.png', (60, 60)),
                                           self.render('data/border_fractions/green_right_up.png', (60, 60)),
                                           self.render('data/border_fractions/green_up_left.png', (60, 60)),
                                           self.render('data/border_fractions/green_left_down_right.png', (60, 60)),
                                           self.render('data/border_fractions/green_down_right_up.png', (60, 60)),
                                           self.render('data/border_fractions/green_right_up_left.png', (60, 60)),
                                           self.render('data/border_fractions/green_up_left_down.png', (60, 60)),
                                           self.render('data/border_fractions/green_up_down.png', (60, 60)),
                                           self.render('data/border_fractions/green_left_right.png', (60, 60))],
                                 'fire': [self.render('data/border_fractions/red.png', (60, 60)),
                                          self.render('data/border_fractions/red_circle.png', (60, 60)),
                                          self.render('data/border_fractions/red_left.png', (60, 60)),
                                          self.render('data/border_fractions/red_down.png', (60, 60)),
                                          self.render('data/border_fractions/red_right.png', (60, 60)),
                                          self.render('data/border_fractions/red_up.png', (60, 60)),
                                          self.render('data/border_fractions/red_left_down.png', (60, 60)),
                                          self.render('data/border_fractions/red_down_right.png', (60, 60)),
                                          self.render('data/border_fractions/red_right_up.png', (60, 60)),
                                          self.render('data/border_fractions/red_up_left.png', (60, 60)),
                                          self.render('data/border_fractions/red_left_down_right.png', (60, 60)),
                                          self.render('data/border_fractions/red_down_right_up.png', (60, 60)),
                                          self.render('data/border_fractions/red_right_up_left.png', (60, 60)),
                                          self.render('data/border_fractions/red_up_left_down.png', (60, 60)),
                                          self.render('data/border_fractions/red_up_down.png', (60, 60)),
                                          self.render('data/border_fractions/red_left_right.png', (60, 60))],
                                 'air': [self.render('data/border_fractions/yellow.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_circle.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_left.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_down.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_right.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_up.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_left_down.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_down_right.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_right_up.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_up_left.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_left_down_right.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_down_right_up.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_right_up_left.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_up_left_down.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_up_down.png', (60, 60)),
                                         self.render('data/border_fractions/yellow_left_right.png', (60, 60))]}

        self.animations_structures = {'tower': [[self.render(f'data/structures/tower/anim{i}.png', (120, 180)) for i in range(1, 6)]],
                                      'mill': [[self.render(f'data/structures/mill/anim{i}.png', (120, 180)) for i in range(1, 4)]],
                                      'mill_support': [[self.render('data/structures/mill/support.png', (60, 60))]],
                                      'mine': [[self.render(f'data/structures/mine/anim{i}.png', (120, 180)) for i in range(1, 8)]],
                                      'homes': [[self.render(f'data/structures/homes/home1_{i}.png', (120, 180)) for i in range(1, 4)],
                                                [self.render(f'data/structures/homes/home2_{i}.png', (120, 180)) for i in range(1, 4)],
                                                [self.render(f'data/structures/homes/home3_{i}.png', (120, 180)) for i in range(1, 4)]],
                                      'sawmill': [[self.render(f'data/structures/sawmill/anim1.png', (120, 180))]],
                                      'fisherman': [[self.render(f'data/structures/fisherman/anim{i}.png', (120, 180)) for i in range(1, 4)]]}

        # self.destroyed_structures = {} для руин

        self.animations_main_structures = {'water': [self.render(f'data/structures/centres/water/anim{i}.png', (120, 180)) for i in range(1, 4)],
                                           'fire': [self.render(f'data/structures/centres/fire/anim{i}.png', (120, 180)) for i in range(1, 4)],
                                           'earth': [self.render(f'data/structures/centres/earth/anim{i}.png', (120, 180)) for i in range(1, 4)],
                                           'air': [self.render(f'data/structures/centres/air/anim{i}.png', (120, 180)) for i in range(1, 4)]}

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
                          'label_online': [self.render(f'data/widgets/menu/labels/ipv4_port.png', (1100, 66)),
                                           self.render(f'data/widgets/menu/labels/ipv4_portt.png', (1100, 66))],
                          'label_count_users': [self.render(f'data/widgets/menu/labels/count_player.png', (550, 66)),
                                                self.render(f'data/widgets/menu/labels/count_playert.png', (550, 66))],
                          'label_port': [self.render(f'data/widgets/menu/labels/port.png', (550, 66)),
                                         self.render(f'data/widgets/menu/labels/portt.png', (550, 66))],
                          'bug_report': [self.render(f'data/widgets/menu/buttons/button10.png', (70, 70)),
                                         self.render(f'data/widgets/menu/buttons/button10t.png', (70, 70))]}

        self.pause = {'background': [self.render(f'data/widgets/menu/labels/background.png', (1920, 1080))],
                      'button_menu': [self.render(f'data/widgets/menu/buttons/button6.png', (400, 70)),
                                      self.render(f'data/widgets/menu/buttons/button6t.png', (400, 70))],
                      'button_setting': self.main_menu['button_setting'],
                      'button_save': [self.render(f'data/widgets/menu/buttons/button9.png', (400, 70)),
                                      self.render(f'data/widgets/menu/buttons/button9t.png', (400, 70))]}

        self.ingame = {'button_end': [self.render(f'data/widgets/menu/buttons/button7.png', (400, 50)),
                                      self.render(f'data/widgets/menu/buttons/button7t.png', (400, 50))],
                       'back_water': [self.render(f'data/ico/fractions/water.png', (60, 60)),
                                      self.render(f'data/ico/fractions/watert.png', (60, 60))],
                       'back_fire': [self.render(f'data/ico/fractions/fire.png', (60, 60)),
                                     self.render(f'data/ico/fractions/firet.png', (60, 60))],
                       'back_air': [self.render(f'data/ico/fractions/air.png', (60, 60)),
                                    self.render(f'data/ico/fractions/airt.png', (60, 60))],
                       'back_earth': [self.render(f'data/ico/fractions/earth.png', (60, 60)),
                                      self.render(f'data/ico/fractions/eartht.png', (60, 60))],
                       'resource': [self.render(f'data/ico/fractions/resource.png', (60, 60)),
                                    self.render(f'data/ico/fractions/no_resource.png', (60, 60))],
                       'back': [self.render('data/ico/fractions/test.png', (1920, 80))]}

        self.buildmenu = {'background': [self.render(f'data/widgets/buildmenu/labels/background.png', (566, 532))],
                          'button_project': [self.render(f'data/widgets/buildmenu/buttons/button1.png', (400, 50)),
                                             self.render(f'data/widgets/buildmenu/buttons/button1t.png', (400, 50))],
                          'button': [self.render(f'data/widgets/buildmenu/buttons/button2.png', (130, 130)),
                                     self.render(f'data/widgets/buildmenu/buttons/button2t.png', (130, 130))]}

        self.save_menu = {'background': [self.render(f'data/widgets/save menu/labels/background.png', (600, 600))],
                          'variant_save': [self.render(f'data/widgets/save menu/buttons/button3.png', (480, 100)),
                                           self.render(f'data/widgets/save menu/buttons/button3t.png', (480, 100))],
                          'button_play': [self.render(f'data/widgets/save menu/buttons/button1.png', (50, 50)),
                                          self.render(f'data/widgets/save menu/buttons/button1t.png', (50, 50))],
                          'button_delete': [self.render(f'data/widgets/save menu/buttons/button2.png', (50, 50)),
                                            self.render(f'data/widgets/save menu/buttons/button2t.png', (50, 50))],
                          'label_save': [self.render(f'data/widgets/menu/labels/name_of_save.png', (1100, 66)),
                                         self.render(f'data/widgets/menu/labels/name_of_savet.png', (1100, 66))]}

        self.setting = {"background": self.save_menu['background'],
                        'nickname': [self.render(f'data/widgets/setting/labels/nickname.png', (560, 50)),
                                     self.render(f'data/widgets/setting/labels/nicknamet.png', (560, 50))],
                        'slicer': [self.render(f'data/widgets/setting/labels/slicer_back.png', (560, 24)),
                                   self.render(f'data/widgets/setting/labels/slicer_point.png', (18, 52))],
                        'switch': [self.render(f'data/widgets/setting/labels/button1.png', (42, 60)),
                                   self.render(f'data/widgets/setting/labels/button1t.png', (42, 60))]}

        self.army = {'small': [self.render(f'data/army/small.png', (60, 60))],
                     'middle': [self.render(f'data/army/midle.png', (60, 60))],
                     'large': [self.render(f'data/army/large.png', (60, 60))]}

    def render(self, address, size):
        if address in self.loaded_textures:
            return self.loaded_textures[address]
        size = size[0] * self.resizer, size[1] * self.resizer
        image = pygame.transform.scale(pygame.image.load(address), size).convert_alpha()
        self.loaded_textures[address] = image
        return image
