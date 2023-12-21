from Finchbot.BirdBrain import Finch

import pygame

pygame.init()
finch = Finch()
from time import sleep

upKeyIsDown = False
downKeyIsDown = False

angleTurned = 0

while True:
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP):
                upKeyIsDown = True
            if(event.key == pygame.K_DOWN):
                downKeyIsDown = True
            if(event.key == pygame.K_LEFT):
                angleTurned -= 20
                finch.setTurn('L', 90, 200)
            if(event.key == pygame.K_RIGHT):
                angleTurned+=20

                finch.setTurn('R', 90, 200)
        if(event.type == pygame.KEYUP):
            if(event.key==pygame.K_DOWN):
                downKeyIsDown = False
            if(event.key == pygame.K_UP):
                upKeyIsDown = False

    
    if(upKeyIsDown):
       finch.setMotors(20, 20)
    
    if(downKeyIsDown):
       finch.setMotors(-20, -20)

    if(upKeyIsDown==False and downKeyIsDown==False):
       finch.setMotors(0,0)

    sleep(0.1)