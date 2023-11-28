import pygame as pg


class Game_Object(pg.sprite.Sprite):
    def __init__(self, image: str, pos: tuple[int, int]):
        self.g = pg.sprite.GroupSingle()
        super().__init__(self.g)
        self.image_path = image
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.health = -1

    def ready_pickle(self):
        image_path = self.image_path
        rect = (*self.rect.topleft, *self.rect.size)
        return image_path, rect, self.health

