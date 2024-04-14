import pygame
from obb.Constants import DEFAULT_COLOR


class Button(pygame.sprite.Sprite):
    def __init__(self, image, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.state = image[0]
        self.trigger = image[1]
        self.image = self.state
        self.func = None
        self.args = None
        self.rect = self.image.get_rect(center=xoy)
        self.one_press = True

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, mouse_click, command=None):
        if self.rect.colliderect(mouse_click[0], mouse_click[1], 1, 1):
            self.image = self.trigger
            if mouse_click[2] and mouse_click[3] == 1 and self.func:
                if self.one_press:
                    self.one_press = False
                    if len(self.args) == 0:
                        return self.func()
                    elif len(self.args) == 1:
                        return self.func(self.args[0])
                    elif len(self.args) == 2:
                        return self.func(self.args[0], self.args[1])
                    elif len(self.args) == 3:
                        return self.func(self.args[0], self.args[1], self.args[2])
                    elif len(self.args) == 4:
                        return self.func(self.args[0], self.args[1], self.args[2], self.args[3])
                    elif len(self.args) == 5:
                        return self.func(self.args[0], self.args[1], self.args[2], self.args[3], self.args[4])
                    elif len(self.args) == 6:
                        return self.func(self.args[0], self.args[1], self.args[2], self.args[3], self.args[4], self.args[5])
            else:
                self.one_press = True
        else:
            self.image = self.state


class InteractLabel(pygame.sprite.Sprite):
    def __init__(self, image, xoy, active=True):
        pygame.sprite.Sprite.__init__(self)
        self.state = image[0]
        self.flex = image[1]
        self.image = self.state
        self.text = "/"
        self.func = None
        self.args = None
        self.active = active
        self.rect = self.image.get_rect(center=xoy)
        self.font = pygame.font.SysFont("progresspixel-bold", self.rect[3] - self.rect[3] // 3)
        self.can_write = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        image = self.font.render(self.text[-1:], False, DEFAULT_COLOR)
        i = 1
        while image.get_rect()[2] < self.rect[2] - 50 and i <= len(self.text):
            image = self.font.render(self.text[-i:], False, DEFAULT_COLOR)
            i += 1
        screen.blit(image, (self.rect[0] + 10, self.rect[1] + 6))

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
            elif int(command.key) == 13:
                if self.func:
                    if len(self.args) == 0:
                        return self.func()
                    elif len(self.args) == 1:
                        return self.func(self.args[0])
                    elif len(self.args) == 2:
                        return self.func(self.args[0], self.args[1])
                    elif len(self.args) == 3:
                        return self.func(self.args[0], self.args[1], self.args[2])
                    elif len(self.args) == 4:
                        return self.func(self.args[0], self.args[1], self.args[2], self.args[3])
                    elif len(self.args) == 5:
                        return self.func(self.args[0], self.args[1], self.args[2], self.args[3], self.args[4])
                    elif len(self.args) == 6:
                        return self.func(self.args[0], self.args[1], self.args[2], self.args[3], self.args[4], self.args[5])
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
    def __init__(self, text, xoy, size, color=DEFAULT_COLOR):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont("progresspixel-bold", size)
        self.label = self.font.render(self.text, 1, color)
        self.rect = self.label.get_rect(center=xoy)

    def new_text(self, text):
        self.text = text
        self.label = self.font.render(text, 1, self.color)

    def draw(self, screen):
        screen.blit(self.label, (self.rect.x, self.rect.y))

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


