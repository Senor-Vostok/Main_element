import pygame
from obb.Constants import DEFAULT_COLOR


class Effect(pygame.sprite.Sprite):
    def __init__(self, xoy, animation, tracer=False, speed=15):
        pygame.sprite.Sprite.__init__(self)
        self.second_animation = 0
        self.tracer = tracer
        self.speed_animation = speed
        self.image = animation[0]
        self.effect = animation
        self.rect = self.image.get_rect(center=xoy)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move):
        self.second_animation += 1
        stadia = self.second_animation // self.speed_animation
        if stadia >= len(self.effect):
            return False
        self.image = self.effect[stadia]
        if self.tracer:
            self.rect.move_ip(move)
        return True


class Information(pygame.sprite.Sprite):
    def __init__(self, y, text, resizer=1):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('progresspixel-bold', int(30 * resizer))
        self.resizer = resizer
        self.speed_animation = 3
        self.alpha = 255
        self.image = self.font.render(text, 1, DEFAULT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.y = y + self.rect[1] // 2
        self.rect.x = -self.rect[2]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move):
        if self.rect[0] < 1920 * self.resizer:
            self.image.set_alpha(self.alpha)
            self.alpha -= 3 * bool(self.rect[0] > 0)
            self.rect.x += self.speed_animation
            return True
        return False
