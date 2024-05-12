import pygame

import obb.Constants
from obb.Constants import DEFAULT_COLOR
from obb.Sond_rendering.Sounds import Sounds
sounds = Sounds()


class Button(pygame.sprite.Sprite):
    def __init__(self, image, xoy, active=True):
        pygame.sprite.Sprite.__init__(self)
        self.state = image[0]
        self.trigger = image[1]
        self.image = self.state
        self.func = None
        self.args = None
        self.active = active
        self.rect = self.image.get_rect(center=xoy)
        self.one_press = True

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if not self.active:
            return
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1):
            self.image = self.trigger
            if mouse_click[2] and mouse_click[3] == 1 and self.func:
                if self.one_press:
                    self.one_press = False
                    pygame.mixer.Channel(1).play(sounds.click)
                    self.func(*self.args)
            else:
                self.one_press = True
        else:
            self.image = self.state


class Switch(pygame.sprite.Sprite):
    def __init__(self, image, xoy, active=False):
        pygame.sprite.Sprite.__init__(self)
        self.active = active
        self.enable = image[0]
        self.disable = image[1]
        self.one_press = False
        self.func, self.args = None, None
        if self.active:
            self.image = self.enable
        else:
            self.image = self.disable
        self.rect = self.image.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and mouse_click[2] and mouse_click[3] == 1:
            if self.one_press:
                return
            pygame.mixer.Channel(1).play(sounds.click)
            self.one_press = True
            self.active = not self.active
            self.image = self.enable if self.active else self.disable
        else:
            self.one_press = False


class Slicer(pygame.sprite.Sprite):
    def __init__(self, image, xoy, cuts=1, now_sector=1):
        pygame.sprite.Sprite.__init__(self)
        self.back_image = image[0]
        self.point_image = image[1]
        self.cuts = cuts
        self.func, self.args = None, None
        self.now_sector = now_sector
        self.rect = self.back_image.get_rect(center=xoy)

    def draw(self, screen):
        delta_x = ((self.rect[2] - self.point_image.get_rect()[2]) / self.cuts) * self.now_sector
        screen.blit(self.back_image, self.rect)
        screen.blit(self.point_image, (self.rect.x + delta_x, self.rect.y - (self.point_image.get_rect()[3] // 2 - self.rect[3] // 2)))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and mouse_click[2] and mouse_click[3] == 1:
            if self.now_sector != (mouse_click[0] - self.rect[0]) // (self.rect[2] / self.cuts) + 1:
                if self.func:
                    self.func(*self.args)
                self.now_sector = int((mouse_click[0] - self.rect[0]) // (self.rect[2] / self.cuts) + 1)


class InteractLabel(pygame.sprite.Sprite):
    def __init__(self, image, xoy, active=True, center=False):
        pygame.sprite.Sprite.__init__(self)
        self.center = center
        self.state = image[0]
        self.flex = image[1]
        self.image = self.state
        self.text = "/"
        self.func = None
        self.args = None
        self.active = active
        self.rect = self.image.get_rect(center=xoy)
        self.font = pygame.font.Font("19363.ttf", self.rect[3] - self.rect[3] // 3)
        self.can_write = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        image = self.font.render(self.text[-1:], False, DEFAULT_COLOR)
        i = 1
        while image.get_rect()[2] < self.rect[2] - 50 and i <= len(self.text):
            image = self.font.render(self.text[-i:], False, DEFAULT_COLOR)
            i += 1
        if not self.center:
            screen.blit(image, (self.rect[0] + 10, self.rect[1] + 6))
        else:
            screen.blit(image, (self.rect[0] + self.rect[2] // 2 - image.get_rect()[2] // 2, self.rect[1] + 6))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if not self.active:
            return
        if not self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and mouse_click[2] and mouse_click[3] == 1:
            self.can_write = False
            self.image = self.state
        elif self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1) and mouse_click[2] and mouse_click[3] == 1:
            self.can_write = True
            self.image = self.flex
        elif self.can_write:
            self.go_write(command)

    def go_write(self, command):
        if command:
            if (command.key == pygame.K_v) and (command.mod & pygame.KMOD_CTRL):
                self.text = self.text[:-1] + ("".join(str(pygame.scrap.get(pygame.SCRAP_TEXT))[2:].split(r"\x00")))[:-1] + "/"
            elif command.key == pygame.K_BACKSPACE:
                self.text = self.text[:-2] + "/"
            elif int(command.key) == obb.Constants.KEY_ENTER:
                if self.func:
                    self.func(*self.args)
            elif len(str(command.unicode)) > 0 and command.type == pygame.KEYDOWN:
                self.text = self.text[:-1] + command.unicode + "/"


class Surface:
    def __init__(self, *args):
        self.widgets = list()
        for i in args:
            self.widgets.append(i)

    def add(self, widget):
        self.widgets.append(widget)

    def update(self, mouse_click, screen, command=None):
        for i in self.widgets:
            i.update(mouse_click, command)
            i.draw(screen)


class Label(pygame.sprite.Sprite):
    def __init__(self, text, xoy, size, color=DEFAULT_COLOR, centric=True):
        pygame.sprite.Sprite.__init__(self)
        text = str(text)
        self.color = color
        self.text = text
        self.size = size
        self.font = pygame.font.Font("19363.ttf", size)
        self.label = list()
        for text in self.text.split('\n'):
            self.label.append(self.font.render(text, 1, color))
        self.rect = self.label[0].get_rect(center=xoy)
        if not centric:
            self.rect.x, self.rect.y = xoy

    def new_text(self, text):
        text = str(text)
        self.label.clear()
        for text in text.split('\n'):
            self.label.append(self.font.render(text, 1, self.color))

    def draw(self, screen):
        for i in range(len(self.label)):
            screen.blit(self.label[i], (self.rect.x, self.rect.y + self.size * 1.5 * i))

    def update(self, mouse_click, command):
        pass


class BackGround(pygame.sprite.Sprite):
    def __init__(self, image, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, mouse_click, command):
        pass


