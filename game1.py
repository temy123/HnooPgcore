import pygame
from pygame.color import Color

from core.core import BaseGame, GameModel, GameComponent, KeyBindings
from core.sprite import RenderModel

from enum import Enum, auto

white = (255, 255, 255)
black = (0, 0, 0)


# class HnooPlatformerSprites:
#     class Tile:


# TODO: ThisGameModel 이름 변경 필요,
class ThisGameModel(GameModel):
    __MAX_X_WEIGHT = 8
    __MAX_Y_WEIGHT = 13
    __GRAVITY_WEIGHT = 0.5

    def __init__(self, sprite_model=None, sprite_rect=pygame.Rect(0, 0, 0, 0)):
        super().__init__(sprite_model, sprite_rect)
        self.__b_gravity = False
        # 4방향 가중치
        self.__x_weight = 0
        self.__y_weight = 0

    def move(self):
        self.sprite_rect.move_ip(self.__x_weight, self.__y_weight)

    def get_x_weight(self):
        return self.__x_weight

    def get_y_weight(self):
        return self.__y_weight

    def add_x_weight(self, additional_value):
        self.__x_weight += additional_value
        if self.__x_weight < -self.__MAX_X_WEIGHT:
            self.__x_weight = -self.__MAX_X_WEIGHT
        elif self.__x_weight > self.__MAX_X_WEIGHT:
            self.__x_weight = self.__MAX_X_WEIGHT

    def add_y_weight(self, additional_value):
        self.__y_weight += additional_value
        self.__y_weight = min(self.__y_weight, self.__MAX_Y_WEIGHT)

    def set_x_weight(self, x):
        self.__x_weight = x

    def set_y_weight(self, y):
        self.__y_weight = y

    def add_gravity(self):
        if self.__b_gravity:
            self.__y_weight += self.__GRAVITY_WEIGHT

    def set_gravity(self, on_):
        self.__b_gravity = on_

    def move_to_center(self, component: GameComponent):
        self.sprite_rect.center = component.get_center()


class TileSprites(ThisGameModel):

    def __init__(self):
        default_tile = RenderModel(32, 32)
        default_tile.load('img/platform-game/Terrain/Terrain (16x16).png',
                          1,
                          3, 0)

        super().__init__(default_tile, default_tile.rect)


class VirtualBoy(ThisGameModel):
    __X_ADDITIONAL_VALUE = 0.5
    __Y_ADDITIONAL_VALUE = 1
    __b_leftright = False

    def __init__(self):
        self.sprite = RenderModel(32, 32)
        self.sprite.load('img/platform-game/Main Characters/Virtual Guy/Idle (32x32).png', 11, 0, 0, Color(0, 0, 0))
        self.rect = self.sprite.rect
        super().__init__(self.sprite, self.rect)
        self.set_gravity(True)

    def move_left(self):
        self.add_x_weight(-self.__X_ADDITIONAL_VALUE)

    def move_right(self):
        self.add_x_weight(self.__X_ADDITIONAL_VALUE)

    def move_to_center(self, component: GameComponent):
        self.rect.center = component.get_center()

    def bind_pressed_key(self):
        self.__b_leftright = False
        if KeyBindings.Pressed.is_key_pressed_left():
            self.__b_leftright = True
            self.move_left()
        if KeyBindings.Pressed.is_key_pressed_right():
            self.__b_leftright = True
            self.move_right()
        if KeyBindings.Pressed.is_key_pressed_space():
            self.set_y_weight(-10)

    def move(self):
        if not self.__b_leftright:
            if self.get_x_weight() < 0:
                self.add_x_weight(self.__X_ADDITIONAL_VALUE)
            elif self.get_x_weight() > 0:
                self.add_x_weight(-self.__X_ADDITIONAL_VALUE)

        super().move()


class Character(Enum):
    Hero = auto()
    Tile_1 = auto()


class HnooPlatformGame(BaseGame):

    def __init__(self, width, height, fps, status):
        super().__init__(fps, status)
        self.component = GameComponent(width, height)

        player = VirtualBoy()
        player.move_to_center(self.component)

        tile = TileSprites()
        tile.move_to_center(self.component)

        self.add_game_model(Character.Hero.name, player)
        self.add_game_model(Character.Tile_1.name, tile)

    def apply_gravity(self):
        for model in self.model:
            model['game_model'].add_gravity()

    def move(self):
        for model in self.model:
            model['game_model'].move()

    def _make_screen(self):
        self.apply_gravity()
        self.move()

        self.component.fill(black)
        self.component.show(self.get_game_model(Character.Hero.name))
        self.component.show(self.get_game_model(Character.Tile_1.name))

    def process_single_key_event(self, event):
        super().process_single_key_event(event)
        if KeyBindings.is_key_type_down(event):
            if event.key == pygame.K_ESCAPE:
                self.stop()
