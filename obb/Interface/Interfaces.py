import pygame.transform
from obb.Interface.Widgets import *


class Pause:
    def __init__(self, xoy, name_world, textures):
        self.background = BackGround(textures.pause['background'][0], xoy)
        self.title_world = Label(name_world, (xoy[0], xoy[1] - 120 * textures.resizer), 30, (48, 35, 22))
        self.button_menu = Button(textures.pause['button_menu'], (xoy[0], xoy[1] - 40 * textures.resizer))
        self.button_setting = Button(textures.pause['button_setting'], (xoy[0], xoy[1] + 40 * textures.resizer))
        self.surface = Surface(self.background, self.button_menu, self.button_setting, self.title_world)


class Menu:
    def __init__(self, xoy, textures):
        self.background = BackGround(textures.main_menu['background'][0], xoy)
        self.button_start = Button(textures.main_menu['button_start'],
                                   (xoy[0] - 530 * textures.resizer, xoy[1] - 450 * textures.resizer))
        self.button_load = Button(textures.main_menu['button_loading'], (
            self.button_start.rect.x + 200 * textures.resizer,
            self.button_start.rect.y + self.button_start.rect[3] + 40 * textures.resizer))
        self.button_online = Button(textures.main_menu['button_online'], (
            self.button_start.rect.x + 200 * textures.resizer,
            self.button_start.rect.y + self.button_start.rect[3] + 115 * textures.resizer))
        self.button_setting = Button(textures.main_menu['button_setting'], (
            self.button_start.rect.x + 200 * textures.resizer,
            self.button_start.rect.y + self.button_start.rect[3] + 190 * textures.resizer))
        self.button_exit = Button(textures.main_menu['button_exit'], (
            self.button_start.rect.x + 200 * textures.resizer,
            self.button_start.rect.y + self.button_start.rect[3] + 265 * textures.resizer))
        self.surface = Surface(self.background, self.button_start, self.button_load, self.button_online,
                               self.button_setting, self.button_exit)


class PopupMenu:
    def __init__(self, xoy, textures):
        r = textures.resizer
        self.button_information = Button(textures.popup_menu['button_information'],
                                         (xoy[0] + 130 * r, xoy[1] - 100 * r))
        self.button_build = Button(textures.popup_menu['button_build'], (xoy[0] + 130 * r, xoy[1] - 48 * r))
        self.button_destroy = Button(textures.popup_menu['button_destroy'], (xoy[0] + 130 * r, xoy[1] + 4 * r))
        self.button_fight = Button(textures.popup_menu['button_fight'], (xoy[0] + 130 * r, xoy[1] + 56 * r))
        self.button_cancel = Button(textures.popup_menu['button_cancel'], (xoy[0] + 130 * r, xoy[1] + 108 * r))
        self.button_buy = Button(textures.popup_menu['button_cancel'], (xoy[0] + 130 * r, xoy[1] + 160 * r))
        self.surface = Surface(self.button_information, self.button_build, self.button_destroy, self.button_fight,
                               self.button_cancel, self.button_buy)


class InGame:
    def __init__(self, xoy, textures):
        r = textures.resizer
        self.button_end = Button(textures.ingame['button_end'], (xoy[0] - 755 * r, xoy[1] + 510 * r))
        self.surface = Surface(self.button_end)


class BuildMenu:
    def __init__(self, xoy, textures):
        r = textures.resizer
        self.background = BackGround(textures.buildmenu['background'][0], (xoy[0] + 705 * r, xoy[1]))
        self.button_project = Button(textures.buildmenu['button_project'], (xoy[0] + 705 * r, xoy[1] + 465 * r))
        self.down = Button(textures.buildmenu['down'], (xoy[0] + 705 * r, xoy[1] + 361 * r))
        self.up = Button(textures.buildmenu['up'], (xoy[0] + 705 * r, xoy[1] - 381 * r))
        self.structure = BackGround(
            pygame.transform.scale(textures.animations_structures['tower'][0], (360 * r, 540 * r)),
            (xoy[0] + 705 * r, xoy[1]))
        self.surface = Surface(self.background, self.button_project, self.down, self.up, self.structure)


class Online_connect:
    def __init__(self, xoy, textures):
        self.interact = InteractLabel(textures.main_menu['label_online'], (xoy[0], xoy[1]))
        self.surface = Surface(self.interact)


class Online_create:
    def __init__(self, xoy, textures):
        r = textures.resizer
        self.count = InteractLabel(textures.main_menu['label_count_users'], (xoy[0] - 280 * r, xoy[1]))
        self.port = InteractLabel(textures.main_menu['label_port'], (xoy[0] + 280 * r, xoy[1]))
        self.surface = Surface(self.count, self.port)


class CreateSave:
    def __init__(self, xoy, textures):
        r = textures.resizer
        self.name = InteractLabel(textures.save_menu['label_save'], xoy)
        self.surface = Surface(self.name)


class ChoiceGame:
    def __init__(self, xoy, textures):
        r = textures.resizer
        self.button_local = Button(textures.main_menu['button_local'], (xoy[0], xoy[1] - 40 * r))
        self.button_online = Button(textures.main_menu['button_online'], (xoy[0], xoy[1] + 40 * r))
        self.surface = Surface(self.button_local, self.button_online)


class Save_menu:
    def __init__(self, xoy, textures):
        self.r = textures.resizer
        self.t = textures
        self.xoy = xoy
        self.background = BackGround(textures.save_menu['background'][0], xoy)
        self.surface = Surface(self.background)
        self.save = dict()

    def delete(self, save):
        print(f'saves/{save}')

    def __decode_world(self, name):
        matr = None
        with open(f'saves/{name}', mode='rt') as file:
            matr = [[j.split('|') for j in i.split('\t')] for i in file.read().split('\n')]
        return matr, name[:-6]

    def add_saves(self, saves, choice, handler):
        r = self.r
        y = 210
        for i in saves:
            spisok = [BackGround(self.t.save_menu['variant_save'][0], (self.xoy[0] - 30 * r, self.xoy[1] - y * r)),
                      Label(i[:-6], (self.xoy[0] - 30 * r, self.xoy[1] - y * r), 30),
                      Button(self.t.save_menu['button_play'], (self.xoy[0] + 235 * r, self.xoy[1] - 25 * r - y * r)),
                      Button(self.t.save_menu['button_delete'], (self.xoy[0] + 235 * r, self.xoy[1] + 25 * r - y * r))]
            decode = self.__decode_world(i)
            spisok[2].connect(choice, handler, handler.centre, decode[0], decode[1])
            spisok[3].connect(self.delete, i)
            self.save[i] = spisok
            for s in spisok:
                self.surface.add(s)
            y -= 105


class Setting:
    def __init__(self, xoy, textures):
        r = textures.resizer
        self.background = BackGround(textures.setting['background'][0], xoy)
        self.nickname = InteractLabel(textures.setting['nickname'], (xoy[0], xoy[1] - 255 * r))
        self.surface = Surface(self.background, self.nickname)
