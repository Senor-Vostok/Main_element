import pygame


class Effect(pygame.sprite.Sprite):
    def __init__(self, xoy, animation, more_main=False):
        pygame.sprite.Sprite.__init__(self)

        self.second_animation = 0
        self.speed_animation = 15
        self.mm = more_main

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
