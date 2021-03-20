import pygame
from pygame.sprite import AbstractGroup
from pygame.surface import Surface


class RenderModel(pygame.sprite.Sprite):

    def __init__(self, crop_width_, crop_height_):
        pygame.sprite.Sprite.__init__(self)
        # 스프라이트 모음집
        self.sprite_sheet = None
        # 스프라이트 배열
        self.images = []
        # 한개의 스프라이트의 가로 세로 크기
        self.crop_width = crop_width_
        self.crop_height = crop_height_
        # 스프라이트의 총 갯수
        self.total_number = 0
        # 현재 보여지고 있는 이미지의 인덱스 값
        self.current_frame = 0
        self.self_timer = 0

        # 스프라이트 내에 자를 이미지의 시작 위치
        self.column_x = 0
        self.column_y = 0

    def load(self, path, total_number_, column_x_index=0, column_y_index=0, color_key=None):
        self.total_number = total_number_
        self.sprite_sheet = pygame.image.load(path).convert_alpha()
        self.column_x = column_x_index * self.crop_width
        self.column_y = column_y_index * self.crop_height

        self.image = Surface((self.crop_width, self.crop_height))
        if color_key:
            self.image.set_colorkey(color_key)

        self.rect = self.image.get_rect()
        return self

    def get_current_rect(self):
        return (self.column_x + (self.crop_width * self.current_frame),
                self.column_y,
                self.crop_width, self.crop_height)

    # 애니메이션이 가능한 Sprite 이미지의 경우 프레임 단위로 다음 이미지 표시
    def next_frame(self):
        if self.current_frame == self.total_number - 1:
            self.current_frame = 0
        else:
            self.current_frame += 1

        self.image.blit(self.sprite_sheet, (0, 0), self.get_current_rect())
        return self

    # 애니메이션 시작 콜백
    def on_animation_start(self):
        pass

    # 애니메이션 끝났을 때 콜백
    def on_animation_stopped(self):
        pass

    # 애니메이션 다음 프레임으로 넘어가기 전에 콜백
    def on_animation_ready_to_next_frame(self, current_frame):
        pass
