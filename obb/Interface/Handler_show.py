import obb.Interface.Interfaces as Interfaces
import sys


def show_ingame(self, centre):
    game = Interfaces.InGame(centre, self.textures)
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
    menu.button_load.connect(self.open_save)
    menu.button_online.connect(show_online, self, self.centre)
    menu.button_exit.connect(sys.exit)
    self.interfaces['menu'] = menu


def show_buildmenu(self, centre, ground=None):
    build = Interfaces.BuildMenu(centre, self.textures)
    build.down.connect(self.next_struct, -1)
    build.up.connect(self.next_struct, 1)
    self.now_str = 0
    build.button_project.connect(self.place_structure, ground)
    if 'popup_menu' in self.interfaces: self.interfaces.pop('popup_menu')
    self.interfaces['buildmenu'] = build


def show_online(self, centre, t='connect', matr=None):
    self.interfaces = dict()
    show_menu(self, self.centre)
    if 'choicegame' in self.interfaces: self.close('choicegame', True)
    if t == 'connect':
        label = Interfaces.Online_connect(centre, self.textures)
        label.interact.connect(self.connecting)
        self.interfaces['online'] = label
    elif t == 'create':
        label = Interfaces.Online_create(centre, self.textures)
        label.count.connect(self.host_game, matr)
        label.port.connect(self.host_game, matr)
        self.interfaces['online'] = label


def show_pause(self, centre):
    pause = Interfaces.Pause(centre, self.name_save, self.textures)
    pause.button_menu.connect(self.go_back_to_menu)
    self.interfaces['pause'] = pause


def show_popup_menu(self, centre, ground=None, fraction=None):
    popup = Interfaces.PopupMenu(centre, self.textures)
    popup.button_build.connect(show_buildmenu, self, self.centre, ground)
    popup.button_destroy.connect(self.place_structure, ground, 'null', True)
    popup.button_buy.connect(self.buy_ground, (int(ground.biom[2]), int(ground.biom[3])), fraction, self.me)
    self.interfaces['popup_menu'] = popup


def show_choicegame(self, centre, matr=None, n=None):
    self.name_save = self.interfaces['create_save'].name.text[:-1] if not n else n
    self.interfaces = dict()
    show_menu(self, self.centre)
    choice = Interfaces.ChoiceGame(centre, self.textures)
    choice.button_local.connect(self.init_world, matr)
    choice.button_online.connect(show_online, self, self.centre, 'create', matr)
    self.interfaces['choicegame'] = choice
