import GUI
import pygame
from sys import exit

pygame.init()

width=800
height=600



screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Shatranj')

GUI.displayBoard(screen)
selected=tuple()
turn = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected,turn=GUI.selections(screen,selected,turn)


    pygame.display.update()

    