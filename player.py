import pygame as pg
import numpy as np
from game_object import Game_Object


class Player(Game_Object):
    def __init__(self, image_path, pos):
        super().__init__(image_path, pos)
        self.speed = 300  # pixels/second
        self.keys = None

    def update(self, delta_time):
        if not self.keys: return

        off_x = self.keys[pg.K_d] - self.keys[pg.K_a]
        off_y = self.keys[pg.K_s] - self.keys[pg.K_w]

        divisor = np.sqrt(np.square(off_x) + np.square(off_y))
        if not divisor: return

        norm_x = off_x / divisor
        norm_y = off_y / divisor

        self.rect.x += norm_x * self.speed * delta_time
        self.rect.y += norm_y * self.speed * delta_time

        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > 800: self.rect.bottom = 800

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 800: self.rect.right = 800
