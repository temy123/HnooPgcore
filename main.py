import pygame  # pygame 모듈의 임포트
import sys  # 외장 모듈
from game1 import HnooPlatformGame
from game2 import Game2
from game3 import Game3
from game4 import Game4
from core.core import GameModel, BaseGame, GameComponent, KeyBindings
from pygame.locals import *  # QUIT 등의 pygame 상수들을 로드한다.

I_INTRO = -1
I_MAIN_MENU = 0
I_GAME_1 = 1
I_GAME_2 = 2

status = I_GAME_1

width = 1024  # 상수 설정
height = 768
white = (255, 255, 255)
black = (0, 0, 0)
fps = 60

MY_GAME_NAME = 'PYGAME_TEST'


# 창 설정
def setup_form():
    pygame.display.set_caption(MY_GAME_NAME)


def is_game_running(game_object: BaseGame):
    return game_object.is_running()


def handle_global_keys():
    global status
    for event in pygame.event.get():  # 발생한 입력 event 목록의 event마다 검사
        if event.type == QUIT:  # event의 type이 QUIT에 해당할 경우
            pygame.quit()  # pygame을 종료한다
            sys.exit()  # 창을 닫는다

        if KeyBindings.is_key_type_down(event):
            status = I_GAME_1 if event.key == pygame.K_1 else status
            status = I_GAME_2 if event.key == pygame.K_2 else status
            status = I_INTRO if event.key == pygame.K_3 else status
            status = I_MAIN_MENU if event.key == pygame.K_4 else status
            # print('status to {status}'.format(status=status))


def select_game():
    global status, GAMES
    return GAMES[status]


def stop_games():
    global GAMES
    for game in GAMES.values():
        game.stop()


GAMES = {
    I_INTRO: None,
    I_MAIN_MENU: None,
    I_GAME_1: None,
    I_GAME_2: None,
}

if __name__ == '__main__':
    setup_form()

    pygame.init()

    # 렌더 시작
    while True:  # 아래의 코드를 무한 반복한다.
        # print('1. INIT NEW GAME')

        GAMES[I_GAME_1] = HnooPlatformGame(width, height, fps, I_GAME_1)
        GAMES[I_GAME_2] = Game2(width, height, fps, I_GAME_2)
        GAMES[I_INTRO] = Game3(width, height, fps, I_INTRO)
        GAMES[I_MAIN_MENU] = Game4(width, height, fps, I_MAIN_MENU)

        running_game = select_game()
        running_game.start()
        # print('2. ================ selected game : ' + str(status))

        while status == running_game.get_status():
            running_game.update()

            # 게임이 끝난 경우 에는 메인메뉴로
            # status = I_MAIN_MENU if is_game_running(running_game) else status

            # handle_global_keys()

            # print('4. equals status {result}'.format(result=status == running_game.get_status()))

        if not is_game_running(running_game):
            break

        stop_games()
