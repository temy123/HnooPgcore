import pygame
from core import BaseGame, GameModel, GameComponent, KeyBindings

white = (255, 255, 255)
black = (0, 0, 0)


# TODO: ThisGameModel 이름 변경 필요,
class ThisGameModel(GameModel):
    def move_to_center(self, component: GameComponent):
        self.rect.center = component.get_center()


class HelloWorldModel(ThisGameModel):

    def __init__(self):
        gulim_font = pygame.font.SysFont('굴림', 70)  # 서체 설정
        render_text = gulim_font.render('Hello, world!', 1, black)

        # .render() 함수에 내용과 안티앨리어싱, 색을 전달하여 글자 이미지 생성
        # render_rect = render_text.get_rect()  # 생성한 이미지의 rect 객체를 가져온다
        # render_rect.center = (width / 2, height / 2)  # 해당 rect의 중앙을 화면 중앙에 맞춘다
        super().__init__(render_text)


class ToadKing(ThisGameModel):

    def __init__(self):
        self.sprite = pygame.image.load('img/character/1 Toad_king/Calm.png')
        self.rect = self.sprite.get_rect()
        super().__init__(self.sprite, self.rect)

    def move_down(self):
        self.rect.move_ip(0, 5)

    def move_up(self):
        self.rect.move_ip(0, -5)

    def move_left(self):
        self.rect.move_ip(-5, 0)

    def move_right(self):
        self.rect.move_ip(-5, 0)

    def move_to_center(self, component: GameComponent):
        self.rect.center = component.get_center()

    def process_key(self, event_):
        if KeyBindings.is_key_press_down(event_):
            if KeyBindings.is_key_up(event_):
                self.move_up()
            if KeyBindings.is_key_down(event_):
                self.move_down()


class Game1(BaseGame):

    def __init__(self, width, height, fps):
        super().__init__(fps)
        self.component = GameComponent(width, height)

        self.add_game_model('hello', HelloWorldModel())
        self.add_game_model('boss1', ToadKing())

    def _make_screen(self):
        self.component.fill(white)
        self.component.show(self.get_game_model('boss1'))