from game_object import Game_Object


class Tile(Game_Object):
    solid: bool
    image_path: str

    def __init__(self, pos: tuple[int, int]):
        super().__init__(self.image_path, pos)

    def __str__(self):
        return "tile"

    def dictionarify(self):
        tile_dict = super().dictionarify()
        tile_dict["solid"] = self.solid
        return tile_dict


class Test_BG(Tile):
    solid = False
    image_path = "imgs/bg.png"


class Ground(Tile):
    solid = False
    image_path = "imgs/ground.png"


class Wall(Tile):
    solid = True
    image_path = "imgs/wall.png"
