import pygame as pg
from game_object import Game_Object


class Enemy(Game_Object):
    image_path: str
    pos: tuple
    speed: int

    def __init__(self):
        super().__init__(self.image_path, self.pos)

