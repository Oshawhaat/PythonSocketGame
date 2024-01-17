import pygame as pg
import numpy as np
from game_object import Game_Object


class Player(Game_Object):
    def __init__(self, image_path, pos, player_id):
        super().__init__(image_path, pos)
        self.speed = 300  # pixels/second
        self.keys = {}
        self.cooldowns = {"water": 0}
        self.username = ""
        self.player_id = player_id

    def __str__(self):
        return "player"

    def update(self, delta_time: float, solid_tile_rects: list):
        for key in self.cooldowns.keys():
            cooldown = self.cooldowns[key]
            if cooldown:
                self.cooldowns[key] = max(0, cooldown - delta_time)

        if not self.keys: return

        w = max(self.keys[pg.K_w], self.keys[pg.K_UP])
        a = max(self.keys[pg.K_a], self.keys[pg.K_LEFT])
        s = max(self.keys[pg.K_s], self.keys[pg.K_DOWN])
        d = max(self.keys[pg.K_d], self.keys[pg.K_RIGHT])

        offset_x = d - a
        offset_y = s - w

        magnitude = np.sqrt(np.square(offset_x) + np.square(offset_y))
        if not magnitude: return

        norm_x = offset_x / magnitude
        norm_y = offset_y / magnitude

        move_x = norm_x * self.speed * delta_time
        move_y = norm_y * self.speed * delta_time

        try:
            self.x += move_x
            if solid_tile_rects is not None:
                for tile in solid_tile_rects:
                    assert not self.rect.colliderect(tile)
        except AssertionError:
            self.x -= move_x

        try:
            self.y += move_y
            if solid_tile_rects is not None:
                for tile in solid_tile_rects:
                    assert not self.rect.colliderect(tile)
        except AssertionError:
            self.y -= move_y

    def dictionarify(self):
        player_dict = super().dictionarify()
        player_dict["username"] = self.username
        player_dict["cooldowns"] = self.cooldowns
        return player_dict

    def on_screen(self, other):
        """
        returns true if other is on the screen of this player
        """
        x_dist, y_dist = self.get_dist(*other.get_pos(), ret_tuple=True)
        abs_x_dist = abs(x_dist) - other.rect.width / 2
        abs_y_dist = abs(y_dist) - other.rect.height / 2
        return abs(abs_x_dist) <= 400 and abs(abs_y_dist) <= 400
