from Widgets import *
import Textures


class Menu:
    pass


class PopupMenu:
    def __init__(self, xoy, textures=Textures.Textures()):
        background = BackGround(textures.popup_menu['label'], xoy)
        button1 = Button(pygame.transform.scale(textures.popup_menu['label'], (100, 50)), (xoy[0], xoy[1] + 10))
        self.display = Surface(background, button1)
