import pygame.transform
from obb.Interface.Widgets import *
from obb.Sond_rendering import Sounds
import os


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
    def __init__(self, xoy, textures, fraction):
        r = textures.resizer
        self.button_back = Button(textures.ingame[f'back_{fraction}'], (xoy[0] * 2 - 40 * r, 40 * r))
        self.resource_ico = BackGround(textures.ingame['resource'][0], (xoy[0] * 2 - 300 * r, 40 * r))
        self.count_resource = Label('-', (xoy[0] * 2 - 240 * r, 40 * r), int(30 * r))
        self.back1 = BackGround(textures.ingame['back'][0], (xoy[0], 40 * r))
        self.back2 = BackGround(textures.ingame['back'][0], (xoy[0], xoy[1] * 2 - 40 * r))
        self.surface = Surface(self.back1, self.back2, self.button_back, self.resource_ico, self.count_resource)


class BuildMenu:
    def __init__(self, xoy, textures, coord_select_ground, structures):
        r = textures.resizer
        self.background = BackGround(textures.buildmenu['background'][0], (293 * r, xoy[1] - 194 * r))
        self.select_ground = BackGround(textures.select, coord_select_ground)
        self.button_project = Button(textures.buildmenu['button_project'], (293 * r, xoy[1] - 104 * r))
        self.down = Button(textures.buildmenu['button'], (98 * r, xoy[1] - 230 * r))
        self.up = Button(textures.buildmenu['button'], (488 * r, xoy[1] - 230 * r))
        self.structure = BackGround(pygame.transform.scale(textures.animations_structures[structures[0]][0][0], (240 * r, 360 * r)), (293 * r, xoy[1] - 200 * r))
        self.s1 = BackGround(textures.animations_structures[structures[-1]][0][0], (98 * r, xoy[1] - 210 * r))
        self.s2 = BackGround(textures.animations_structures[structures[1]][0][0], (488 * r, xoy[1] - 210 * r))
        self.surface = Surface(self.background, self.select_ground, self.button_project, self.down, self.up, self.structure, self.s1, self.s2)


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
        self.deleted = list()
        self.save = dict()

    def delete(self, save):
        self.save[save][0].image = self.t.save_menu['variant_save'][1]
        self.save[save][2].active = False
        self.save[save][1].color = (68, 41, 23)
        self.save[save][1].new_text(self.save[save][1].text)
        os.remove(f'saves/{save}')

    def __decode_world(self, name):
        with open(f'saves/{name}', mode='rt') as file:
            distribut = file.read().split(':l:')
            game = distribut[0]
            matr = [[j.split('|') for j in i.split(':t:')] for i in distribut[2].split(':n:')]
            info_players = distribut[1].split(':n:')
        return [matr, name[:-6], [[i.split('|')[0], i.split('|')[1], [int(j) for j in [i.split('|')[2], i.split('|')[3]]], int(i.split('|')[4]), int(i.split('|')[5])] for i in info_players]], game

    def add_saves(self, saves, local, online, handler):
        r = self.r
        y = 210
        for i in saves:
            try:
                spisok = [BackGround(self.t.save_menu['variant_save'][0], (self.xoy[0] - 30 * r, self.xoy[1] - y * r)),
                          Label(i[:-6], (self.xoy[0] - 30 * r, self.xoy[1] - y * r), 30),
                          Button(self.t.save_menu['button_play'], (self.xoy[0] + 235 * r, self.xoy[1] - 25 * r - y * r)),
                          Button(self.t.save_menu['button_delete'], (self.xoy[0] + 235 * r, self.xoy[1] + 25 * r - y * r))]
                decode, game = self.__decode_world(i)
                if game == 'local':
                    spisok[2].connect(local, decode[0], decode[1], decode[2])
                else:
                    spisok[2].connect(online, handler, handler.centre, 'create', decode[0], decode[1], decode[2])
                spisok[3].connect(self.delete, i)
                self.save[i] = spisok
                for s in spisok:
                    self.surface.add(s)
                y -= 105
            except Exception:
                pass


class Setting:
    def __init__(self, xoy, textures):
        r = textures.resizer
        self.background = BackGround(textures.setting['background'][0], xoy)
        self.nickname = InteractLabel(textures.setting['nickname'], (xoy[0], xoy[1] - 255 * r))
        self.surface = Surface(self.background, self.nickname)
