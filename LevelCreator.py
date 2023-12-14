import pickle
import pygame as pg

pg.init()

MAIN_SCREEN_WIDTH = 800
MAIN_SCREEN_HEIGHT = 800
SIDE_MENU_WIDTH = 100
SCALE = 0.5 # TODO what is this constant for? name not clear
GRID_TO_ARRAY = 100 # TODO what is this constant for? name not clear
TILES_PER_ROW = 16
TILES_PER_COLUMN = 16

TILE_WIDTH = MAIN_SCREEN_WIDTH // TILES_PER_ROW
TILE_HEIGHT = MAIN_SCREEN_HEIGHT // TILES_PER_COLUMN

screen = pg.display.set_mode((MAIN_SCREEN_WIDTH + SIDE_MENU_WIDTH, MAIN_SCREEN_HEIGHT))
picked_tile = pg.image.load(r'imgz/image1.jpeg')

tile_image_paths = ["imgz/Image1.jpeg",
                    "imgz/Image2.jpeg",
                    "imgz/Image3.jpeg",
                    "imgz/Image4.jpeg",
                    "imgz/Image5.jpeg",
                    "imgz/Image6.png",
                    "imgz/Image7.jpeg",
                    "imgz/Image8.jpeg"]
tile_images = [pg.image.load(image) for image in tile_image_paths]


def pick_image():
    if mouseX < MAIN_SCREEN_WIDTH: return

    for ind, image in enumerate(tile_images):
        if mouseY <= (ind+1) * 100:
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
        pg.draw.line(screen, pg.colordict.THECOLORS["black"], (x, 0), (x, MAIN_SCREEN_HEIGHT))

    for y in range(0, MAIN_SCREEN_HEIGHT, TILE_HEIGHT):
        pg.draw.line(screen, pg.colordict.THECOLORS["black"], (0, y), (MAIN_SCREEN_WIDTH, y))

    for index, image in enumerate(tile_images):
        screen.blit(pg.transform.scale(image, (100, 100)), (800, index * 100)) # TODO magic numbers

    if lmb:
        picked = pick_image()
        if picked:
            picked_tile = picked
        else:
            grid[mouseX // GRID_TO_ARRAY][mouseY // GRID_TO_ARRAY] = picked_tile
            screen.blit(pg.transform.scale(picked_tile, (100 * SCALE, 100 * SCALE)),
                        (100 * (mouseX // 50) * SCALE, 100 * (mouseY // 50) * SCALE)) # TODO magic numbers

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    pg.display.flip()
