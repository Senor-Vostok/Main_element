import Player
from Structures import *
from Interfaces import *
import pygame

label_choice = None


def place_structure(gr, structure_name='mill'):
    gr.biom[1] = structure_name
    gr.structure = ClassicStructure(gr.textures.animations_structures[structure_name][0],
                                    (gr.rect[0] + gr.rect[2] // 2, gr.rect[1] + gr.rect[3] // 2), structure_name,
                                    gr.textures)


def remove_structure(gr):
    gr.biom[1] = 'null'
    gr.structure = None
    gr.image = gr.tile_image


def check_ground_info(gr, screen):
    gr.my_font = pygame.font.SysFont('Futura book C', 30)
    # units_cnt = gr.my_font.render(str(gr.units_count), False, (0, 0, 0))
    biome_name = gr.my_font.render(str(gr.name), False, (0, 0, 0))
    if gr.structure:
        # screen.blit(units_cnt, (gr.structure.rect.x + 50, gr.structure.rect.y + 80))
        screen.blit(biome_name, (gr.structure.rect.x + 50, gr.structure.rect.y + 95))
    else:
        # screen.blit(units_cnt, (gr.rect.x + 20, gr.rect.y + 25))
        screen.blit(biome_name, (gr.rect.x + 20, gr.rect.y + 40))


def check_event(gr, there, screen):  # event_id - какое действие пришло обработчику (изменить структуру/поселение и тд)
    global label_choice
    if there[3] == 1:  # лкм
        pass  # убрать интерфейс
    elif there[3] == 3:  # пкм
        if not label_choice:
            label_choice = PopupMenu((gr.rect[0] + gr.rect[2] // 2, gr.rect[1] + gr.rect[3] // 2))
        # do_name, *args = Окно из интерфейса
        # запихиваем интерфейс в label_choice
        # checker(do_name, *args)
    if label_choice:
        label_choice.display.update(there, screen)


# label_choice.update(btn, screen)


def checker(player, gr, action_name, *args): #args: (название_постройки, стоимость, список_разрешенных_биомов)
    if action_name == 'build':
        # Можем ли мы позволить себе постройку если да то строй
        if (player.action_pts >= args[1]) and (gr.name in gr.biome_permissions[args[0]]):
            place_structure(gr, args[0])
        else:
            # говорим, что невозможно построить
            pass
