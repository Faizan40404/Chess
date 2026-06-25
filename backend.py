import pygame

def movePiece(board, current_loc, next_loc):
    curr_x,curr_y=current_loc
    pieceSymbol=board[curr_y][curr_x]
    next_x,next_y=next_loc
    board[next_y][next_x]=pieceSymbol
    board[curr_y][curr_x]=""
