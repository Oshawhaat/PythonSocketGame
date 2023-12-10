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

scale = 0.5
yPosImage = False
xPosImage = False


def pick_image(mouseX, mouseY): #TODO handle if mouse is at exactly a multiple of 100 #TODO so many magic number
    if not mouseX > 800: return

    if(mouseY < 100):
        tilePicked = pg.image.load(r'imgz/image1.jpeg')
    if(mouseY > 100 and mouseY < 200):
        tilePicked = pg.image.load(r'imgz/image2.jpeg')
    if(mouseY > 200 and mouseY < 300):
        tilePicked = pg.image.load(r'imgz/image3.jpeg')
    if(mouseY > 300 and mouseY < 400):
        tilePicked = pg.image.load(r'imgz/image4.jpeg')
    if(mouseY > 400 and mouseY < 500):
        tilePicked = pg.image.load(r'imgz/image5.jpeg')
    if(mouseY > 500 and mouseY < 600):
        tilePicked = pg.image.load(r'imgz/image6.png')
    if(mouseY > 600 and mouseY < 700):
        tilePicked = pg.image.load(r'imgz/image7.jpeg')
    if(mouseY > 700):
        tilePicked = pg.image.load(r'imgz/image8.jpeg')
    return screen.blit(pg.transform.scale(tilePicked,(100,100)), (mouseX, mouseY))
    

# --- Create grid of numbers
# Create an empty list
# --- Create grid of numbers
# Create an empty list
grid = []
# Loop for each row
for row in range(10): #TODO magic number
    # For each row, create a list that will
    # represent an entire row
    grid.append([])
    # Loop for each column
    for column in range(10): #TODO magic number
        # Add a the number zero to the current row
        grid[row].append(0)


while True:
    screen.fill((255,255,255))

    mouseX, mouseY = pg.mouse.get_pos()

    pg.draw.line(screen, (0,0,0), (800,0), (800,800))

    i = 0
    while(i < 8/scale+1): #TODO an iterating while loop is the same as a for loop
        i+=1
        pg.draw.line(screen, (0,0,0), (i*scale*100,0), (i*scale*100,800)) #TODO magic number

    im = 0
    while(im < 8/scale+1): #TODO ^(ln69) #TODO magic number
        im+=1
        pg.draw.line(screen, (0,0,0), (0,im*scale*100), (800,im*scale*100)) #TODO magic number

    #TODO when repeating a bunch of code but slighly differnt, a for loop is almost always the solution #TODO magic number
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image1.jpeg'),(100,100)), (800, 0))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image2.jpeg'),(100,100)), (800, 100))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image3.jpeg'),(100,100)), (800, 200))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image4.jpeg'),(100,100)), (800, 300))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image5.jpeg'),(100,100)), (800, 400))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image6.png'),(100,100)), (800, 500))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image7.jpeg'),(100,100)), (800, 600))
    screen.blit(pg.transform.scale(pg.image.load(r'imgz/image8.jpeg'),(100,100)), (800, 700))

    if(pg.mouse.get_pressed(3)[0] == True):
       grid[mouseX//100][mouseY//100] = 1 #TODO magic number
       print(grid)         

    
    for column in range(int(8/scale)): #TODO magic number
        for row in range(int(8/scale)): #TODO magic number
            screen.blit(pg.transform.scale(pg.image.load(r'imgz/image8.jpeg'),(100*scale,100*scale)), (100*column*scale, 100*row*scale)) #TODO lots of magic numbers
    
    if(grid[mouseX//100][mouseY//100] == 1): #TODO what is this code for? it is not clear to me when reading it #TODO magic number
        screen.blit(pg.transform.scale(tilePicked,(100*scale,100*scale)), (100*(200//50)*scale, 100*(299//50)*scale)) #TODO magic number
        screen.blit(pg.transform.scale(tilePicked,(100*scale,100*scale)), (100*(mouseX//50)*scale, 100*(mouseY//50)*scale)) #TODO magic number
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            pos=pg.mouse.get_pos()
            btn=pg.mouse
            print ("x = {}, y = {}".format(pos[0], pos[1])) #TODO you can simply fill the curleys with the var you want by using an f string

    pg.display.flip()
