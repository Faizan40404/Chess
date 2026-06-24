import pygame

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
black  = (181, 136, 99)

white_selected = (246, 246, 105)
black_selected = (186, 202, 68)

black_box=pygame.Surface((box_size,box_size))
black_box.fill(black)

black_selected_box=pygame.Surface((box_size,box_size))
black_selected_box.fill(black_selected)

white_box=pygame.Surface((box_size,box_size))
white_box.fill(white)

white_selected_box=pygame.Surface((box_size,box_size))
white_selected_box.fill(white_selected)

class ChessPiece:
    def __init__(self, color, name, x, y):
        self.color=color
        self.name=name
        self.image=pygame.image.load(f'Pieces/{color}/{name}.png')
        self.image=pygame.transform.smoothscale(self.image,(65,65))
        self.rect=self.image.get_rect(topleft=(x,y))

    def drawPiece(self,screen):
        screen.blit(self.image,self.rect)

    def move_to(self,x,y):
        self.rect.topleft=(x*box_size+5,y*box_size+5)
        

def loadPieces():
    pieces={}

    for color in ['black','white']:
        for piece in ['rook','knight','bishop','queen','king','pawn']:
            key_piece=piece[0] if piece!='knight' else 'n'
            pieces[color[0]+key_piece]=ChessPiece(color,piece,0,0)

    return pieces

pieces=loadPieces()

def displayBoard(screen):
    for i in range(8):
        for j in range(8):
            x_pos=j*box_size
            y_pos=i*box_size
            if (i+j) % 2:
                screen.blit(black_box,(x_pos,y_pos))
            else:
                screen.blit(white_box,(x_pos,y_pos))

            pieceSymbol=board[i][j]
            if pieceSymbol != '':
                piece=pieces[pieceSymbol]
                piece.move_to(j,i)
                piece.drawPiece(screen)


def deSelectPiece(screen,cell_x,cell_y):
    pieceSymbol=board[cell_y][cell_x]
    if (cell_x+cell_y)%2:
        screen.blit(black_box,(cell_x*box_size,cell_y*box_size))
    else:
        screen.blit(white_box,(cell_x*box_size,cell_y*box_size))
    piece = pieces[pieceSymbol]
    piece.move_to(cell_x,cell_y)
    piece.drawPiece(screen)

def selectPiece(screen,cell_x,cell_y):
    pieceSymbol=board[cell_y][cell_x]
    if pieceSymbol != '':
        if (cell_x+cell_y)%2:
            screen.blit(black_selected_box,(cell_x*box_size,cell_y*box_size))
        else:
            screen.blit(white_selected_box,(cell_x*box_size,cell_y*box_size))
        piece = pieces[pieceSymbol]
        piece.move_to(cell_x,cell_y)
        piece.drawPiece(screen)
        return cell_x,cell_y

def selections(screen,selected):
    mouse_x, mouse_y=pygame.mouse.get_pos()
    cell_y=int(mouse_y / box_size)
    cell_x=int(mouse_x / box_size)
    if cell_x < 8 and cell_y<8:
        if not selected:
           return selectPiece(screen,cell_x,cell_y)
        elif (cell_x,cell_y) == selected:
            deSelectPiece(screen,cell_x,cell_y)
            return None
        else:
            old_x,old_y=selected
            deSelectPiece(screen,old_x,old_y)
            return selectPiece(screen,cell_x,cell_y)
            
    return None   