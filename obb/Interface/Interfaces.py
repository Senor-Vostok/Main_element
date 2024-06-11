import pygame.transform

import obb.Constants
from obb.Interface.Widgets import *
import os


class Pause:
    def __init__(self, language_data, xoy, name_world, textures):
        self.background = BackGround(textures.pause['background'][0], xoy)
        self.title_world = Label(name_world, (xoy[0], xoy[1] - 120 * textures.resizer), 30, (48, 35, 22))
        self.button_menu = Button(textures.main_menu['button2'], (xoy[0], xoy[1] + 40 * textures.resizer), True, language_data['menu'])
        self.button_setting = Button(textures.main_menu['button2'], (xoy[0], xoy[1] - 40 * textures.resizer), True, language_data['settings'].lower())
        self.surface = Surface(self.background, self.button_menu, self.button_setting, self.title_world)


class EndGame:
    def __init__(self, language_data, xoy, textures, status='lose'):
        r = textures.resizer
        self.title = Label(language_data['lose'] if status == 'lose' else language_data['win'], xoy, int(50 * r), (52, 35, 11) if status == 'lose' else (182, 116, 20))
        self.ico = BackGround(textures.main_menu['winner_ico' if status != 'lose' else 'loser_ico'][0], (xoy[0], xoy[1] - 100 * r))
        self.surface = Surface(self.title, self.ico)


class SelectUnions:
    def __init__(self, language_data, xoy, textures, selected):
        r = textures.resizer
        self.drag = Slicer(textures.setting['slicer'], xoy, int(selected[0][5]), int(selected[0][5]))
        self.confirm = Button(textures.main_menu['button3'], (xoy[0], xoy[1] + 50 * r), True, language_data['attack'])
        self.surface = Surface(self.drag, self.confirm)


class HelloMenu:
    def __init__(self, language_data, xoy, textures):
        r = textures.resizer
        self.background = BackGround(textures.main_menu['hello_background'][0], xoy)
        self.main_ico = BackGround(textures.main_menu['name'][0], (xoy[0], xoy[1] - 430 * r))
        with open('data/user/about_world', mode='rt', encoding='utf-8') as file:
            file = file.read()
            self.hello_text = Label(file, (20 * r, xoy[1] - 240 * r), int(20 * r), DEFAULT_COLOR, centric=False)
        self.info = Label('Нажмите ESC для продолжения', (xoy[0], xoy[1] + 440 * r), int(30 * r))
        self.surface = Surface(self.background, self.main_ico, self.hello_text, self.info)


class Menu:
    def __init__(self, language_data, xoy, textures):
        self.background = BackGround(textures.main_menu['background'][0], xoy)
        self.button_start = Button(textures.main_menu['button1'],
                                   (xoy[0] - 530 * textures.resizer, xoy[1] - 450 * textures.resizer), True, language_data['new_game'])
        self.button_load = Button(textures.main_menu['button2'], (
            self.button_start.rect.x + 200 * textures.resizer,
            self.button_start.rect.y + self.button_start.rect[3] + 40 * textures.resizer), True, language_data['download_game'])
        self.button_online = Button(textures.main_menu['button2'], (
            self.button_start.rect.x + 200 * textures.resizer,
            self.button_start.rect.y + self.button_start.rect[3] + 115 * textures.resizer), True, language_data['online'])
        self.button_setting = Button(textures.main_menu['button2'], (
            self.button_start.rect.x + 200 * textures.resizer,
            self.button_start.rect.y + self.button_start.rect[3] + 190 * textures.resizer), True, language_data['settings'])
        self.button_exit = Button(textures.main_menu['button2'], (
            self.button_start.rect.x + 200 * textures.resizer,
            self.button_start.rect.y + self.button_start.rect[3] + 265 * textures.resizer), True, language_data['quit'])
        self.bug_report = Button(textures.main_menu['bug_report'], (self.button_start.rect.x + 35 * textures.resizer, self.button_start.rect.y + self.button_start.rect[3] + 340 * textures.resizer))
        self.surface = Surface(self.background, self.button_start, self.button_load, self.button_online, self.button_setting, self.button_exit, self.bug_report)


