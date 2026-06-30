import pygame
import backend
from enum import Enum


board = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wr","wn","wb","wq","wk","wb","wn","wr"]
]

box_size=75

white = (240, 217, 181)
black = (181, 136, 99)

white_selected = (246, 246, 105)
black_selected = (186, 202, 68)

white_move = (170, 215, 255)
black_move = (90, 170, 230)

white_threat = (255, 160, 160)
black_threat = (200, 80, 80)

font_color= (200, 162, 74)

black_box=pygame.Surface((box_size,box_size))
black_box.fill(black)

black_selected_box=pygame.Surface((box_size,box_size))
black_selected_box.fill(black_selected)

black_move_box=pygame.Surface((box_size,box_size))
black_move_box.fill(black_move)

black_threat_box=pygame.Surface((box_size,box_size))
black_threat_box.fill(black_threat)

white_box=pygame.Surface((box_size,box_size))
white_box.fill(white)

white_selected_box=pygame.Surface((box_size,box_size))
white_selected_box.fill(white_selected)

white_move_box=pygame.Surface((box_size,box_size))
white_move_box.fill(white_move)

white_threat_box=pygame.Surface((box_size,box_size))
white_threat_box.fill(white_threat)

trajan_pro=pygame.font.Font('Fonts/trajan-pro/TrajanPro-Bold.otf',40)
title_surface=trajan_pro.render('Shatranj',True,font_color)
title_rect=title_surface.get_rect(midtop=(712,20))

# State for Each Square
class SquareState(Enum):
    NORMAL = 0
    SELECTED = 1
    MOVE = 2 
    THREAT =3

# Piece Class contains color, name, image, rect
class ChessPiece:
    def __init__(self, color, name, x, y):
        self.color=color
        self.name=name
        self.image=pygame.image.load(f'Images/Pieces/{color}/{name}.png')
        self.image=pygame.transform.smoothscale(self.image,(65,65))
        self.rect=self.image.get_rect(topleft=(x,y))

    def drawPiece(self,screen):
        screen.blit(self.image,self.rect)

    def move_to(self,x,y):
        self.rect.topleft=(x*box_size+5,y*box_size+5)
        
# Loads All pieces, stores and returns in dictionary
# 'pieceSymbol': ChessPiece
# pieceSymbol -> 2 chars where char[0]->color char[1]->piece
def loadPieces():
    pieces={}

    for color in ['black','white']:
        for piece in ['rook','knight','bishop','queen','king','pawn']:
            key_piece=piece[0] if piece!='knight' else 'n'
            pieces[color[0]+key_piece]=ChessPiece(color,piece,0,0)

    return pieces

pieces=loadPieces()

# Displays:
#   1. Background Image
#   2. Title
def displayMenu(screen):
    background_img=pygame.image.load('Images/Background/background.png').convert_alpha()
    background_img=pygame.transform.smoothscale(background_img,(225,600))
    background_rect=background_img.get_rect(topleft = (600,0))
    screen.blit(background_img,background_rect)

    screen.blit(title_surface,title_rect)

# Draws each box with different colors based on position, selection, move, or threat
def drawBox(screen,x,y,state):
    if state == SquareState.NORMAL:
        if (x+y) % 2:
            screen.blit(black_box,(x*box_size,y*box_size))
        else:
            screen.blit(white_box,(x*box_size,y*box_size))
    elif state == SquareState.SELECTED:
        if (x+y) % 2:
            screen.blit(black_selected_box,(x*box_size,y*box_size))
        else:
            screen.blit(white_selected_box,(x*box_size,y*box_size))
    elif state == SquareState.MOVE:
        if (x+y) % 2:
            screen.blit(black_move_box,(x*box_size,y*box_size))
        else:
            screen.blit(white_move_box,(x*box_size,y*box_size))
    elif state == SquareState.THREAT:
        if (x+y) % 2:
            screen.blit(black_threat_box,(x*box_size,y*box_size))
        else:
            screen.blit(white_threat_box,(x*box_size,y*box_size))

# Draws the 2d Box for chess board and the menu
def displayBoard(screen):
    for i in range(8):
        for j in range(8):
            drawBox(screen,j,i,SquareState.NORMAL)
            pieceSymbol=board[i][j]
            if pieceSymbol != '':
                piece=pieces[pieceSymbol]
                piece.move_to(j,i)
                piece.drawPiece(screen)

    displayMenu(screen)

# Selects the piece by highlighting it and showing its legal moves
#
# Returns (selectedPieceLocation)
def selectPiece(screen,cell_x,cell_y,turn):
    pieceSymbol=board[cell_y][cell_x]

    drawBox(screen,cell_x,cell_y,SquareState.SELECTED)
    piece = pieces[pieceSymbol]
    piece.move_to(cell_x,cell_y)
    piece.drawPiece(screen)

    showPieceMoves(screen,(cell_x,cell_y),turn)
    return cell_x,cell_y

# Deselects a Piece by drawing the window all over again
def deSelectPiece(screen):
    displayBoard(screen)

