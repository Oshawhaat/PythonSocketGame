from game_object import Game_Object


class Attack(Game_Object):
    image_path: str

    def __init__(self, player, target_pos: tuple):
        super().__init__(self.image_path, (player.x, player.y))

    def update(self, delta_time, target_enemy):
        pass

    def on_hit_enemy(self):
        pass

    def on_hit_wall(self):
        pass

    def delete(self):
        del self


class Projectile(Attack):
    speed: int
    radius: int
    duration: int
    enemy_piercing: int
    wall_piercing: int

    def __init__(self, player, target_pos: tuple):
        super().__init__(player, target_pos)
        self.dir_x, self.dir_y = self.get_dir(target_pos)

    def update(self, delta_time, target_enemy):
        self.x += self.dir_x * self.speed * delta_time
        self.y += self.dir_y * self.speed * delta_time

    def on_hit_enemy(self):
        if self.enemy_piercing == 0:
            self.delete()
        self.enemy_piercing -= 1

    def on_hit_wall(self):
        if self.wall_piercing == 0:
            self.delete()
        self.wall_piercing -= 1


class AOE(Attack):
    radius: int
    duration: int

    def __init__(self, player, target_pos: tuple):
        super().__init__(player, target_pos)


class Melee(Attack):
    radius: int
    duration: int


