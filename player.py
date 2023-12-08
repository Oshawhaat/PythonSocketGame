import pygame as pg
import numpy as np
from game_object import Game_Object


class Player(Game_Object):
    def __init__(self, image_path, pos):
        super().__init__(image_path, pos)
        self.speed = 300  # pixels/second
        self.keys = {}
        self.username = ""

    def update(self, delta_time: float, solid_tile_rects: list = []):
        if not self.keys: return

        w = max(self.keys[pg.K_w], self.keys[pg.K_UP])
        a = max(self.keys[pg.K_a], self.keys[pg.K_LEFT])
        s = max(self.keys[pg.K_s], self.keys[pg.K_DOWN])
        d = max(self.keys[pg.K_d], self.keys[pg.K_RIGHT])

        offset_x = d - a
        offset_y = s - w

        divisor = np.sqrt(np.square(offset_x) + np.square(offset_y))
        if not divisor: return

        norm_x = offset_x / divisor
        norm_y = offset_y / divisor

        move_x = norm_x * self.speed * delta_time
        move_y = norm_y * self.speed * delta_time

        try:
            self.x += move_x
            assert not self.rect.collidelist(solid_tile_rects)
        except AssertionError:
            self.x -= move_x

        try:
            self.x += move_y
            assert not self.rect.collidelist(solid_tile_rects)
        except AssertionError:
            self.y -= move_y

    def dictionarify(self):
        player_dict = super().dictionarify()
        player_dict["class"] = "player"
        player_dict["username"] = self.username
        return player_dict
