import pygame as pg


class Game_Object(pg.sprite.Sprite):
    def __init__(self, image_path: str, pos: tuple[int, int]):
        self.g = pg.sprite.GroupSingle()
        super().__init__(self.g)

        self.max_health = 0
        self.health = 0

        self.x = 0
        self.y = 0
        self.rect = None
        self.image = None
        self.image_path = None

        self.set_image(image_path)
        self.rect.center = pos

    def dictionarify(self):
        image_name = self.image_path.split('/')[1]
        rect = (*self.rect.topleft, *self.rect.size)
        obj_dict = {"image_name": image_name,
                       "rect": rect,
                       "class": str(self),
                       "x": self.x,
                       "y": self.y,
                       "max_health": self.max_health,
                       "health": self.health}
        return obj_dict

    def set_image(self, image_path):
        self.image_path = image_path
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
