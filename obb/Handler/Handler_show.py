import obb.Interface.Interfaces as Interfaces
from obb.Image_rendering.Resources import Resource
import sys
import os


def close(self, name, open_some, func=None):
    self.open_some = open_some
    self.interfaces.pop(name)
    if func: func()


def show_ingame(self, centre):
    game = Interfaces.InGame(centre, self.textures, self.me.fraction_name)
    game.button_back.connect(self.move_to_coord, self.me.start_point)
    self.interfaces['ingame'] = game


def show_create_save(self, centre):
    self.interfaces = dict()
    show_menu(self, self.centre)
    name = Interfaces.CreateSave(centre, self.textures)
    name.name.connect(show_choicegame, self, centre, None)
    self.interfaces['create_save'] = name


def show_menu(self, centre):
    menu = Interfaces.Menu(centre, self.textures)
    menu.button_start.connect(show_create_save, self, self.centre)
    if len([i for i in os.listdir('saves') if len(i.split('.maiso')) > 1]) > 4:
        menu.button_start.connect(self.open_save)
    menu.button_load.connect(self.open_save)
    menu.button_online.connect(show_online, self, self.centre)
    menu.button_setting.connect(show_settings, self, self.centre)
    menu.button_exit.connect(sys.exit)
    self.interfaces['menu'] = menu


def show_buildmenu(self, centre, ground=None):
    build = Interfaces.BuildMenu(centre, self.textures, (ground.rect[0] + ground.rect[2] // 2, ground.rect[1] + ground.rect[3] // 2), self.structures)
    build.down.connect(self.next_struct, -1)
    build.up.connect(self.next_struct, 1)
    self.now_structure = 0
    i, j = int(ground.biome[2]), int(ground.biome[3])
    build.button_project.connect(self.place_structure, (i, j), None, True, self.me)
    if 'popup_menu' in self.interfaces: self.interfaces.pop('popup_menu')
    self.interfaces['buildmenu'] = build


def show_online(self, centre, t='connect', matr=None, name_save=None, info_players=None):
    if name_save:
        self.loaded_save = True
        self.name_save = name_save
        self.info_players = info_players
    self.interfaces = dict()
    show_menu(self, self.centre)
    if 'choicegame' in self.interfaces: close(self, 'choicegame', True)
    if t == 'connect':
        label = Interfaces.Online_connect(centre, self.textures)
        label.interact.connect(self.connecting)
        self.interfaces['online'] = label
    elif t == 'create':
        label = Interfaces.Online_create(centre, self.textures)
        label.count.connect(self.host_game, matr)
        if self.loaded_save:
            label.count.active = not self.loaded_save
            label.count.text = f"{len([i for i in [j[0] for j in self.info_players] if 'bot' not in i])}/"
        label.port.connect(self.host_game, matr)
        self.interfaces['online'] = label


def show_pause(self, centre):
    pause = Interfaces.Pause(centre, self.name_save, self.textures)
    pause.button_menu.connect(self.go_back_to_menu)
    self.interfaces['pause'] = pause


def show_popup_menu(self, centre, ground, fraction):
    popup = Interfaces.PopupMenu(centre, self.textures)
    popup.button_build.connect(show_buildmenu, self, self.centre, ground)
    i, j = int(ground.biome[2]), int(ground.biome[3])
    popup.button_destroy.connect(self.place_structure, (i, j), 'null', True, self.me)
    popup.button_buy.connect(self.set_fraction, (i, j), fraction, True, self.me)
    self.interfaces['popup_menu'] = popup


def show_choicegame(self, centre, matr=None):
    self.name_save = self.interfaces['create_save'].name.text[:-1]
    self.interfaces = dict()
    show_menu(self, self.centre)
    choice = Interfaces.ChoiceGame(centre, self.textures)
    choice.button_local.connect(self.init_world, matr)
    choice.button_online.connect(show_online, self, self.centre, 'create', matr)
    self.interfaces['choicegame'] = choice


def show_settings(self, centre):
    self.interfaces = dict()
    show_menu(self, self.centre)
    setting = Interfaces.Setting(centre, self.textures)
    setting.nickname.text = "Ваш ник/"
    self.interfaces['setting'] = setting


def show_resources(self, count):
    if count <= 0:
        return
    count = 10 if count > 10 else count
    y = self.interfaces['ingame'].back2.rect[1]
    interval = self.size[0] // count
    for i in range(self.size[0], self.size[0] * 2, interval):
         self.effects_disappearance_resource.append(Resource((i / 2, y), self.textures.ingame['resource'][0]))
