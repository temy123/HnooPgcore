import pygame
import sys
from pygame.rect import Rect
from pygame.color import Color

from core.core import BaseGame, GameModel, GameComponent, KeyBindings
from core.sprite import RenderModel

from enum import Enum, auto

white = (255, 255, 255)
black = (0, 0, 0)

TILE_WIDTH = 32
TILE_HEIGHT = 16

BACKGROUND_WIDTH = 64
BACKGROUND_HEIGHT = 64


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

    def set_max_x_weight(self, x):
        self.__MAX_X_WEIGHT = x

    def set_max_y_weight(self, y):
        self.__MAX_Y_WEIGHT = y

    def get_x_weight(self):
        return self.__x_weight

    def get_y_weight(self):
        return self.__y_weight

    def add_x_weight(self, additional_value):
        self.__x_weight += additional_value
        if self.__MAX_X_WEIGHT:
            if self.__x_weight < -self.__MAX_X_WEIGHT:
                self.__x_weight = -self.__MAX_X_WEIGHT
            elif self.__x_weight > self.__MAX_X_WEIGHT:
                self.__x_weight = self.__MAX_X_WEIGHT

    def add_y_weight(self, additional_value):
        self.__y_weight += additional_value
        if self.__MAX_Y_WEIGHT:
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

    def __init__(self, sprite):
        rect = Rect(sprite.rect.left, sprite.rect.top, sprite.rect.width, sprite.rect.height)
        super().__init__(sprite, rect)
        self.set_max_x_weight(0)
        self.set_max_y_weight(0)

    def move(self):
        super().move()
        if self.get_x_weight():
            self.set_x_weight(0)
        if self.get_y_weight():
            self.set_y_weight(0)


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
        elif KeyBindings.Pressed.is_key_pressed_right():
            self.__b_leftright = True
            self.move_right()

    def bind_single_key(self, event_):
        if KeyBindings.is_current_key_down(event_, pygame.K_SPACE):
            print('key down space')
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


class TileEnum(Enum):
    TILE_GROUND = auto()
    TILE_DIRT = auto()


class BackgroundEnum(Enum):
    BACKGROUND_1 = auto()


class HnooPlatformGame(BaseGame):
    # 공용 이미지 불러오기
    __TILE_SETS = {
        TileEnum.TILE_GROUND.name: RenderModel(TILE_WIDTH, TILE_HEIGHT),
        TileEnum.TILE_DIRT.name: RenderModel(TILE_WIDTH, TILE_HEIGHT),
    }

    __BACKGROUNDS = {
        BackgroundEnum.BACKGROUND_1.name: RenderModel(TILE_WIDTH, TILE_HEIGHT),
    }

    TILE_XY = [
        'a',
        'a',
        'a',
        'a',
        'a',
        'a',
        'a',
        'a',
        'a',
        'a',
        'a',
        'a',
        'a',
        'aaaaa',
        'aaaaa000',
        '0000011100aaaa0000000000000000000000000',
        '1111111111aaaa1111111111111111111111111'
    ]

    levels = []

    def __init__(self, width, height, fps, status):
        self.width = width
        self.height = height
        super().__init__(fps, status)
        self.component = GameComponent(width, height)

        self.player = VirtualBoy()
        self.player.move_to_center(self.component)

        self.__load_tiles()  # 타일 이미지 불러오기
        self.__load_levels()  # 타일 배치 가져오기
        self.__load_background()  # 배경 이미지 불러오기

        self.add_game_model(Character.Hero.name, self.player)

    def __load_background(self):
        self.__BACKGROUNDS[BackgroundEnum.BACKGROUND_1.name] = RenderModel(BACKGROUND_WIDTH, BACKGROUND_HEIGHT).load(
            'img/platform-game/Background/Blue.png', 1, 0, 0).next_frame()

    def __load_tiles(self):
        self.__TILE_SETS[TileEnum.TILE_GROUND.name] = RenderModel(TILE_WIDTH, TILE_HEIGHT).load(
            'img/platform-game/Terrain/Terrain (16x16).png', 1, 3, 0).next_frame()

        self.__TILE_SETS[TileEnum.TILE_DIRT.name] = RenderModel(TILE_WIDTH, TILE_HEIGHT).load(
            'img/platform-game/Terrain/Terrain (16x16).png', 1, 3, 1).next_frame()

    def __load_levels(self):
        result = {'type_list': [], 'rect_list': []}
        type_list = []
        rect_list = []

        y = 0
        for line in self.TILE_XY:
            x = 0
            for piece in line:
                x += TILE_WIDTH
                type_list.append(piece)
                rect_list.append(Rect(x, y, TILE_WIDTH, TILE_HEIGHT))

            y += TILE_HEIGHT

        result['type_list'] = type_list
        result['rect_list'] = rect_list
        self.levels = result

    def __draw_tiles(self):
        for i in range(0, len(self.levels['type_list'])):
            self.__blit_tiles(self.levels['type_list'][i], self.levels['rect_list'][i])

    def __blit_tiles(self, type_, rect):
        if type_ == '0':
            self.component.blit(self.__TILE_SETS[TileEnum.TILE_GROUND.name].image, rect)
        elif type_ == '1':
            self.component.blit(self.__TILE_SETS[TileEnum.TILE_DIRT.name].image, rect)
        elif type_ == 'a':
            pass

    def apply_gravity(self):
        for model in self.model:
            model['game_model'].add_gravity()

    def move(self):
        for model in self.model:
            model['game_model'].move()

    def __draw_background(self):
        x_count = int(self.width / BACKGROUND_WIDTH)
        y_count = int(self.height / BACKGROUND_HEIGHT)

        for y in range(0, y_count):
            for x in range(0, x_count):
                self.component.blit(self.__BACKGROUNDS[BackgroundEnum.BACKGROUND_1.name].image,
                                    (x * BACKGROUND_WIDTH, y * BACKGROUND_HEIGHT))

    def _make_screen(self):
        self.apply_gravity()
        self.move()

        self.component.fill(black)
        self.__draw_background()
        self.component.show(self.get_game_model(Character.Hero.name))

        self.__draw_tiles()

        # test = self.player.rect.collidelist(self.levels['rect_list'])
        # print('collide : ' + test)

    def process_single_key_event(self, event):
        super().process_single_key_event(event)
        print('single_key_event')
        if KeyBindings.is_current_key_down(event, pygame.K_ESCAPE):
            pygame.quit()  # pygame을 종료한다
            sys.exit()  # 창을 닫는다
            self.stop()
