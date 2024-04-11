import pygame
from obb.Constants import DEFAULT_COLOR


class Effect(pygame.sprite.Sprite):
    def __init__(self, xoy, animation):
        pygame.sprite.Sprite.__init__(self)
        self.second_animation = 0
        self.speed_animation = 15
        self.image = animation[0]
        self.effect = animation
        self.rect = self.image.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.second_animation += 1
        stadia = self.second_animation // self.speed_animation + 1
        if stadia >= len(self.effect):
            return False
        self.image = self.effect[stadia]
        return True


class Information(pygame.sprite.Sprite):
    def __init__(self, y, text, resizer=1):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('progresspixel-bold', int(30 * resizer))
        self.resizer = resizer
        self.speed_animation = 3
        self.image = self.font.render(text, 1, DEFAULT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.y = y + self.rect[1] // 2
        self.rect.x = -self.rect[2]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.rect[0] < 1920 * self.resizer:
            self.rect.x += self.speed_animation
            return True
        return False