class PopupMenu:
    def __init__(self, language_data, xoy, textures):
        r = textures.resizer
        self.button_information = InteractLabel(textures.popup_menu['button_information'], (xoy[0] + 130 * r, xoy[1] - 100 * r), False, True)
        self.button_build = Button(textures.main_menu['button3'], (xoy[0] + 130 * r, xoy[1] - 48 * r), True, language_data['bild'])
        self.button_destroy = Button(textures.main_menu['button3'], (xoy[0] + 130 * r, xoy[1] + 4 * r), True, language_data['destroy'])
        self.button_buy = Button(textures.main_menu['button3'], (xoy[0] + 130 * r, xoy[1] + 56 * r), True, language_data['buy'])
        self.surface = Surface(self.button_information, self.button_build, self.button_destroy, self.button_buy)


class InGame:
    def __init__(self, language_data, xoy, textures, fraction):
        r = textures.resizer
        self.button_back = Button(textures.ingame[f'back_{fraction}'], (xoy[0] * 2 - 40 * r, 40 * r))
        self.resource_ico = BackGround(textures.ingame['resource'][0], (xoy[0] * 2 - 300 * r, 40 * r))
        self.count_resource = Label('-', (xoy[0] * 2 - 240 * r, 40 * r), int(30 * r))
        self.back1 = BackGround(textures.ingame['back'][0], (xoy[0], 40 * r))
        self.back2 = BackGround(textures.ingame['back'][0], (xoy[0], xoy[1] * 2 - 40 * r))
        self.state_game = Switch(textures.setting['switch'], (xoy[0] * 2 - 400 * r, 40 * r))
        self.surface = Surface(self.back1, self.back2, self.button_back, self.resource_ico, self.count_resource, self.state_game)


class BuildMenu:
    def __init__(self, language_data, xoy, textures, coord_select_ground, structures):
        r = textures.resizer
        self.background = BackGround(textures.buildmenu['background'][0], (293 * r, xoy[1] - 194 * r))
        self.select_ground = BackGround(textures.select, coord_select_ground)
        self.button_project = Button(textures.main_menu['button3'], (293 * r, xoy[1] - 104 * r), True, language_data['create'])
        self.down = Button(textures.buildmenu['button'], (98 * r, xoy[1] - 230 * r))
        self.up = Button(textures.buildmenu['button'], (488 * r, xoy[1] - 230 * r))
        self.structure = BackGround(pygame.transform.scale(textures.animations_structures[structures[0]][0][0], (240 * r, 360 * r)), (293 * r, xoy[1] - 200 * r))
        self.s1 = BackGround(textures.animations_structures[structures[-1]][0][0], (98 * r, xoy[1] - 210 * r))
        self.s2 = BackGround(textures.animations_structures[structures[1]][0][0], (488 * r, xoy[1] - 210 * r))
        self.about = Label(f'Empty message', (90 * r, xoy[1] - 20 * r), int(15 * r))
        self.surface = Surface(self.background, self.select_ground, self.button_project, self.down, self.up, self.structure, self.s1, self.s2, self.about)


class Online_connect:
    def __init__(self, language_data, xoy, textures):
        self.text = Label(language_data['ip_port'], (xoy[0], xoy[1] - 55 * textures.resizer), int(30 * textures.resizer), obb.Constants.TEXT_ENABLE)
        self.interact = InteractLabel(textures.main_menu['label2'], (xoy[0], xoy[1]), True, True)
        self.surface = Surface(self.interact, self.text)


