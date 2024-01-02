from game_object import Game_Object


class Attack(Game_Object):
    image_path: str
    damage: float
    radius: float
    duration: float
    hit_players: bool
    hit_enemies: bool

    def __init__(self, caster, target_pos: tuple):
        super().__init__(self.image_path, (caster.x, caster.y))
        self.ignored_tile_coords = []
        self.target_pos = target_pos
        self.remaining_duration = self.duration

    def update(self, delta_time, solid_tiles, players, enemies):
        ignored_targets = [tile for tile in solid_tiles if tile.get_pos() not in self.ignored_tile_coords]

        targets = (players if self.hit_players else []) + \
                  (enemies if self.hit_enemies else [])
        hittable_targets = [target for target in targets if target not in ignored_targets]

        for target in hittable_targets:
            if not self.get_dist(*target.get_pos()) < self.radius + target.rect.width: continue
            self.on_hit_target(target)

        hittable_tiles = [tile for tile in solid_tiles if tile not in ignored_targets]

        for tile in hittable_tiles:
            if not self.get_dist(*tile.get_pos()) < self.radius + tile.rect.width: continue
            self.on_hit_tile(tile)

        if not self.remaining_duration >= 0: return
        self.remaining_duration -= delta_time
        if self.remaining_duration <= 0: self.delete()

    def on_hit_target(self, target):
        target.damage(self.damage)

    def on_hit_tile(self, tile):
        pass

    def on_delete(self):
        pass

    def delete(self):
        self.on_delete()
        del self


class Projectile_Attack(Attack):
    speed: int
    enemy_piercing: int
    wall_piercing: int

    def __init__(self, caster, target_pos: tuple):
        super().__init__(caster, target_pos)
        self.dir_x, self.dir_y = self.get_dir(*target_pos)

    def update(self, delta_time, solid_tiles, players, enemies):
        super().update(delta_time, solid_tiles, players, enemies)
        self.x += self.dir_x * self.speed * delta_time
        self.y += self.dir_y * self.speed * delta_time

    def on_hit_target(self, target):
        if self.enemy_piercing == 0:
            self.delete()
        self.enemy_piercing -= 1

    def on_hit_tile(self, tile):
        if self.wall_piercing == 0:
            self.delete()
        self.wall_piercing -= 1


class AOE_Attack(Attack):
    expand_time: float

    def __init__(self, caster, target_pos: tuple):
        super().__init__(caster, target_pos)
        self.max_radius = self.radius
        self.radius = 0
        self.expand_time_remaining = self.expand_time

    def update(self, delta_time, solid_tiles, players, enemies):
        super().update(delta_time, solid_tiles, players, enemies)
        self.expand_time_remaining -= delta_time
        percent_expanded = self.expand_time_remaining / self.expand_time
        self.radius = percent_expanded * self.radius


class Melee_Attack(Attack):
    swing_angle: int

    def __init__(self, caster, target_pos: tuple):
        super().__init__(caster, target_pos)
        self.caster = caster

    def update(self, delta_time, solid_tiles, players, enemies):
        super().update(delta_time, solid_tiles, players, enemies)
        self.rotation = self.swing_angle * (self.remaining_duration / self.duration)
        self.set_pos(*self.caster.get_pos())
