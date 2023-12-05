from game_object import Game_Object
from dataclasses import dataclass


@dataclass
class Tile(Game_Object):
    solid: bool
    image_path: str

    def __init__(self, image_path: str, pos: tuple[int, int]):
        super().__init__(image_path, pos)


class Ground(Tile):
    solid = False
    image_path = "imgs/ground.png"


class Wall(Tile):
    solid = True
    image_path = "imgs/wall.png"
