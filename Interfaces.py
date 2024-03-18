from Widgets import *
import Textures


class Pause:
    def __init__(self, xoy, textures=Textures.Textures()):
        self.background = BackGround(textures.pause['background'][0], xoy)
        self.button_menu = Button(textures.pause['button_menu'], xoy)
        self.button_setting = Button(textures.pause['button_setting'], (xoy[0], xoy[1] + 80 * textures.resizer))

    def create_surface(self):
        return Surface(self.background, self.button_menu, self.button_setting)


class Menu:
    def __init__(self, xoy, textures=Textures.Textures()):
        self.background = BackGround(textures.main_menu['background'][0], xoy)
        self.button_start = Button(textures.main_menu['button_start'], (xoy[0] - 530 * textures.resizer, xoy[1] - 450 * textures.resizer))
        self.button_load = Button(textures.main_menu['button_loading'], ( self.button_start.rect.x + 200 * textures.resizer, self.button_start.rect.y + self.button_start.rect[3] + 40 * textures.resizer))
        self.button_online = Button(textures.main_menu['button_online'], (
            self.button_start.rect.x + 200 * textures.resizer, self.button_start.rect.y + self.button_start.rect[3] + 115 * textures.resizer))
        self.button_setting = Button(textures.main_menu['button_setting'], (
            self.button_start.rect.x + 200 * textures.resizer, self.button_start.rect.y + self.button_start.rect[3] + 190 * textures.resizer))
        self.button_exit = Button(textures.main_menu['button_exit'], (
            self.button_start.rect.x + 200 * textures.resizer, self.button_start.rect.y + self.button_start.rect[3] + 265 * textures.resizer))

    def create_surface(self):
        return Surface(self.background, self.button_start, self.button_load, self.button_online, self.button_setting, self.button_exit)


class PopupMenu:
    def __init__(self, xoy, textures=Textures.Textures()):
        r = textures.resizer
        self.button_information = Button(textures.popup_menu['button_information'], (xoy[0] + 130 * r, xoy[1] - 100 * r))
        self.button_build = Button(textures.popup_menu['button_build'], (xoy[0] + 130 * r, xoy[1] - 48 * r))
        self.button_destroy = Button(textures.popup_menu['button_destroy'], (xoy[0] + 130 * r, xoy[1] + 4 * r))
        self.button_fight = Button(textures.popup_menu['button_fight'], (xoy[0] + 130 * r, xoy[1] + 56 * r))
        self.button_cancel = Button(textures.popup_menu['button_cancel'], (xoy[0] + 130 * r, xoy[1] + 108 * r))

    def create_surface(self):
        return Surface(self.button_information, self.button_build, self.button_destroy, self.button_fight, self.button_cancel)
