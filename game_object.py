import pygame as pg


class Game_Object(pg.sprite.Sprite):
    def __init__(self, image_path: str, pos: tuple[int, int]):
        self.g = pg.sprite.GroupSingle()
        super().__init__(self.g)
        self.health = -1
        self.rect = None
        self.image = None
        self.image_path = None
        self.set_image(image_path)
        self.rect.center = pos

    def ready_pickle(self):
        image_path = self.image_path
        rect = (*self.rect.topleft, *self.rect.size)
        return image_path, rect, self.health

    def set_image(self, image_path):
        self.image_path = image_path
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()

