from obb.Constants import UPDATE_LIMIT
from obb.Constants import DEFAULT_COLOR
from obb.Image_rendering.Efffect import Effect
import pygame.display
import itertools


def update_effects(self):
    if self.camera.mouse_click[2] and int(self.camera.mouse_click[3]) == 1:
        if not self.pressed:
            self.pressed = True
            self.effects.append(Effect((self.camera.mouse_click[0], self.camera.mouse_click[1]), self.textures.effects['mouse1']))
    else:
        self.pressed = False
    for i in self.effects:
        i.draw(self.screen)
        if not i.update():
            self.effects.remove(i)


def rendering(handler, machine):
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
            sprite.update(machine.synchronous, camera_move, flag and not handler.open_some)
            sprite.draw(machine.win, mouse_click, machine.handler)

        machine.synchronous = machine.synchronous + 1 if machine.synchronous < UPDATE_LIMIT else 0

    c = handler.click_handler()
    if handler.screen_world:
        handler.machine()

    try:
        for interface in handler.interfaces.values():
            interface.surface.update(handler.camera.mouse_click, handler.screen, c)
    except Exception as e:
        pass
    update_effects(handler)
    point_pos = (handler.camera.mouse_click[0] - 10, handler.camera.mouse_click[1] - 10)
    handler.screen.blit(handler.textures.point, point_pos)
    fps_text = handler.textures.font.render(f'fps: {int(handler.clock.get_fps())}', False, DEFAULT_COLOR)
    handler.screen.blit(fps_text, (30, 30))
    pygame.display.flip()
