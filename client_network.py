import pickle
import socket
import glob
import os
import pygame as pg
import random as rnd

pg.init()

screen_width = 800
screen_height = 800
screen = pg.display.set_mode((screen_width, screen_height))


class Player(pg.sprite.Sprite):
    def __init__(self, image_name, rect, health, username, group):
        super().__init__(group)
        self.image_name = image_name
        self.rect = rect
        self.health = health
        self.username = username

        self.image = pg.image.load(f"imgz/{image_name}")


class Network:
    def __init__(self):
        self.client = socket.socket()
        self.server = "10.234.5.138" # "127.0.0.1"
        self.port = 9999
        self.address = (self.server, self.port)
        num_images, self.id = self.connect()
        print(self.id)

        try: os.mkdir("imgz")
        except FileExistsError: pass

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
            print(f"{ind+1}:", img)
        try:
            image_ind = int(input("Enter the index of the image you want: ")) - 1

            if image_ind < 0:
                image_ind = rnd.randint(0, len(available_images)-1)

            image = "imgz/" + available_images[image_ind]

        except ValueError:
            print("That is not a valid number! try again: ")

    return username, image


def get_keys():
    used_keys = [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_SPACE, pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT]
    pressed_keys = pg.key.get_pressed()
    return { key:pressed_keys[key] for key in used_keys }


def redraw_screen(players):
    screen.fill((255, 255, 255))
    if players:
        player_group = pg.sprite.Group()
        for player_stats in players:
            Player(*player_stats, player_group)
        player_group.draw(screen)

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
