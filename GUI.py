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

black_box=pygame.Surface((box_size,box_size))
black_box.fill(black)

white_box=pygame.Surface((box_size,box_size))
white_box.fill(white)

def loadPieces():
    pieces={}

    for color in ['black','white']:
        for piece in ['rook','knight','bishop','queen','king','pawn']:
            path='Pieces/'+color+'/'+piece+'.png'
            image = pygame.image.load(path)
            image=pygame.transform.scale(image,(65,65))
            rect=image.get_rect(topleft=(0,0))

            key_piece=piece[0] if piece!='knight' else 'n'
            pieces[color[0]+key_piece]=(image,rect)

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

            piece=board[i][j]
            if piece != '':
                image,rect=pieces[piece]
                rect.topleft=(x_pos+5,y_pos+5)
                screen.blit(image,rect)

    pygame.display.update()
