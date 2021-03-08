import pygame
import sys

from abc import abstractmethod

from pygame.locals import *


class KeyBindings:
    class Pressed:
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


class GameModel:

    def __init__(self, render_model=None, render_rect=pygame.Rect(0, 0, 0, 0)):
        self.model = render_model
        self.rect = render_rect

    def bind_single_key(self, event_):
        pass

    def bind_pressed_key(self):
        pass

    def unload(self):
        self.model = None
        self.rect = None


class BaseGame:
    __running = False
    model = []

    def __init__(self, fps, status):
        self.fps = fps
        self.__clock = pygame.time.Clock()
        self.start()
        self.status = status

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

    # 시간 설정
    def clock(self):
        self.__clock.tick(self.fps)

    def update(self):
        # 단일 된 키 입력 처리
        for event in pygame.event.get():
            self.process_single_key_event(event)

        # 연속 된 키 입력 처리
        self.process_pressed_key_event()

        # 화면 만들기
        self._make_screen()

        # pygame 을 통해 화면을 업데이트한다
        pygame.display.update()

        # 화면 표시 회수 설정만큼 루프의 간격을 둔다
        self.clock()

    @abstractmethod
    def _make_screen(self):
        pass

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
        # 메인 디스플레이를 설정한다
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((width, height), 0, 32)

    def fill(self, color):
        self.display.fill(color)  # displaysurf를 하얀색으로 채운다

    def show(self, model: GameModel):
        self.display.blit(model.model, model.rect)

    def get_center(self):
        return self.width / 2, self.height / 2
