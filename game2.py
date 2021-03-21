import pygame
import sys
from pygame.color import Color
from core.core import BaseGame, GameModel, GameComponent, KeyBindings
from core.sprite import RenderModel

white = (255, 255, 255)
black = (0, 0, 0)

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
    'aaaaa111aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1',
    'aaaaa000aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0',
    'aaaaa000aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0',
    'aaaaa000aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0',
    '0000011100aaaa0000000000000000000000000',
    '1111111111aaaa1111111111111111111111111'
]

tiles = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()


# TODO: ThisGameModel 이름 변경 필요,
class GameTwoModel(GameModel):
    def move_to_center(self, component: GameComponent):
        self.sprite_rect.center = component.get_center()


class Tile(RenderModel):
    WIDTH = 16
    HEIGHT = 16

    def __init__(self, x, y):
        super().__init__(self.WIDTH, self.HEIGHT)
        self.x = x
        self.y = y
        self.load('img/platform-game/Terrain/Terrain (16x16).png', 1, 6, 0, Color(0, 0, 0))
        self.rect.x = self.WIDTH * x
        self.rect.y = self.HEIGHT * y


class VirtualBoy(RenderModel):
    WIDTH = 32
    HEIGHT = 32

    def __init__(self):
        super().__init__(self.WIDTH, self.HEIGHT)
        self.load('img/platform-game/Main Characters/Virtual Guy/Idle (32x32).png', 11, 0, 0, Color(0, 0, 0))

    def move(self):
        if KeyBindings.Pressed.is_key_pressed_left():
            self.rect.move_ip(-3, 0)
        elif KeyBindings.Pressed.is_key_pressed_right():
            self.rect.move_ip(3, 0)
        if KeyBindings.Pressed.is_key_pressed_up():
            self.rect.move_ip(0, -3)
        elif KeyBindings.Pressed.is_key_pressed_down():
            self.rect.move_ip(0, 3)


class Game2(BaseGame):
    TILESIZE = 32

    def __init__(self, width, height, fps, status):
        self.width = width
        self.height = height
        super().__init__(fps, status)
        self.background = pygame.display.set_mode((self.width, self.height))
        self.component = GameComponent(width, height)
        self.player = VirtualBoy()

        for i in range(0, 50):
            tiles.add(Tile(i, 0))

    def draw_grid(self):
        # 0부터 TILESIZE씩 건너뛰면서 WIDTH까지 라인을 그려준다
        for x in range(0, self.width, self.TILESIZE):
            # 첫번째 인자부터 game_world(게임 화면)에 (0,0,0,50)의 색으로 차례대로 라인을 그려준다
            pygame.draw.line(self.background, (0, 0, 0, 50), (x, 0), (x, self.width))
        for y in range(0, self.height, self.TILESIZE):
            pygame.draw.line(self.background, (0, 0, 0, 50), (0, y), (self.width, y))

    def _make_screen(self):
        self.component.fill(white)
        self.draw_grid()
        self.player.move()
        tiles.draw(self.background)
        self.component.blit(self.player.next_frame(), self.player.rect)

    def process_single_key_event(self, event):
        super().process_single_key_event(event)
        if KeyBindings.is_key_type_down(event):
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                self.stop()
