import math
import pygame as pg


class Game_Object(pg.sprite.Sprite):
    def __init__(self, image_path: str, pos: tuple[int, int]):
        self.g = pg.sprite.GroupSingle()
        super().__init__(self.g)

        self.max_health = 0
        self.health = 0
        self.defense = 0

        self.x = 0
        self.y = 0
        self.rotation = 0

        self.rect = None
        self.image = None
        self.image_path = None

        self.set_image(image_path)
        self.rect.center = pos

    def damage(self, damage):
        damage_taken = damage * (1 - self.defense)
        self.health -= damage_taken

    def dictionarify(self):
        """
        returns a dictionary representing this object
        """
        image_name = self.image_path.split('/')[1]
        rect = (*self.rect.topleft, *self.rect.size)
        obj_dict = {"image_name": image_name,
                    "rect":       rect,
                    "class":      str(self),
                    "x":          self.x,
                    "y":          self.y,
                    "max_health": self.max_health,
                    "health":     self.health}
        return obj_dict

    def set_image(self, image_path):
        self.image_path = image_path
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

    def get_dist(self, x, y, ret_tuple=False):
        """
        returns the distance from this object to the specified coordinates
        :param ret_tuple: returns the distance as a vector
        """
        x_dist = x - self.x
        y_dist = y - self.y

        if ret_tuple: return x_dist, y_dist

        dist = math.sqrt((x_dist ** 2) + (y_dist ** 2))
        return dist

    def get_dir(self, x, y):
        """
        returns the direction, the normalized vector of distance, from this object to the other
        """
        x_dist, y_dist = self.get_dist(x, y, ret_tuple=True)
        magnitude = self.get_dist(x, y)
        if not magnitude: return 0, 0
        x_norm = x_dist / magnitude
        y_norm = y_dist / magnitude
        return x_norm, y_norm

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, x, y):
        self.x = x
        self.y = y
