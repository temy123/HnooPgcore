import pygame
import sys

from abc import abstractmethod

from pygame.locals import *
from core.sprite import RenderModel


class Print:
    @staticmethod
    def print_rect(name, rect):
        print('-- {name} ____ top {top}, bottom {bottom}, left {left}, right {right}, x {x}, y{y} : '.format(
            name=name,
            top=rect.top, bottom=rect.bottom,
            left=rect.left, right=rect.right,
            x=rect.x, y=rect.y))


class KeyBindings:
    class Pressed:
        @staticmethod
        def is_key_pressed_current(key_):
            return pygame.key.get_pressed()[key_]

        @staticmethod
        def is_key_pressed_space():
            return pygame.key.get_pressed()[pygame.K_SPACE]

        @staticmethod
        def is_key_pressed_left():
            return pygame.key.get_pressed()[pygame.K_LEFT]

        @staticmethod
        def is_key_pressed_right():
            return pygame.key.get_pressed()[pygame.K_RIGHT]

        @staticmethod
        def is_key_pressed_up():
            return pygame.key.get_pressed()[pygame.K_UP]

        @staticmethod
        def is_key_pressed_down():
            return pygame.key.get_pressed()[pygame.K_DOWN]

        @staticmethod
        def print():
            print('get_pressed(): ' + str(pygame.key.get_pressed()))

    @staticmethod
    def is_key_left(event_):
        return event_.key == pygame.K_LEFT

    @staticmethod
    def is_key_right(event_):
        return event_.key == pygame.K_RIGHT

    @staticmethod
    def is_key_up(event_):
        return event_.key == pygame.K_UP

    @staticmethod
    def is_key_down(event_):
        return event_.key == pygame.K_DOWN

    @staticmethod
    def is_key_type_up(event_):
        return event_.type == pygame.KEYUP

    @staticmethod
    def is_key_type_down(event_):
        return event_.type == pygame.KEYDOWN

    @staticmethod
    def is_current_key_down(event_, key_code):
        return event_.type == pygame.KEYDOWN and event_.key == key_code


class GameModel:

    def __init__(self, sprite_model=None, sprite_rect=pygame.Rect(0, 0, 0, 0)):
        # ??????????????? RenderModel ??? ???????????? ?????? ??????
        self.sprite = sprite_model
        self.sprite_rect = sprite_rect

    def bind_single_key(self, event_):
        pass

    def bind_pressed_key(self):
        pass

    def unload(self):
        self.sprite = None
        self.sprite_rect = None


class BaseGame:
    __running = False

    def __init__(self, fps, status):
        self.fps = fps
        self.__clock = pygame.time.Clock()
        self.start()
        self.status = status
        self.model = []

    def start(self):
        self.__running = True

    def stop(self):
        self.__running = False
        # for model in self.model:
        #     model['key'] = None
        #     if model['game_model']:
        #         model['game_model'].unload()
        # model['game_model'] = None
        # del model

    def is_running(self):
        return self.__running

    def get_status(self):
        return self.status

    # ?????? ??????
    def clock(self):
        self.__clock.tick(self.fps)

    def update(self):
        # ?????? ??? ??? ?????? ??????
        for event in pygame.event.get():
            self.process_single_key_event(event)

        # ?????? ??? ??? ?????? ??????
        self.process_pressed_key_event()

        # ??????????????? ??????
        self._blit_sprites()

        # ?????? ?????????
        self._make_screen()

        # pygame ??? ?????? ????????? ??????????????????
        pygame.display.update()

        # ?????? ?????? ?????? ???????????? ????????? ????????? ??????
        self.clock()

    @abstractmethod
    def _make_screen(self):
        pass

    # ?????? ???????????? ?????? ??????????????? ????????? ?????? ?????? ???
    # HnooPygame ??? sprite.RenderModel ??? ???????????? ?????? ???
    def _blit_sprites(self):
        for model in self.model:
            if type(model['game_model'].sprite) == RenderModel:
                model['game_model'].sprite.next_frame()

    def process_single_key_event(self, event):
        for model in self.model:
            model['game_model'].bind_single_key(event)

    def process_pressed_key_event(self):
        for model in self.model:
            model['game_model'].bind_pressed_key()

    def add_game_model(self, key_, game_model):
        self.model.append({'key': key_, 'game_model': game_model})

    def get_game_model(self, key_):
        return next((item for item in self.model if item['key'] == key_), None)['game_model']


class GameComponent:
    def __init__(self, width, height):
        # ?????? ?????????????????? ????????????
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((width, height), 0, 32)

    def fill(self, color):
        self.display.fill(color)  # displaysurf??? ??????????????? ?????????

    # ???????????? ?????? ????????? ????????? ???????????? ?????? ??????
    def show(self, model: GameModel):
        if type(model.sprite) == RenderModel:
            self.display.blit(model.sprite.image, model.sprite_rect)

        else:
            self.display.blit(model.sprite, model.sprite_rect)

    # ???????????? ?????? ????????? ????????? ???????????? ?????? ??????
    def blit(self, sprite, rect):
        self.display.blit(sprite, rect)

    def get_center(self):
        return self.width / 2, self.height / 2
