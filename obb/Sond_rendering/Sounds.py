import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(10)


class Sounds:
    def __init__(self):
        self.loaded_sound = dict()
        self.click = self.__load_sound(f'data/sounds/click.mp3')
        self.draw = self.__load_sound(f'data/sounds/draw.mp3')
        self.menu = self.__load_sound(f'data/sounds/menu.mp3')
        self.place = self.__load_sound(f'data/sounds/place.mp3')
        self.delete = self.__load_sound(f'data/sounds/delete.mp3')
        self.background = [self.__load_sound(f'data/sounds/mus{i}.mp3') for i in range(1, 5)]

    def __load_sound(self, file):
        if file not in self.loaded_sound:
            self.loaded_sound[file] = pygame.mixer.Sound(file)
        return self.loaded_sound[file]
