import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.func = None
        self.args = None
        self.rect = self.image.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def connect(self, func, *args):
        self.func = func
        self.args = args

    def update(self, there, command=None):
        if self.rect.colliderect(there[0], there[1], 1, 1) and there[2] and there[3] == 1 and self.func:
            self.func(self.args) if self.args else self.func()


class InteractLabel(pygame.sprite.Sprite):
    def __init__(self, image, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.text = "_"
        # self.font.render(self.text, False, (99, 73, 47))
        self.rect = self.image.get_rect(center=xoy)
        self.font = pygame.font.SysFont("Futura book C", self.rect[3] + self.rect[3] // 4)
        self.can_write = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        image = self.font.render(self.text, False, (99, 73, 47))
        i = 1
        while image.get_rect()[2] > self.rect[2] - 5:
            image = self.font.render("." + self.text[i:], False, (99, 73, 47))
            i += 1
        screen.blit(image, (self.rect.x + 2, self.rect.y + 2))

    def update(self, there, command=None):
        if not self.rect.colliderect(there[0], there[1], 1, 1) and there[2] and there[3] == 1:
            self.can_write = False
        elif self.rect.colliderect(there[0], there[1], 1, 1) and there[2] and there[3] == 1:
            self.can_write = True
        elif self.can_write:
            self.go_write(command)

    def go_write(self, command):
        if command:
            if command.key == pygame.K_BACKSPACE:
                self.text = self.text[:-2] + "_"
            elif len(command.unicode) > 0:
                self.text = self.text[:-1] + command.unicode + "_"


class Surface:
    def __init__(self, *args):
        self.widgets = list()
        for i in args:
            self.widgets.append(i)

    def update(self, there, screen, command=None):
        for i in self.widgets:
            i.update(there, command)
            i.draw(screen)


class Label(pygame.sprite.Sprite):
    def __init__(self, text, xoy, size):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pygame.font.SysFont("Futura book C", size)
        self.label = self.font.render(self.text, 1, (99, 73, 47))
        self.rect = self.label.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.label, (self.rect.x, self.rect.y))

    def update(self, there, command):
        pass


class BackGround(pygame.sprite.Sprite):
    def __init__(self, image, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, there, command):
        pass
