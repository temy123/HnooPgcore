import pygame  # pygame 모듈의 임포트
import sys  # 외장 모듈
from game1 import Game1
from core import GameModel, BaseGame, GameComponent, KeyBindings
from pygame.locals import *  # QUIT 등의 pygame 상수들을 로드한다.

STATUS_INTRO = -1
STATUS_MAIN_MENU = 0
STATUS_GAME_1 = 1
STATUS_GAME_2 = 2

status = STATUS_INTRO

width = 1024  # 상수 설정
height = 768
white = (255, 255, 255)
black = (0, 0, 0)
fps = 60

MY_GAME_NAME = 'PYGAME_TEST'


# 창 설정
def setup_form():
    pygame.display.set_caption(MY_GAME_NAME)


game_status = 0

if __name__ == '__main__':
    setup_form()

    pygame.init()
    game1 = Game1(width, height, fps)

    # 렌더 시작
    while True:  # 아래의 코드를 무한 반복한다.
        for event in pygame.event.get():  # 발생한 입력 event 목록의 event마다 검사
            if event.type == QUIT:  # event의 type이 QUIT에 해당할 경우
                pygame.quit()  # pygame을 종료한다
                sys.exit()  # 창을 닫는다

            # 단일 키 입력 처리
            game1.process_single_key_event(event)

        # 연속 된 키 입력 처리
        game1.process_pressed_key_event()
        game1.update()
        # print('K DOWN ' + str(pygame.key.get_pressed()[pygame.K_DOWN]))
        # KeyBindings.Pressed.print()

        # while status == STATUS_INTRO:
        #     game1.update()

        # while status == STATUS_MAIN_MENU:
        #     pass
        #
        # while status == STATUS_GAME_1:
        #     pass
        #
        # while status == STATUS_GAME_2:
        #     pass
