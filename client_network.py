import pickle
import socket
import glob
import os
import pygame as pg
import random as rnd

pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
PLAYER_FONT_SIZE = 12
PLAYER_NAME_OFFSET = 5

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pg.font.Font(pg.font.get_default_font(), PLAYER_FONT_SIZE)


class Game_Object_Group(pg.sprite.Group):
    def sprites(self, obj_class: type = None, tag=None):
        sprites = super().sprites()
        if not obj_class:
            return sprites
        return [sprite for sprite in sprites if type(sprite) == obj_class]

    def draw_names(self):
        pass


class Game_Object(pg.sprite.Sprite):
    def __init__(self, obj_dict, group):
        super().__init__(group)
        self.rect = pg.Rect(*obj_dict["rect"])
        self.x = obj_dict["x"]
        self.y = obj_dict["y"]
        self.rect.x += SCREEN_WIDTH / 2
        self.rect.y += SCREEN_HEIGHT / 2
        self.image = pg.image.load(f"imgz/{obj_dict['image_name']}")
        if obj_dict["health"]:
            self.health = obj_dict["health"]


class Player(Game_Object):
    def __init__(self, player_dict: dict, group: Game_Object_Group, main_player=False):
        super().__init__(player_dict, group)
        self.username = player_dict["username"]
        self.main_player = main_player

    def draw_name(self):
        text = font.render(self.username, True, pg.color.THECOLORS["red"])
        text_rect = text.get_rect()
        text_rect.midbottom = self.rect.centerx, self.rect.top + PLAYER_NAME_OFFSET
        screen.blit(text, text_rect)


class Tile(Game_Object):
    def __init__(self, tile_dict: dict, group: pg.sprite.Group):
        super().__init__(tile_dict, group)
        self.solid = tile_dict["solid"]


class Network:
    def __init__(self):
        self.client = socket.socket()
        # self.server = "127.0.0.1"
        self.server = "10.234.12.200"
        self.port = 9999
        self.address = (self.server, self.port)
        try:
            num_images, self.id = self.connect()
        except OSError as error:
            print(f"\n*********************************\n"
                  f"Could not connect to server\n"
                  f"{error}\n"
                  f"*********************************")
            pg.quit()
            quit()
        print(f"player id: {self.id}")

        try:
            os.mkdir("imgz")
        except FileExistsError:
            pass

        for file in glob.glob("imgz/*.*"):
            os.remove(file)

        for x in range(num_images):
            self.client.send(f"ri{x}".encode('latin-1'))
            image = self.client.recv(4096000)
            self.client.send(f"rn{x}".encode('latin-1'))
            image_name = self.client.recv(4096).decode('latin-1')
            with open(f"imgz/{image_name}", "xb") as file:
                file.write(image)

    def connect(self):
        self.client.connect(self.address)
        ret = pickle.loads(self.client.recv(4096))
        print("Connected to server!")
        return ret

    def send(self, data):
        self.client.send(pickle.dumps(data))
        return pickle.loads(self.client.recv(4096))


def get_player_info():
    available_images = [img for img in os.listdir("imgz") if img.startswith("player_")]
    username = input("Enter a Username: ")
    image = None

    while image is None:
        print("Here are the available images:")
        print("(enter 0 for random)")
        for ind, img in enumerate(available_images):
            print(f"{ind + 1}:", img)
        try:
            image_ind = int(input("Enter the index of the image you want: ")) - 1

            if image_ind < 0:
                image_ind = rnd.randint(0, len(available_images) - 1)

            image = "imgz/" + available_images[image_ind]

        except ValueError:
            print("That is not a valid number! try again: ")

    print("The game is ready, open the window")

    return username, image


def get_keys():
    used_keys = [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT, pg.K_SPACE, pg.KMOD_SHIFT]
    pressed_keys = pg.key.get_pressed()
    key_dict = {key: pressed_keys[key] for key in used_keys}
    key_dict["mb1"], key_dict["mb2"], key_dict["mb3"] = pg.mouse.get_pressed(num_buttons=3)
    key_dict["mpos"] = pg.mouse.get_pos()
    return key_dict


def redraw_screen(objects):
    screen.fill((255, 255, 255))
    if not objects:
        return

    object_group = Game_Object_Group()
    player_group = Game_Object_Group()

    main_player = Player(objects[0], group=player_group, main_player=True)
    for obj_dict in objects[1:]:
        if obj_dict["class"] == "player":
            Player(obj_dict, group=player_group)
        if obj_dict["class"] == "tile":
            Tile(obj_dict, group=object_group)

    for obj in object_group.sprites() + \
            [p for p in player_group.sprites() if not p.main_player]:
        obj.rect.x -= main_player.x
        obj.rect.y -= main_player.y
    object_group.draw(screen)
    player_group.draw(screen)

    for player in player_group:
        player.draw_name()


def main():
    running = True
    clock = pg.time.Clock()
    network = Network()
    network.send(("info", get_player_info()))

    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        redraw_screen(network.send(("keys", get_keys())))
        pg.display.update()


if __name__ == "__main__":
    main()
