import pickle
import pygame as pg

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
SCALE = 0.5
GRID_TO_ARRAY = 100

AMOGUS = pg.image.load(r'imgz/amogus.png')

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tilePicked = pg.image.load(r'imgz/image1.jpeg')

tile_images = ["imgz/Image1.jpeg",
               "imgz/Image2.jpeg",
               "imgz/Image3.jpeg",
               "imgz/Image4.jpeg",
               "imgz/Image5.jpeg",
               "imgz/Image6.png",
               "imgz/Image7.jpeg",
               "imgz/Image8.jpeg"]


def pick_image(mouseX, mouseY):  # TODO so many magic number
    if mouseX < 800: return

    if mouseY <= 100:
        tilePicked = pg.image.load(r'imgz/image1.jpeg')
    if 100 < mouseY <= 200:
        tilePicked = pg.image.load(r'imgz/image2.jpeg')
    if 200 < mouseY <= 300:
        tilePicked = pg.image.load(r'imgz/image3.jpeg')
    if 300 < mouseY <= 400:
        tilePicked = pg.image.load(r'imgz/image4.jpeg')
    if 400 < mouseY <= 500:
        tilePicked = pg.image.load(r'imgz/image5.jpeg')
    if 500 < mouseY <= 600:
        tilePicked = pg.image.load(r'imgz/image6.png')
    if 600 < mouseY <= 700:
        tilePicked = pg.image.load(r'imgz/image7.jpeg')
    if mouseY >= 700:
        tilePicked = pg.image.load(r'imgz/image8.jpeg')
    return tilePicked


# --- Create grid of numbers
# Create an empty list
grid = []
# Loop for each row
for row in range(10):  # TODO magic number
    # For each row, create a list that will
    # represent an entire row
    grid.append([])
    # Loop for each column
    for column in range(10):  # TODO magic number
        # Add a the number zero to the current row
        grid[row].append(0)

screen.fill((255, 255, 255))
while True:

    mouseX, mouseY = pg.mouse.get_pos()

    pg.draw.line(screen, (0, 0, 0), (800, 0), (800, 800))

    i = 0
    while (i < 8 / SCALE + 1):  # TODO an iterating while loop is the same as a for loop
        i += 1
        pg.draw.line(screen, (0, 0, 0), (i * SCALE * 100, 0), (i * SCALE * 100, 800))  # TODO magic number

    im = 0
    while (im < 8 / SCALE + 1):  # TODO ^(ln69) #TODO magic number
        im += 1
        pg.draw.line(screen, (0, 0, 0), (0, im * SCALE * 100), (800, im * SCALE * 100))  # TODO magic number

    # TODO make sure this works #TODO magic number
    for index, image in enumerate(tile_images):
        screen.blit(pg.transform.scale(pg.image.load(image), (100, 100)), (800, index * 100))
    # screen.blit(pg.transform.scale(pg.image.load(r'imgz/image1.jpeg'), (100,100)), (800, 0))
    # screen.blit(pg.transform.scale(pg.image.load(r'imgz/image2.jpeg'), (100,100)), (800, 100))
    # screen.blit(pg.transform.scale(pg.image.load(r'imgz/image3.jpeg'), (100,100)), (800, 200))
    # screen.blit(pg.transform.scale(pg.image.load(r'imgz/image4.jpeg'), (100,100)), (800, 300))
    # screen.blit(pg.transform.scale(pg.image.load(r'imgz/image5.jpeg'), (100,100)), (800, 400))
    # screen.blit(pg.transform.scale(pg.image.load(r'imgz/image6.png'), (100,100)), (800, 500))
    # screen.blit(pg.transform.scale(pg.image.load(r'imgz/image7.jpeg'), (100,100)), (800, 600))
    # screen.blit(pg.transform.scale(pg.image.load(r'imgz/image8.jpeg'), (100,100)), (800, 700))

    if (pg.mouse.get_pressed(3)[0] == True):
        tilePicked = pick_image(mouseX, mouseY)
        grid[int(mouseX // GRID_TO_ARRAY)][int(mouseY // GRID_TO_ARRAY)] = 1  # TODO magic number

    if (grid[mouseX // int(GRID_TO_ARRAY)][mouseY // int(
            GRID_TO_ARRAY)] == 1):  # TODO what is this code for? it is not clear to me when reading it #TODO magic number
        screen.blit(pg.transform.scale(tilePicked, (100 * SCALE, 100 * SCALE)),
                    (100 * (mouseX // 50) * SCALE, 100 * (mouseY // 50) * SCALE))  # TODO magic number

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    pg.display.flip()
