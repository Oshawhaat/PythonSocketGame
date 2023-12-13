import pickle
import pygame as pg

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
SCALE = 0.5 # TODO what is this constant for? name not clear
GRID_TO_ARRAY = 100 # TODO what is this constant for? name not clear
TILES_PER_ROW = 10
TILES_PER_COLUMN = 10

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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


def pick_image(mouseX, mouseY):  # TODO so many magic number
    if mouseX < 800: return

    # TODO this must be compactable
    if mouseY <= 100:
        tilePicked = tile_images[0]
    if 100 < mouseY <= 200:
        tilePicked = tile_images[1]
    if 200 < mouseY <= 300:
        tilePicked = tile_images[2]
    if 300 < mouseY <= 400:
        tilePicked = tile_images[3]
    if 400 < mouseY <= 500:
        tilePicked = tile_images[4]
    if 500 < mouseY <= 600:
        tilePicked = tile_images[5]
    if 600 < mouseY <= 700:
        tilePicked = tile_images[6]
    if mouseY >= 700:
        tilePicked = tile_images[7]
    return tilePicked


# --- Create grid of numbers
# Create an empty list
grid = []
# Loop for each row
for row in range(TILES_PER_COLUMN):  # TODO magic number
    # For each row, create a list that will
    # represent an entire row
    grid.append([])
    # Loop for each column
    for column in range(TILES_PER_ROW):  # TODO magic number
        # Add a number zero to the current row
        grid[row].append(0)

screen.fill((255, 255, 255))

while True:

    mouseX, mouseY = pg.mouse.get_pos()
    lmb, rmb, mmb = pg.mouse.get_pressed(3)

    pg.draw.line(screen, (0, 0, 0), (800, 0), (800, 800))

    i = 0
    while i < 8 / SCALE + 1:  # TODO an iterating while loop is the same as a for loop #TODO magic number
        i += 1
        pg.draw.line(screen, (0, 0, 0), (i * SCALE * 100, 0), (i * SCALE * 100, 800))  # TODO magic number

    im = 0
    while im < 8 / SCALE + 1:  # TODO an iterating while loop is the same as a for loop # TODO magic number
        im += 1
        pg.draw.line(screen, (0, 0, 0), (0, im * SCALE * 100), (800, im * SCALE * 100))  # TODO magic numbers

    for index, image in enumerate(tile_images):
        screen.blit(pg.transform.scale(pg.image.load(image), (100, 100)), (800, index * 100)) # TODO magic numbers

    if lmb:
        picked = pick_image(mouseX, mouseY)
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
