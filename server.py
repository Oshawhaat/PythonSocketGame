import os
import pickle
import socket
import tile
import pygame as pg
import random as rnd
from player import Player
from _thread import start_new_thread

# server = "127.0.0.1"
server = "10.234.7.127"
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Server started, awaiting connections")

# remove invisible .DS_Store file that does not seem to be able to be removed
image_paths = ["imgs/" + image_name for image_name in os.listdir("imgs") if image_name != ".DS_Store"]
player_image_paths = [image for image in image_paths if image.split("/")[1].startswith("player")]
print(f"found {len(image_paths)} images:\n", image_paths)
print(f"found {len(player_image_paths)} player images:\n", player_image_paths)

players = pg.sprite.Group()
tiles = pg.sprite.Group()
clock = pg.time.Clock()

tile = tile.Test_BG((0, 0))
tiles.add(tile)


class My_Exception(Exception):
    pass


def check_if_request(data, images, image_names, conn):
    try:
        reply = data.decode()
        if not reply: raise My_Exception(f"Reply was empty ({reply})")
        if not reply[0] == 'r': raise My_Exception(f'Reply did not start with "r" ({reply})')
        print(reply)

        match reply[1]:
            case "i":
                image_index = int(reply[2:])
                conn.send(images[image_index])
                return True
            case "n":
                name_index = int(reply[2:])
                conn.send(image_names[name_index].encode())
                return True

        raise My_Exception("Could not process request!")

    except UnicodeDecodeError:
        return False

    except My_Exception as exception:
        print(exception)
        return False


def threaded_client(conn):
    player_pos = 400, 400
    player_image = "imgs/loading.png"
    print("creating new player with default image:", player_image)

    player_id = len(players.sprites())
    client_player = Player(player_image, player_pos, player_id)

    conn.send(pickle.dumps((len(image_paths), player_id)))
    images = []
    image_names = []
    for file_path in image_paths:
        file_name = file_path.split('/')[1]
        with open(file_path, "rb") as file:
            images.append(file.read())
            image_names.append(file_name)

    players.add(client_player)
    try:
        while True:
            _data = conn.recv(4096)

            if check_if_request(_data, images, image_names, conn): continue

            if not _data: break

            key, data = pickle.loads(_data)

            match key:
                case "info":
                    client_player.username, image_path = data
                    if image_path: client_player.set_image(image_path)
                    print(data)

                case "keys":
                    client_player.keys = data

            players_list = [player.dictionarify() for player in players.sprites() if player.player_id != player_id]
            tiles_list = [tile.dictionarify() for tile in tiles.sprites()]

            conn.send(pickle.dumps([client_player.dictionarify()] + players_list + tiles_list))
    except ConnectionResetError:
        pass
    print("Disconnected")
    players.remove(client_player)


def threaded_game():
    while True:
        delta_time = clock.tick(60) / 1000
        players.update(delta_time)


start_new_thread(threaded_game, ())
while True:
    connection, address = s.accept()
    print("Connected to:", address)

    start_new_thread(threaded_client, (connection,))
