def isMyTurn(board,pieceLocation,turn):
    piece_x,piece_y=pieceLocation
    if (turn==1 and board[piece_y][piece_x][0]=='w') or (turn==0 and board[piece_y][piece_x][0]=='b'):
        return True
    else:
        return False
def movePiece(board, current_loc, next_loc,turn):
    curr_x,curr_y=current_loc
    pieceSymbol=board[curr_y][curr_x]
    next_x,next_y=next_loc
    board[next_y][next_x]=pieceSymbol
    board[curr_y][curr_x]=""

    turn^=1
    return turn

def checkFriendly(board,piece1_loc,piece2_loc):
    p1_x,p1_y=piece1_loc
    p2_x,p2_y=piece2_loc
    return True if board[p1_y][p1_x][0] == board[p2_y][p2_x][0] else False

def isCoordinateValid(x,y):
    if x<0 or x>7 or y<0 or y>7:
        return False
    return True

def getLinearMoves(board, pieceLocation, directionList):
    empty=[]
    enemy=[]
    for direction in directionList:
        mark_x,mark_y=pieceLocation
        dx,dy=direction
        mark_x+=dx
        mark_y+=dy
        while isCoordinateValid(mark_x,mark_y) and len(board[mark_y][mark_x])==0 :
           empty.append((mark_x,mark_y))
           mark_x+=dx
           mark_y+=dy
        if isCoordinateValid(mark_x,mark_y):
            if not checkFriendly(board,pieceLocation,(mark_x,mark_y)):
                enemy.append((mark_x,mark_y))
    return empty,enemy


def getBishopMoves(board, bishopLocation):
    directions=[(1,1),(1,-1),(-1,-1),(-1,1)]
    return getLinearMoves(board,bishopLocation,directions)

def getBishopPsuedolegalMoves(board,bishopLocation):
    enemy,empty=getBishopMoves(board,bishopLocation)
    return enemy+empty

def getRookMoves(board, rookLocation):
    directions=[(1,0),(-1,0),(0,1),(0,-1)]
    return getLinearMoves(board,rookLocation,directions)

def getRookPsuedolegalMoves(board,rookLocation):
    enemy,empty=getRookMoves(board,rookLocation)
    return enemy+empty

def getQueenMoves(board, queenLocation):
    directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]
    return getLinearMoves(board,queenLocation,directions)

def getQueenPsuedolegalMoves(board,queenLocation):
    enemy,empty=getQueenMoves(board,queenLocation)
    return enemy+empty

def getStepMoves(board, pieceLocation, directionList):
    empty=[]
    enemy=[]
    for direction in directionList:
        mark_x,mark_y=pieceLocation
        dx,dy=direction
        mark_x+=dx
        mark_y+=dy
        if isCoordinateValid(mark_x,mark_y):
            if len(board[mark_y][mark_x])==0:
                empty.append((mark_x,mark_y))
            elif not checkFriendly(board,pieceLocation,(mark_x,mark_y)):
                enemy.append((mark_x,mark_y))
    return empty,enemy

def getKingMoves(board, kingLocation):
    directions=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]
    return getStepMoves(board, kingLocation,directions)

def getKingPsuedolegalMoves(board,kingLocation):
    empty,enemy=getKingMoves(board,kingLocation)
    return empty+enemy

def getKnightMoves(board, knightLocation):
    directions=[(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
    return getStepMoves(board, knightLocation,directions)

def getKnightPsuedolegalMoves(board,knightLocation):
    empty,enemy=getKnightMoves(board,knightLocation)
    return empty+enemy

def canPawnMoveTwoSteps(board, pawnLocation):
    pawn_x,pawn_y=pawnLocation
    if (board[pawn_y][pawn_x][0]=='w' and pawn_y==6) or (board[pawn_y][pawn_x][0]=='b' and pawn_y==1):
        return True
    else:
        return False

def createPawnMoves(board, pawnLocation,directionList):
    enemy=[]
    empty=[]
    mark_x,mark_y=pawnLocation
    dy=directionList[0][1]
    mark_y+=dy
    if isCoordinateValid(mark_x,mark_y):
        if len(board[mark_y][mark_x])==0:
            empty.append((mark_x,mark_y))
            if canPawnMoveTwoSteps(board, pawnLocation):
                mark_y+=dy
                if isCoordinateValid(mark_x,mark_y):
                    if len(board[mark_y][mark_x])==0:
                        empty.append((mark_x,mark_y))
    
    for direction in directionList:
        mark_x,mark_y=pawnLocation
        dx,dy=direction
        mark_x+=dx
        mark_y+=dy
        if isCoordinateValid(mark_x,mark_y):
            if len(board[mark_y][mark_x])>0:
                if not checkFriendly(board, pawnLocation,(mark_x,mark_y)):
                    enemy.append((mark_x,mark_y))

    return empty,enemy

def getPawnMoves(board,pawnLocation):
    pawn_x,pawn_y=pawnLocation
    directionList=[]
    if board[pawn_y][pawn_x][0]=='w':
        directionList=[(-1,-1),(1,-1)]
    else:
        directionList=[(-1,1),(1,1)]
    return createPawnMoves(board, pawnLocation,directionList)

def getPawnPsuedolegalMoves(board, pawnLocation):
    empty,enemy=getPawnMoves(board,pawnLocation)
    return empty+enemy

def getPiecePsuedoLegalMoves(board, pieceLocation):
    piece_x,piece_y=pieceLocation
    if board[piece_y][piece_x][1]=='p':
        return getPawnPsuedolegalMoves(board,pieceLocation)
    elif board[piece_y][piece_x][1]=='k':
        return getKingPsuedolegalMoves(board,pieceLocation)
    elif board[piece_y][piece_x][1]=='q':
        return getQueenPsuedolegalMoves(board,pieceLocation)
    elif board[piece_y][piece_x][1]=='n':
        return getKnightPsuedolegalMoves(board,pieceLocation)
    elif board[piece_y][piece_x][1]=='r':
        return getRookPsuedolegalMoves(board,pieceLocation)
    elif board[piece_y][piece_x][1]=='b':
        return getBishopPsuedolegalMoves(board,pieceLocation)