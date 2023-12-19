from game_object import Game_Object


class Enemy(Game_Object):
    image_path: str
    speed: int
    aggro_range: int

    def __init__(self, pos):
        super().__init__(self.image_path, pos)
        self.curr_target = None

    def __str__(self):
        return "enemy"

    def update(self, delta_time, players):
        self.curr_target = self.get_nearest_player(players, self.aggro_range)
        if not self.curr_target: return

        dir_x, dir_y = self.get_dir(self.curr_target)
        self.x += dir_x * self.speed * delta_time
        self.y += dir_y * self.speed * delta_time

    def get_nearest_player(self, players, aggro_range):
        nearest_player = None
        nearest_dist = aggro_range

        player_dists = [self.get_dist(player) for player in players]

        for player, dist in zip(players, player_dists):
            if nearest_dist < dist: continue
            nearest_player = player
            nearest_dist = dist

        return nearest_player


class Test_Enemy(Enemy):
    image_path = "imgs/enemy.png"
    speed = 100
    aggro_range = 400
