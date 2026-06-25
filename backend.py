import pygame

def movePiece(board, current_loc, next_loc):
    curr_x,curr_y=current_loc
    pieceSymbol=board[curr_y][curr_x]
    next_x,next_y=next_loc
    board[next_y][next_x]=pieceSymbol
    board[curr_y][curr_x]=""

def checkFriendly(board,piece1_loc,piece2_loc):
    p1_x,p1_y=piece1_loc
    p2_x,p2_y=piece2_loc
    return True if board[p1_y][p1_x][0] == board[p2_y][p2_x][0] else False

def checkValidCoordinates(x,y):
    if x<0 or x>7 or y<0 or y>7:
        return False
    return True

def getBishopMoves(board, bishopLocation):
    empty=[]
    enemy=[]
    for direction in [(1,1),(1,-1),(-1,-1),(-1,1)]:
        mark_x,mark_y=bishopLocation
        dx,dy=direction
        mark_x+=dx
        mark_y+=dy
        while checkValidCoordinates(mark_x,mark_y) and len(board[mark_y][mark_x])==0 :
           empty.append((mark_x,mark_y))
           mark_x+=dx
           mark_y+=dy
        if checkValidCoordinates(mark_x,mark_y):
            if not checkFriendly(board,bishopLocation,(mark_x,mark_y)):
                enemy.append((mark_x,mark_y))
    return empty,enemy

def getBishopPsuedolegalMoves(board,bishopLocation):
    enemy,empty=getBishopMoves(board,bishopLocation)
    return enemy+empty

def getRookMoves(board, rookLocation):
    empty=[]
    enemy=[]
    for direction in [(1,0),(-1,0),(0,1),(0,-1)]:
        mark_x,mark_y=rookLocation
        dx,dy=direction
        mark_x+=dx
        mark_y+=dy
        while checkValidCoordinates(mark_x,mark_y) and len(board[mark_y][mark_x])==0 :
           empty.append((mark_x,mark_y))
           mark_x+=dx
           mark_y+=dy
        if checkValidCoordinates(mark_x,mark_y):
            if not checkFriendly(board,rookLocation,(mark_x,mark_y)):
                enemy.append((mark_x,mark_y))
    return empty,enemy

def getRookPsuedolegalMoves(board,rookLocation):
    enemy,empty=getRookMoves(board,rookLocation)
    return enemy+empty

def getQueenMoves(board, queenLocation):
    empty=[]
    enemy=[]
    for direction in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]:
        mark_x,mark_y=queenLocation
        dx,dy=direction
        mark_x+=dx
        mark_y+=dy
        while checkValidCoordinates(mark_x,mark_y) and len(board[mark_y][mark_x])==0 :
           empty.append((mark_x,mark_y))
           mark_x+=dx
           mark_y+=dy
        if checkValidCoordinates(mark_x,mark_y):
            if not checkFriendly(board,queenLocation,(mark_x,mark_y)):
                enemy.append((mark_x,mark_y))
    return empty,enemy

def getQueenPsuedolegalMoves(board,queenLocation):
    enemy,empty=getRookMoves(board,queenLocation)
    return enemy+empty