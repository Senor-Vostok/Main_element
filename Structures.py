import pygame
import Textures


class ClassicStructure(pygame.sprite.Sprite):
    def __init__(self, image, xoy, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.name = name
        self.animation = Textures.animations_structures[name]
        self.rect = self.image.get_rect(center=xoy)

        self.second_animation = 0
        self.speed_animation = 15

    def start_animation(self):
        self.second_animation += 1
        stadia = self.second_animation // self.speed_animation
        if stadia >= len(self.animation):
            self.second_animation = 0
            stadia = 0
        self.image = self.animation[stadia]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move, y_n):
        self.start_animation()
        if y_n:
            self.rect.x += move[0]
            self.rect.y += move[1]
