import pickle
import pygame as pg
import socket
import glob
import os
import random as rnd
pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
AMOGUS = pg.image.load(r'imgz/amogus.png')
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tilePicked = pg.image.load(r'imgz/image1.jpeg')
mouseX,mouseY = pg.mouse.get_pos()
emouseX = mouseX
emouseY = mouseY
scale = 0.5
yPosImage = False
xPosImage = False
def PickImage():
    global tilePicked
    if(mouseY < 100 and mouseX > 800):
        tilePicked = pg.image.load(r'imgz/image1.jpeg')
    if(mouseY > 100 and mouseY < 200 and mouseX > 800):
        print("2nd")
        tilePicked = pg.image.load(r'imgz/image2.jpeg')
    if(mouseY > 200 and mouseY < 300 and mouseX > 800):
        tilePicked = pg.image.load(r'imgz/image3.jpeg')
    if(mouseY > 300 and mouseY< 400 and mouseX > 800):
        tilePicked = pg.image.load(r'imgz/image4.jpeg')
    if(mouseY > 400 and mouseY < 500 and mouseX > 800):
        tilePicked = pg.image.load(r'imgz/image5.jpeg')
    if(mouseY > 500 and mouseY < 600) and mouseX > 800:
        tilePicked = pg.image.load(r'imgz/image6.png')
    if(mouseY > 600 and mouseY < 700 and mouseX > 800):
        tilePicked = pg.image.load(r'imgz/image7.jpeg')
    if(mouseY > 700):
        tilePicked = pg.image.load(r'imgz/image8.jpeg')
    if(mouseX < 800):
        global emouseX
        emouseX = mouseX
        global emouseY
        emouseY = mouseY
        return screen.blit(pg.transform.scale(tilePicked,(100,100)), (emouseX, emouseY))
# --- Create grid of numbers
# Create an empty list
# --- Create grid of numbers
# Create an empty list
grid = []
# Loop for each row
for row in range(10):
    # For each row, create a list that will
    # represent an entire row
    grid.append([])
    # Loop for each column
    for column in range(10):
        # Add a the number zero to the current row
        grid[row].append(0)

while True:
    screen.fill((255,255,255))
    pg.draw.line(screen, (0,0,0), (800,0), (800,800))
    i = 0
    im = 0
    while(i < 8/scale+1):
        i+=1
        pg.draw.line(screen, (0,0,0), (i*scale*100,0), (i*scale*100,800))
    while(im < 8/scale+1):
        im+=1
        pg.draw.line(screen, (0,0,0), (0,im*scale*100), (800,im*scale*100))


    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image1.jpeg'),(100,100)), (800, 0))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image2.jpeg'),(100,100)), (800, 100))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image3.jpeg'),(100,100)), (800, 200))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image4.jpeg'),(100,100)), (800, 300))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image5.jpeg'),(100,100)), (800, 400))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image6.png'),(100,100)), (800, 500))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image7.jpeg'),(100,100)), (800, 600))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image8.jpeg'),(100,100)), (800, 700))
    mouseX,mouseY = pg.mouse.get_pos()
    if(pg.mouse.get_pressed(3)[0] == True):
       grid[mouseX//100][mouseY//100] = 1
       print(grid)         

    
    
    for column in range(int(8/scale)):
        for row in range(int(8/scale)):
            screen.blit(pg.transform.scale(pg.image.load(r'imgz/image8.jpeg'),(100*scale,100*scale)), (100*column*scale, 100*row*scale))
    if(grid[mouseX//100][mouseY//100] == 1):
        screen.blit(pg.transform.scale(tilePicked,(100*scale,100*scale)), (100*(200//50)*scale, 100*(299//50)*scale))
        screen.blit(pg.transform.scale(tilePicked,(100*scale,100*scale)), (100*(mouseX//50)*scale, 100*(mouseY//50)*scale))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            pos=pg.mouse.get_pos()
            btn=pg.mouse
            print ("x = {}, y = {}".format(pos[0], pos[1]))
    pg.display.flip()
    # stuff can go here too
    pg.display.update()
    # I wouldn't put anything after the display.update() call