import os
import pickle
import pygame as pg

pg.init()

MAIN_SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SIDE_MENU_WIDTH = 100
TILES_PER_ROW = 15
TILES_PER_COLUMN = 15

tile_image_paths = [f"imgz/{image}" for image in os.listdir("imgz") if image.startswith("tile_")]
tile_images = [pg.image.load(image) for image in tile_image_paths]

path_to_image = {image:path for (image, path) in zip(tile_image_paths, tile_images)}
image_to_path = {path:image for image, path in zip(tile_image_paths, tile_images)}

side_tile_length = SCREEN_HEIGHT // len(tile_image_paths)
tile_width = MAIN_SCREEN_WIDTH // TILES_PER_ROW
tile_height = SCREEN_HEIGHT // TILES_PER_COLUMN

screen = pg.display.set_mode((MAIN_SCREEN_WIDTH + side_tile_length, SCREEN_HEIGHT))
picked_tile = path_to_image[tile_image_paths[0]]

colors = pg.color.THECOLORS


def pick_image():
    if mouseX < MAIN_SCREEN_WIDTH: return

    for ind, image in enumerate(tile_images):
        if mouseY <= (ind+1) * side_tile_length:
            return image


def save_map():
    save_num = 1
    while True:
        try:
            with open(f"map{save_num}.pkl", "xb") as file:
                pickle.dump(grid, file)

        except FileExistsError:
            save_num += 1
            continue
        break


# create grid of Nones to hold tile data
grid = [[None] * TILES_PER_COLUMN] * TILES_PER_ROW

screen.fill(colors["white"])

while True:

    keys = pg.key.get_pressed()
    mouseX, mouseY = pg.mouse.get_pos()
    lmb, rmb, mmb = pg.mouse.get_pressed(3)

    pg.draw.line(screen, colors["black"], (800, 0), (800, 800))

    for x in range(0, MAIN_SCREEN_WIDTH, tile_width):
        pg.draw.line(screen, colors["black"], (x, 0), (x, SCREEN_HEIGHT))

    for y in range(0, SCREEN_HEIGHT, tile_height):
        pg.draw.line(screen, colors["black"], (0, y), (MAIN_SCREEN_WIDTH, y))

    for index, image in enumerate(tile_images):
        scale = (side_tile_length,) * 2  # make tuple of number
        scaled_image = pg.transform.scale(image, scale)
        screen.blit(scaled_image, (MAIN_SCREEN_WIDTH, index * side_tile_length))

    if lmb:
        picked = pick_image()
        if picked:
            picked_tile = picked
        else:
            grid[mouseX // side_tile_length][mouseY // side_tile_length] = image_to_path[picked_tile]
            screen.blit(pg.transform.scale(picked_tile, (tile_width, tile_height)),
                        ((mouseX // tile_width) * tile_height, (mouseY // tile_height) * tile_height))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                save_map()

    pg.display.flip()
