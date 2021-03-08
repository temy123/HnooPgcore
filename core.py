import pygame
import sys

from abc import abstractmethod

from pygame.locals import *


class KeyBindings:
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
    def is_key_press_up(event_):
        return event_.type == pygame.KEYUP

    @staticmethod
    def is_key_press_down(event_):
        return event_.type == pygame.KEYDOWN


class GameModel:

    def __init__(self, render_model=None, render_rect=pygame.Rect(0, 0, 0, 0)):
        self.model = render_model
        self.rect = render_rect

    def process_key(self, event_):
        pass


class BaseGame:
    model = []

    def __init__(self, fps):
        self.fps = fps
        self.__clock = pygame.time.Clock()

    # 시간 설정
    def clock(self):
        self.__clock.tick(self.fps)

    def update(self):
        for event in pygame.event.get():  # 발생한 입력 event 목록의 event마다 검사
            if event.type == QUIT:  # event의 type이 QUIT에 해당할 경우
                pygame.quit()  # pygame을 종료한다
                sys.exit()  # 창을 닫는다

            # KEY 이벤트 작동
            self._process_key(event)

        # 화면 만들기
        self._make_screen()

        # pygame 을 통해 화면을 업데이트한다
        pygame.display.update()

        # 화면 표시 회수 설정만큼 루프의 간격을 둔다
        self.clock()

    @abstractmethod
    def _make_screen(self):
        pass

    def _process_key(self, event):
        for model in self.model:
            model['game_model'].process_key(event)

    def add_game_model(self, key_, game_model):
        self.model.append({'key': key_, 'game_model': game_model})

    def get_game_model(self, key_):
        return next((item for item in self.model if item['key'] == key_), None)['game_model']

    def process_key(self):
        for model in self.model:
            model.process_key()


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
