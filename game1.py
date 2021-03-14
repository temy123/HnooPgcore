import pygame
from pygame.color import Color

from core.core import BaseGame, GameModel, GameComponent, KeyBindings
from core.sprite import RenderModel

from enum import Enum, auto

white = (255, 255, 255)
black = (0, 0, 0)


# TODO: ThisGameModel 이름 변경 필요,
class ThisGameModel(GameModel):
    def move_to_center(self, component: GameComponent):
        self.sprite_rect.center = component.get_center()


class VirtualBoy(ThisGameModel):

    def __init__(self):
        self.sprite = RenderModel(32, 32)
        self.sprite.load('img/platform-game/Main Characters/Virtual Guy/Idle (32x32).png', 11, Color(0, 0, 0))
        self.rect = self.sprite.rect
        super().__init__(self.sprite, self.rect)

    def move_down(self):
        self.rect.move_ip(0, 5)

    def move_up(self):
        self.rect.move_ip(0, -5)

    def move_left(self):
        self.rect.move_ip(-5, 0)

    def move_right(self):
        self.rect.move_ip(5, 0)

    def move_to_center(self, component: GameComponent):
        self.rect.center = component.get_center()

    def bind_pressed_key(self):
        if KeyBindings.Pressed.is_key_pressed_up():
            self.move_up()
        if KeyBindings.Pressed.is_key_pressed_down():
            self.move_down()
        if KeyBindings.Pressed.is_key_pressed_left():
            self.move_left()
        if KeyBindings.Pressed.is_key_pressed_right():
            self.move_right()


class Character(Enum):
    Hero = auto()


class HnooPlatformGame(BaseGame):

    def __init__(self, width, height, fps, status):
        super().__init__(fps, status)
        self.component = GameComponent(width, height)

        player = VirtualBoy()
        player.move_to_center(self.component)

        self.add_game_model(Character.Hero.name, player)

    def _make_screen(self):
        self.component.fill(white)
        self.component.show(self.get_game_model(Character.Hero.name))

    def process_single_key_event(self, event):
        super().process_single_key_event(event)
        if KeyBindings.is_key_type_down(event):
            if event.key == pygame.K_ESCAPE:
                self.stop()
