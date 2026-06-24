import pygame

turn = 1

def movePiece(pieces, current_loc, next_loc):
    curr_x,curr_y=current_loc
    piece=pieces[curr_x][curr_y]
    next_x,next_y=next_loc
    pieces[next_x][next_y]=piece
    pieces[curr_x][curr_y]=""