import os
import pickle
import pygame as pg

pg.init()

MAIN_SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SIDE_MENU_WIDTH = 100
GRID_TO_ARRAY = 100 # TODO what is this constant for? name not clear
TILES_PER_ROW = 16
TILES_PER_COLUMN = 16

TILE_IMAGE_PATHS = [image for image in os.listdir("imgz") if image.startswith("tile_")]
SIDE_TILE_HEIGHT = SCREEN_HEIGHT // len(TILE_IMAGE_PATHS)
TILE_WIDTH = MAIN_SCREEN_WIDTH // TILES_PER_ROW
TILE_HEIGHT = SCREEN_HEIGHT // TILES_PER_COLUMN

screen = pg.display.set_mode((MAIN_SCREEN_WIDTH + SIDE_TILE_HEIGHT, SCREEN_HEIGHT))
picked_tile = pg.image.load(r'imgz/image1.jpeg')

tile_images = [pg.image.load(image) for image in TILE_IMAGE_PATHS]


def pick_image():
    if mouseX < MAIN_SCREEN_WIDTH: return

    for ind, image in enumerate(tile_images):
        if mouseY <= (ind+1) * 100: # TODO magic number
            return image


# --- Create grid of numbers
# Create an empty list
grid = []
# Loop for each row
for row in range(TILES_PER_COLUMN):
    # For each row, create a list that will
    # represent an entire row
    grid.append([])
    # Loop for each column
    for column in range(TILES_PER_ROW):
        # Add a None object to the current row
        grid[row].append(None)

screen.fill((255, 255, 255))

while True:

    mouseX, mouseY = pg.mouse.get_pos()
    lmb, rmb, mmb = pg.mouse.get_pressed(3)

    pg.draw.line(screen, (0, 0, 0), (800, 0), (800, 800))

    for x in range(0, MAIN_SCREEN_WIDTH, TILE_WIDTH):
        pg.draw.line(screen, pg.colordict.THECOLORS["black"], (x, 0), (x, SCREEN_HEIGHT))

    for y in range(0, SCREEN_HEIGHT, TILE_HEIGHT):
        pg.draw.line(screen, pg.colordict.THECOLORS["black"], (0, y), (MAIN_SCREEN_WIDTH, y))

    for index, image in enumerate(tile_images):
        scale = (SIDE_TILE_HEIGHT,) * 2 # make tuple of number
        scaled_image = pg.transform.scale(image, scale)
        screen.blit(scaled_image, (MAIN_SCREEN_WIDTH, index * GRID_TO_ARRAY))

    if lmb:
        picked = pick_image()
        if picked:
            picked_tile = picked
        else:
            grid[mouseX // GRID_TO_ARRAY][mouseY // GRID_TO_ARRAY] = picked_tile
            screen.blit(pg.transform.scale(picked_tile, (TILE_WIDTH, TILE_HEIGHT)),
                        ((mouseX // TILE_WIDTH) * TILE_HEIGHT, (mouseY // TILE_HEIGHT) * TILE_HEIGHT))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    pg.display.flip()
