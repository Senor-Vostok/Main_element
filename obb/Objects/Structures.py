import pygame


class ClassicStructure(pygame.sprite.Sprite):
    def __init__(self, image, xoy, name, textures):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.name = name
        try:
            self.animation = textures.animations_structures[name]
        except:
            pass
        self.rect = self.image.get_rect(center=xoy)

        self.second_animation = 0
        self.speed_animation = 15

    def __start_animation(self):
        self.second_animation += 1
        stadia = self.second_animation // self.speed_animation
        if stadia >= len(self.animation):
            self.second_animation = 0
            stadia = 0
        self.image = self.animation[stadia]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move, y_n):
        self.__start_animation()
        if y_n:
            self.rect.x += move[0]
            self.rect.y += move[1]


class CenterStructure(ClassicStructure):
    pass


class MainStructure(ClassicStructure):
    def __init__(self, image, xoy, name, textures):
        ClassicStructure.__init__(self, image, xoy, name, textures)
        self.animation = textures.animations_main_structures[name]