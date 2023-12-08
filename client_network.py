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
        if not obj_class: return sprites
        for sprite in sprites:
            if type(sprite) == obj_class:
                yield sprite

    def draw_names(self):
        pass


class Game_Object(pg.sprite.Sprite):
    def __init__(self, obj_dict, group):
        super().__init__(group) if group else super().__init__()
        self.rect = pg.Rect(*obj_dict["rect"])
        self.image = pg.image.load(f"imgz/{obj_dict['image_name']}")
        if obj_dict["health"]:
            self.health = obj_dict["health"]


class Player(Game_Object):
    def __init__(self, player_dict: dict, group: Game_Object_Group):
        super().__init__(player_dict, group)
        self.username = player_dict["username"]

    def draw_name(self):
        text = font.render(self.username, True, pg.color.THECOLORS["blue"])
        text_rect = text.get_rect()
        text_rect.midbottom = self.rect.centerx, self.rect.top + PLAYER_NAME_OFFSET
        screen.blit(text, text_rect)


class Network:
    def __init__(self):
        self.client = socket.socket()
        self.server = "10.234.12.66"  # "127.0.0.1"
        self.port = 9999
        self.address = (self.server, self.port)
        try:
            num_images, self.id = self.connect()
        except OSError as error:
            print(f"\n*********************************\n"
                  f"Could not connect to server\n"
                  f"{error}\n"
                  f"*********************************")
            exit()
        print(self.id)

        try:
            os.mkdir("imgz")
        except FileExistsError:
            pass

        for file in glob.glob("imgz/*.*"):
            os.remove(file)

        for x in range(num_images):
            self.client.send(str.encode(f"ri{x}"))
            image = self.client.recv(4096000)
            self.client.send(str.encode(f"rn{x}"))
            image_name = self.client.recv(4096).decode()
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
    available_images = os.listdir("imgz")
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
    if objects:

        object_group = Game_Object_Group()

        for obj_dict in objects:
            match obj_dict["class"]:
                case "player":
                    Player(obj_dict, group=object_group)
                case "tile":
                    pass  # TODO make tile class

        object_group.draw(screen)

        for player in object_group.sprites(Player):
            player.draw_name()

    pg.display.update()


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


main()
