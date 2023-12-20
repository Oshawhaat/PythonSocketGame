from game_object import Game_Object


class Attack(Game_Object):
    image_path: str
    radius: int
    hit_players: bool
    hit_enemies: bool

    def __init__(self, player, target_pos: tuple):
        super().__init__(self.image_path, (player.x, player.y))
        self.ignored_targets = []

    def update(self, delta_time, solid_tiles, players, enemies):
        targets = (players if self.hit_players else []) + \
                  (enemies if self.hit_enemies else [])
        hittable_targets = [target for target in targets if target not in self.ignored_targets]

        for target in hittable_targets:
            if not self.get_dist(target) < self.radius + target.rect.width: return
            self.on_hit_target()

        hittable_tiles = [tile for tile in solid_tiles if tile not in self.ignored_targets]

        for tile in hittable_tiles:
            if not self.get_dist(tile) < self.radius + tile.rect.width: return
            self.on_hit_tile()

    def on_hit_target(self):
        pass

    def on_hit_tile(self):
        pass

    def delete(self):
        del self


class Projectile(Attack):
    speed: int
    duration: int
    enemy_piercing: int
    wall_piercing: int

    def __init__(self, player, target_pos: tuple):
        super().__init__(player, target_pos)
        self.dir_x, self.dir_y = self.get_dir(target_pos)

    def update(self, solid_tiles, delta_time, target_enemy):
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
    duration: int

    def __init__(self, player, target_pos: tuple):
        super().__init__(player, target_pos)


class Melee(Attack):
    duration: int


