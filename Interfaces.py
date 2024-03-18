from Widgets import *
import Textures


class Menu:
    def __init__(self, xoy, textures=Textures.Textures()):
        self.background = BackGround(textures.main_menu['background'][0], xoy)
        self.button_start = Button(textures.main_menu['button_start'], (xoy[0] - 530, xoy[1] - 450))

    def create_surface(self):
        return Surface(self.background, self.button_start)


class PopupMenu:
    def __init__(self, xoy, textures=Textures.Textures()):
        background = BackGround(textures.popup_menu['label'], xoy)
        button1 = Button(pygame.transform.scale(textures.popup_menu['label'], (100, 50)), (xoy[0], xoy[1] + 10))
        self.display = Surface(background, button1)