# Decides what to do when left click happens based on rules
# 1. If no pawn to promote
#   1.1. If click happens and:
#       1.1.1. Nothing is already selected then selects the clicked cell if a piece is there and its that colors turn
#       1.1.2. Clicked cell is same as already selected one then deselects 
#       1.1.3. Clicked cell is not same as already selected cell:
#           1.1.3.1. Clicked cell is empty or enemy then tries to move there
#           1.1.3.2. Clicked cell is friendly then selects clicked cell
# 2. If no pawn to promote:
#   2.1. Check which piece to promote the pawn to
#
# Returns (selectedPieceLocation, turn)
def selections(screen,selected,turn):
    mouse_x, mouse_y=pygame.mouse.get_pos()
    cell_y=int(mouse_y / box_size)
    cell_x=int(mouse_x / box_size)
    if not backend.pawnToPromote(board):
        if cell_x < 8 and cell_y<8:
            if not selected:
                if board[cell_y][cell_x]!='':
                    if backend.isMyTurn(board,(cell_x,cell_y),turn):  
                        return selectPiece(screen,cell_x,cell_y,turn),turn
            elif (cell_x,cell_y) == selected:
                deSelectPiece(screen)
                return None,turn
            else:
                old_x,old_y=selected
                deSelectPiece(screen)
                if  len(board[cell_y][cell_x])>0 and board[cell_y][cell_x][0] == board[old_y][old_x][0]: 
                    return selectPiece(screen,cell_x,cell_y,turn),turn
                else:
                    return None,movePiece(screen,selected,(cell_x,cell_y),turn)
    else:
        pieceSymbol,location=checkPromotionPiece()
        if pieceSymbol is not None:
            loc_x,loc_y=location
            board[loc_y][loc_x]=pieceSymbol
            deSelectPiece(screen)
            if backend.isCheckMate(board,turn):
                print('CheckMate')
            elif backend.isStaleMate(board,turn):
                print('StaleMate')

    return None,turn

# Draws the options to promote the pawn to
def showPromotionPieces(screen,pieceLocation):
    draw_x=9
    draw_y=1
    piece_x,piece_y=pieceLocation
    if board[piece_y][piece_x][0]=='w':
        pieceSymbols=['wq','wr','wn','wb']
    else:
        pieceSymbols=['bq','br','bn','bb']
    for pieceSymbol in pieceSymbols:
        piece=pieces[pieceSymbol]
        drawBox(screen,draw_x,draw_y,SquareState.NORMAL)
        piece.move_to(draw_x,draw_y)
        piece.drawPiece(screen)
        draw_y+=1


# Checks which piece has the player decided to promote the pawn to
#
# Returns (pieceSymbol,promotedPawnLocation)
def checkPromotionPiece():
    pawn_x,pawn_y=backend.whichPawnToPromote(board)
    promotionPawn=board[pawn_y][pawn_x]
    color=promotionPawn[0]
    mouse_x,mouse_y=pygame.mouse.get_pos()
    box_x=int(mouse_x/box_size)
    box_y=int(mouse_y/box_size)
    if box_x==9:
        if box_y==1:
            return color+'q',(pawn_x,pawn_y)
        elif box_y==2:
            return color+'r',(pawn_x,pawn_y)
        elif box_y==3:
            return color+'n',(pawn_x,pawn_y)
        elif box_y==4:
            return color+'b',(pawn_x,pawn_y)
    return None,None

# Tries to move a piece from 1 cell to other
# 1. If move is legal:
#   1.1. Moves Piece Visually
#   1.2. Asks Backend to move the piece in the list
# 2. If move is not legal:
#   2.1. Deselects the piece
#
# Returns (turn)
def movePiece(screen,current_loc, next_loc,turn):
    if next_loc in backend.getLegalPieceMoves(board,current_loc,turn):
        curr_x,curr_y=current_loc
        drawBox(screen,curr_x,curr_y,SquareState.NORMAL)
        pieceSymbol = board[curr_y][curr_x]
        next_x,next_y=next_loc
        drawBox(screen,next_x,next_y,SquareState.NORMAL)
        piece=pieces[pieceSymbol]
        piece.move_to(next_x,next_y)
        piece.drawPiece(screen)

        turn=backend.movePiece(board,current_loc,next_loc,turn)

        if backend.pawnToPromote(board):
            showPromotionPieces(screen,next_loc)

        if backend.isCheckMate(board,turn):
            print('CheckMate')
            return turn
        elif backend.isStaleMate(board,turn):
            print('StaleMate')
            return turn

        return turn
    else:
        deSelectPiece(screen)
        return turn

# Shows all legal moves of the required piece. Both Empty and enemy cell highlighted with different colors
def showPieceMoves(screen,pieceLocation,turn):
    empty_cell,enemy_cell=backend.getLegalPieceMovesSeperately(board,pieceLocation,turn)
    for cell in empty_cell:
        empty_x,empty_y=cell
        drawBox(screen,empty_x,empty_y,SquareState.MOVE)
    for cell in enemy_cell:
        enemy_x,enemy_y=cell
        pieceSymbol=board[enemy_y][enemy_x]
        drawBox(screen,enemy_x,enemy_y,SquareState.THREAT)
        piece=pieces[pieceSymbol]
        piece.move_to(enemy_x,enemy_y)
        piece.drawPiece(screen)