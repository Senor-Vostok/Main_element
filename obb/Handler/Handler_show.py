import obb.Constants
import obb.Interface.Interfaces as Interfaces
from obb.Image_rendering.Resources import Resource
import webbrowser
import pygame
import sys
import os


def close(self, name, open_some, func=None):
    self.open_some = open_some
    self.interfaces.pop(name)
    if func: func()


def show_ingame(self, centre):
    game = Interfaces.InGame(self.language_data, centre, self.textures, self.me.fraction_name)
    game.button_back.connect(self.move_to_coord, self.me.start_point)
    self.interfaces['ingame'] = game


def show_end_game(self, centre, status):
    end = Interfaces.EndGame(self.language_data, centre, self.textures, status)
    self.interfaces['end'] = end


def show_create_save(self, centre):
    close_useless(self)
    name = Interfaces.CreateSave(self.language_data, centre, self.textures)
    name.name.connect(show_choicegame, self, centre, None)
    self.interfaces['create_save'] = name


def show_hello_menu(self, centre):
    hello = Interfaces.HelloMenu(self.language_data, centre, self.textures)
    self.interfaces['hello'] = hello


def show_menu(self, centre):
    menu = Interfaces.Menu(self.language_data, centre, self.textures)
    menu.button_start.connect(show_create_save, self, self.centre)
    if len([i for i in os.listdir('saves') if len(i.split('.maiso')) > 1]) > 4:
        menu.button_start.connect(self.open_save)
    menu.button_load.connect(self.open_save)
    menu.button_online.connect(show_online, self, self.centre)
    menu.button_setting.connect(show_settings, self, self.centre)
    menu.button_exit.connect(self.quit)
    menu.bug_report.connect(webbrowser.open, 'https://forms.gle/sdNSuzHwrFXjS7rK8')
    self.interfaces['menu'] = menu


def show_buildmenu(self, centre, ground=None):
    build = Interfaces.BuildMenu(self.language_data, centre, self.textures, (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2), self.structures)
    build.down.connect(self.next_struct, -1)
    build.up.connect(self.next_struct, 1)
    self.now_structure = 0
    struct = self.structures[self.now_structure]
    build.about.new_text(f'{self.language_data["price"]}: {self.rules["StructuresCosts"][struct][0]}\n{self.language_data["gives"]}: {self.language_data["resource"]} - {self.rules["ResourcesFromStructures"][struct][0]}, {self.language_data["army"]} - {self.rules["ArmyFromStructures"][struct][0]}, {self.language_data["def"]} - {self.rules["StructuresProtection"][struct][0]}\n{self.language_data["info"]}: {self.language_data[struct]}')
    i, j = int(ground.biome[2]), int(ground.biome[3])
    build.button_project.connect(self.place_structure, (i, j), None, True, self.me)
    if 'popup_menu' in self.interfaces: self.interfaces.pop('popup_menu')
    self.interfaces['buildmenu'] = build


def show_online(self, centre, t='connect', matr=None, name_save=None, info_players=None):
    close_useless(self)
    if name_save:
        self.loaded_save = True
        self.name_save = name_save
        self.info_players = info_players
    if 'choicegame' in self.interfaces: close(self, 'choicegame', True)
    if t == 'connect':
        label = Interfaces.Online_connect(self.language_data, centre, self.textures)
        label.interact.connect(self.connecting)
        self.interfaces['online'] = label
    elif t == 'create':
        label = Interfaces.Online_create(self.language_data, centre, self.textures)
        label.count.connect(self.host_game, matr)
        if self.loaded_save:
            label.count.active = not self.loaded_save
            label.count.text = f"{len([i for i in [j[1] for j in self.info_players] if 'bot' not in i])}/"
        label.port.connect(self.host_game, matr)
        self.interfaces['online'] = label


def show_pause(self, centre):
    pause = Interfaces.Pause(self.language_data, centre, self.name_save, self.textures)
    pause.button_menu.connect(self.go_back_to_menu)
    pause.button_setting.connect(show_settings, self, centre, False)
    self.interfaces['pause'] = pause


def show_popup_menu(self, centre, ground, fraction):
    close_useless(self)
    popup = Interfaces.PopupMenu(self.language_data, centre, self.textures)
    popup.button_build.connect(show_buildmenu, self, self.centre, ground)
    popup.button_information.text = ground.biome[5]
    i, j = int(ground.biome[2]), int(ground.biome[3])
    popup.button_destroy.connect(self.place_structure, (i, j), 'null', True, self.me)
    popup.button_buy.connect(self.set_fraction, (i, j), fraction, True, self.me)
    self.interfaces['popup_menu'] = popup


def show_selectunions(self, center, selected):
    select = Interfaces.SelectUnions(self.language_data, center, self.textures, selected)
    select.confirm.connect(self.attack, self.me, selected)
    self.interfaces['attack'] = select


def show_choicegame(self, centre, matr=None):
    self.name_save = self.interfaces['create_save'].name.text
    self.interfaces.pop('create_save')
    choice = Interfaces.ChoiceGame(self.language_data, centre, self.textures)
    choice.button_local.connect(self.init_world, matr)
    choice.button_online.connect(show_online, self, self.centre, 'create', matr)
    self.interfaces['choicegame'] = choice


def show_settings(self, centre, active=True):
    close_useless(self)
    setting = Interfaces.Setting(self.language_data, centre, self.textures)
    setting.nickname.connect(self.save_settings, 'nickname')
    setting.sound_loud.now_sector = 100 * self.volumes_channels[0]  # Проценты
    setting.sound_loud.connect(self.change_volume, setting.sound_loud, 0)
    setting.language.connect(show_languages, self, (centre[0] + setting.background.rect[2] // 2 + setting.language.rect[2] // 2, centre[1] - setting.background.rect[3] // 2 + setting.language.rect[3] // 2))
    setting.nickname.text = self.me.nickname
    setting.nickname.active = active
    setting.language.active = active
    self.interfaces['setting'] = setting


def show_languages(self, centre):
    language = Interfaces.SettingLanguage(self.language_data, centre, self.textures, self.export_language)
    self.interfaces['language_setting'] = language


def show_resources(self, count):
    if count <= 0:
        return
    count = obb.Constants.MAX_RESOURCE_ON_SCREEN if count > obb.Constants.MAX_RESOURCE_ON_SCREEN else count
    y = self.interfaces['ingame'].back2.rect[1]
    interval = self.size[0] // count
    for i in range(self.size[0], self.size[0] * 2, interval):
         self.effects_disappearance_resource.append(Resource((i / 2, y), self.textures.ingame['resource'][0]))


def close_useless(self):
    if 'menu' in self.interfaces and len(self.interfaces) > 1:
        self.interfaces.pop([_ for _ in self.interfaces if self.interfaces[_] == self.last_interface][0])
