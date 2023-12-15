import os
import pickle
import pygame as pg

pg.init()

MAIN_SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SIDE_MENU_WIDTH = 100
TILES_PER_ROW = 15
TILES_PER_COLUMN = 15

TILE_IMAGE_PATHS = [f"imgz/{image}" for image in os.listdir("imgz") if image.startswith("tile_")]
TILE_IMAGES = [pg.image.load(image) for image in TILE_IMAGE_PATHS]

path_to_image = {image:path for (image, path) in zip(TILE_IMAGE_PATHS, TILE_IMAGES)}
image_to_path = {path:image for image, path in zip(TILE_IMAGE_PATHS, TILE_IMAGES)}

SIDE_TILE_LENGTH = SCREEN_HEIGHT // len(TILE_IMAGE_PATHS)
TILE_WIDTH = MAIN_SCREEN_WIDTH // TILES_PER_ROW
TILE_HEIGHT = SCREEN_HEIGHT // TILES_PER_COLUMN

screen = pg.display.set_mode((MAIN_SCREEN_WIDTH + SIDE_TILE_LENGTH, SCREEN_HEIGHT))
picked_tile = path_to_image[TILE_IMAGE_PATHS[0]]


def pick_image():
    if mouseX < MAIN_SCREEN_WIDTH: return

    for ind, image in enumerate(TILE_IMAGES):
        if mouseY <= (ind+1) * SIDE_TILE_LENGTH:
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

screen.fill((255, 255, 255))

while True:

    keys = pg.key.get_pressed()
    mouseX, mouseY = pg.mouse.get_pos()
    lmb, rmb, mmb = pg.mouse.get_pressed(3)

    pg.draw.line(screen, (0, 0, 0), (800, 0), (800, 800))

    for x in range(0, MAIN_SCREEN_WIDTH, TILE_WIDTH):
        pg.draw.line(screen, pg.colordict.THECOLORS["black"], (x, 0), (x, SCREEN_HEIGHT))

    for y in range(0, SCREEN_HEIGHT, TILE_HEIGHT):
        pg.draw.line(screen, pg.colordict.THECOLORS["black"], (0, y), (MAIN_SCREEN_WIDTH, y))

    for index, image in enumerate(TILE_IMAGES):
        scale = (SIDE_TILE_LENGTH,) * 2  # make tuple of number
        scaled_image = pg.transform.scale(image, scale)
        screen.blit(scaled_image, (MAIN_SCREEN_WIDTH, index * SIDE_TILE_LENGTH))

    if lmb:
        picked = pick_image()
        if picked:
            picked_tile = picked
        else:
            grid[mouseX // SIDE_TILE_LENGTH][mouseY // SIDE_TILE_LENGTH] = image_to_path[picked_tile]
            screen.blit(pg.transform.scale(picked_tile, (TILE_WIDTH, TILE_HEIGHT)),
                        ((mouseX // TILE_WIDTH) * TILE_HEIGHT, (mouseY // TILE_HEIGHT) * TILE_HEIGHT))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                save_map()

    pg.display.flip()
