import obb.Objects.Structures
from obb.Constants import UPDATE_LIMIT
from obb.Constants import DEFAULT_COLOR
from obb.Image_rendering.Efffect import Effect, Information
import pygame.display
import itertools


def update_effects(self):
    if self.camera.mouse_click[2] and int(self.camera.mouse_click[3]) == obb.Constants.MOUSE_CLICK_LEFT:
        if not self.pressed:
            self.pressed = True
            self.effects.append(
                Effect((self.camera.mouse_click[0], self.camera.mouse_click[1]), self.textures.effects['mouse1']))
    else:
        self.pressed = False
    for i in [_ for _ in self.effects if isinstance(_, Effect)]:
        i.draw(self.screen)
        if not i.update(self.camera.move):
            self.effects.remove(i)
    for i in [_ for _ in self.effects if isinstance(_, Information)]:
        i.draw(self.screen)
        if not i.update(self.camera.move):
            self.effects.remove(i)
        break


def update_resource_effects(self):
    for i in self.effects_disappearance_resource:
        i.draw(self.screen)
        there = self.interfaces['ingame'].resource_ico.rect
        if i.update(self.camera.move, (there[0], there[1])):
            self.effects_disappearance_resource.remove(i)


def update_titles(handler):
    r = handler.textures.resizer
    if 'ingame' in handler.interfaces:
        handler.interfaces['ingame'].count_resource.new_text(str(handler.me.resources))
    handler.screen.blit(handler.version, (10 * r, 10 * r))
    handler.screen.blit(handler.uid, (10 * r, 40 * r))


def rendering(handler, machine):
    title_main_structures = list()
    if machine and machine.rendering:
        camera_move = handler.camera.move
        mouse_click = handler.camera.mouse_click
        flag = machine.check_barrier(camera_move, machine.centre)
        if flag and not handler.open_some:
            machine.now_dr[0] = machine.great_world[0][0].rect[0]
            machine.now_dr[1] = machine.great_world[0][0].rect[1]
            machine.move_scene()
        elif not flag:
            camera_move[0] *= -1
            camera_move[1] *= -1
        for sprite in itertools.chain.from_iterable(machine.great_world):
            if 'ingame' in handler.interfaces and handler.interfaces['ingame'].state_game.active and isinstance(sprite.structure, obb.Objects.Structures.MainStructure):
                rect = sprite.rect
                title_main_structures.append([rect[0] + rect[2] // 2, rect[1] - rect[3] // 2, handler.info_players[[i[2] for i in handler.info_players].index(sprite.biome[4])][0]])
            sprite.update(machine.synchronous, camera_move, flag and not handler.open_some)
            sprite.draw(machine.win, mouse_click, machine.handler)
        machine.synchronous = machine.synchronous + 1 if machine.synchronous < UPDATE_LIMIT else 0
    for title in title_main_structures:
        image = handler.textures.font.render(f'{title[2]}', False, (0, 0, 0))
        handler.screen.blit(image, (title[0] - image.get_rect()[2] // 2, title[1]))
    c = handler.click_handler()
    if handler.screen_world:
        handler.machine()
    update_resource_effects(handler)
    if None not in handler.selected_cell:
        dr = handler.screen_world.now_dr
        cord = handler.screen_world.world_coord
        size = handler.textures.land['barrier'][0].get_rect()[2]
        y1, x1 = dr[1] + (int(handler.selected_cell[0][2]) - cord[0]) * size, dr[0] + (int(handler.selected_cell[0][3]) - cord[1]) * size
        y2, x2 = dr[1] + (int(handler.selected_cell[1][2]) - cord[0]) * size, dr[0] + (int(handler.selected_cell[1][3]) - cord[1]) * size
        pygame.draw.line(handler.screen, (212, 112, 78), (x1 + size / 2, y1 + size / 2), (x2 + size / 2, y2 + size / 2), 5)
    for selected_cell in handler.selected_cells:
        dr = handler.screen_world.now_dr
        cord = handler.screen_world.world_coord
        size = handler.textures.land['barrier'][0].get_rect()[2]
        y1, x1 = dr[1] + (int(selected_cell[0][2]) - cord[0]) * size, dr[0] + (int(selected_cell[0][3]) - cord[1]) * size
        y2, x2 = dr[1] + (int(selected_cell[1][2]) - cord[0]) * size, dr[0] + (int(selected_cell[1][3]) - cord[1]) * size
        pygame.draw.line(handler.screen, (190, 152, 118), (x1 + size / 2, y1 + size / 2), (x2 + size / 2, y2 + size / 2), 5)
    try:
        for interface in handler.interfaces.values():
            interface.surface.update(handler.camera.mouse_click, handler.screen, c)
            handler.last_interface = interface
    except Exception:
        pass
    update_effects(handler)
    point_pos = (handler.camera.mouse_click[0] - 10, handler.camera.mouse_click[1] - 10)
    handler.screen.blit(handler.textures.point, point_pos)
    update_titles(handler)
    pygame.display.flip()
