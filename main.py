import pygame  # pygame 모듈의 임포트
import sys  # 외장 모듈
from pygame.locals import *  # QUIT 등의 pygame 상수들을 로드한다.

width = 1024  # 상수 설정
height = 768
white = (255, 255, 255)
black = (0, 0, 0)
fps = 60

MY_GAME_NAME = 'PYGAME_TEST'


class GameModel:

    def __init__(self, render_model=None, render_rect=None):
        self.model = render_model
        self.rect = render_rect

    def _get_center(self):
        return width / 2, height / 2


class HelloWorldModel(GameModel):

    def __init__(self):
        gulim_font = pygame.font.SysFont('굴림', 70)  # 서체 설정
        render_text = gulim_font.render('Hello, world!', 1, black)

        # .render() 함수에 내용과 안티앨리어싱, 색을 전달하여 글자 이미지 생성
        render_rect = render_text.get_rect()  # 생성한 이미지의 rect 객체를 가져온다
        render_rect.center = (width / 2, height / 2)  # 해당 rect의 중앙을 화면 중앙에 맞춘다
        super().__init__(render_text, render_rect)


class ToadKing(GameModel):
    def __init__(self):
        self.sprite = pygame.image.load('img/character/1 Toad_king/Calm.png')
        self.rect = self.sprite.get_rect()
        self.rect.center = self._get_center()
        super().__init__(self.sprite, self.rect)

    def move_down(self):
        self.rect.bottom += 5

    def move_up(self):
        self.rect.bottom -= 5


class GameComponent:
    def __init__(self):
        # 메인 디스플레이를 설정한다
        self.display = pygame.display.set_mode((width, height), 0, 32)
        self.__clock = pygame.time.Clock()

    def fill(self, color):
        self.display.fill(color)  # displaysurf를 하얀색으로 채운다

    def show(self, model: GameModel):
        self.display.blit(model.model, model.rect)

    # 시간 설정
    def clock(self):
        self.__clock.tick(fps)


# 창 설정
def setup_form():
    pygame.display.set_caption(MY_GAME_NAME)


if __name__ == '__main__':
    setup_form()

    pygame.init()
    game = GameComponent()

    # 렌더 시작
    while True:  # 아래의 코드를 무한 반복한다.
        text_model = HelloWorldModel()
        image_model = ToadKing()

        for event in pygame.event.get():  # 발생한 입력 event 목록의 event마다 검사
            if event.type == QUIT:  # event의 type이 QUIT에 해당할 경우
                pygame.quit()  # pygame을 종료한다
                sys.exit()  # 창을 닫는다

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    image_model.move_down()
                elif event.key == pygame.K_UP:
                    image_model.move_up()

        game.fill(white)
        game.show(image_model)

        pygame.display.update()  # 화면을 업데이트한다
        game.clock()  # 화면 표시 회수 설정만큼 루프의 간격을 둔다