class Online_create:
    def __init__(self, language_data, xoy, textures):
        r = textures.resizer
        self.text1 = Label(language_data['count_players'], (xoy[0] - 280 * r, xoy[1] - 55 * r), int(30 * r), obb.Constants.TEXT_DISABLE)
        self.text2 = Label(language_data['port'], (xoy[0] + 280 * r, xoy[1] - 55 * r), int(30 * r), obb.Constants.TEXT_DISABLE)
        self.count = InteractLabel(textures.main_menu['label1'], (xoy[0] - 280 * r, xoy[1]), True, True)
        self.port = InteractLabel(textures.main_menu['label1'], (xoy[0] + 280 * r, xoy[1]), True, True)
        self.surface = Surface(self.count, self.port, self.text1, self.text2)


class CreateSave:
    def __init__(self, language_data, xoy, textures):
        r = textures.resizer
        self.text = Label(language_data['name_world'], (xoy[0], xoy[1] - 55 * r), int(30 * r), obb.Constants.TEXT_ENABLE)
        self.name = InteractLabel(textures.main_menu['label2'], xoy, True, True)
        self.surface = Surface(self.name, self.text)


class ChoiceGame:
    def __init__(self, language_data, xoy, textures):
        r = textures.resizer
        self.button_local = Button(textures.main_menu['button2'], (xoy[0], xoy[1] - 40 * r), True, language_data['local'].lower())
        self.button_online = Button(textures.main_menu['button2'], (xoy[0], xoy[1] + 40 * r), True, language_data['online'].lower())
        self.surface = Surface(self.button_local, self.button_online)


class Save_menu:
    def __init__(self, language_data, xoy, textures):
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
        return [matr, name[:-6], [[i.split('|')[0], i.split('|')[1], i.split('|')[2], [int(j) for j in [i.split('|')[3], i.split('|')[4]]], int(i.split('|')[5]), int(i.split('|')[6])] for i in info_players]], game

    def add_saves(self, saves, local, online, handler):
        r = self.r
        y = 210
        for i in saves:
            try:
                decode, game = self.__decode_world(i)
                spisok = [BackGround(self.t.save_menu['variant_save'][0], (self.xoy[0] - 30 * r, self.xoy[1] - y * r)),
                          Label(i[:-6], (self.xoy[0] - 30 * r, self.xoy[1] - y * r), int(30 * r)),
                          Button(self.t.save_menu['button_play'], (self.xoy[0] + 235 * r, self.xoy[1] - 25 * r - y * r)),
                          Button(self.t.save_menu['button_delete'], (self.xoy[0] + 235 * r, self.xoy[1] + 25 * r - y * r)),
                          BackGround(self.t.ingame[f'back_{decode[2][0][2]}'][0], (self.xoy[0] - 215 * r, self.xoy[1] - y * r))]
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
    def __init__(self, language_data, xoy, textures):
        r = textures.resizer
        self.background = BackGround(textures.setting['background'][0], xoy)
        self.nickname = InteractLabel(textures.setting['nickname'], (xoy[0], xoy[1] - 255 * r))
        self.label_sound = Label(language_data['volume'], (xoy[0], xoy[1] - 200 * r), int(20 * r))
        self.sound_loud = Slicer(textures.setting['slicer'], (xoy[0], xoy[1] - 150 * r), 100, 1)
        self.language = Button(textures.main_menu['button3'], (xoy[0], xoy[1] - 80 * r), True, language_data['lang'])
        self.surface = Surface(self.background, self.nickname, self.label_sound, self.sound_loud, self.language)


class SettingLanguage:
    def __init__(self, language_data, xoy, textures, func):
        r = textures.resizer
        languages = list()
        i = 0
        for language in os.listdir('data/language'):
            image = textures.main_menu['button3']
            with open(f'data/language/{language}/name.txt', mode='rt', encoding='utf-8') as file:
                button = Button(image, (xoy[0], xoy[1] + (image[0].get_rect()[3] + 5) * i), True, file.read())
                button.connect(func, language)
            i += 1
            languages.append(button)
        self.surface = Surface(*languages)
