import pygame
from sys import exit

pygame.init()
import GUI

width=825
height=600

# WK-WQ-BK-BQ
castling_rights=(True,True,True,True)

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Shatranj')

icon=pygame.image.load('Images/Pieces/black/knight.png')
pygame.display.set_icon(icon)

GUI.displayBoard(screen)

# None or (x,y)
selected=tuple()

# 1-White 0-Blac
turn = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected,turn=GUI.selections(screen,selected,turn)


    pygame.display.update()