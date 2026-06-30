def isMyTurn(board,pieceLocation,turn):
    piece_x,piece_y=pieceLocation
    if (turn==1 and board[piece_y][piece_x][0]=='w') or (turn==0 and board[piece_y][piece_x][0]=='b'):
        return True
    else:
        return False

def pawnToPromote(board):
    if 'wp' in board[0] or 'bp' in board[7]:
        return True
    return False

def whichPawnToPromote(board):
    x=0
    for pieceSymbol in board[0]:
        if pieceSymbol != '':
            if pieceSymbol[1]=='p':
                return x,0
        x+=1
    x=0
    for pieceSymbol in board[7]:
        if pieceSymbol != '':
            if pieceSymbol[1]=='p':
                return x,7
        x+=1


def movePiece(board, current_loc, next_loc,turn):
    curr_x,curr_y=current_loc
    pieceSymbol=board[curr_y][curr_x]
    next_x,next_y=next_loc
    board[next_y][next_x]=pieceSymbol
    board[curr_y][curr_x]=""

    turn^=1
    return turn

def checkFriendly(board,piece1_loc,piece2_loc,turn):
    p1_x,p1_y=piece1_loc
    p2_x,p2_y=piece2_loc
    if board[p1_y][p1_x]!='':
        return True if board[p1_y][p1_x][0] == board[p2_y][p2_x][0] else False
    else:
        color='w' if turn else 'b'
        return True if color == board[p2_y][p2_x][0] else False

def isCoordinateValid(x,y):
    if x<0 or x>7 or y<0 or y>7:
        return False
    return True

def getLinearMoves(board, pieceLocation, directionList,turn):
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
            if not checkFriendly(board,pieceLocation,(mark_x,mark_y),turn):
                enemy.append((mark_x,mark_y))
    return empty,enemy


def getBishopMoves(board, bishopLocation,turn):
    directions=[(1,1),(1,-1),(-1,-1),(-1,1)]
    return getLinearMoves(board,bishopLocation,directions,turn)

def getBishopPsuedolegalMoves(board,bishopLocation,turn):
    enemy,empty=getBishopMoves(board,bishopLocation,turn)
    return enemy+empty

def getRookMoves(board, rookLocation,turn):
    directions=[(1,0),(-1,0),(0,1),(0,-1)]
    return getLinearMoves(board,rookLocation,directions,turn)

def getRookPsuedolegalMoves(board,rookLocation,turn):
    enemy,empty=getRookMoves(board,rookLocation,turn)
    return enemy+empty

def getQueenMoves(board, queenLocation,turn):
    directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]
    return getLinearMoves(board,queenLocation,directions,turn)

def getQueenPsuedolegalMoves(board,queenLocation,turn):
    enemy,empty=getQueenMoves(board,queenLocation,turn)
    return enemy+empty

def getStepMoves(board, pieceLocation, directionList,turn):
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
            elif not checkFriendly(board,pieceLocation,(mark_x,mark_y),turn):
                enemy.append((mark_x,mark_y))
    return empty,enemy

def getKingMoves(board, kingLocation,turn):
    directions=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]
    return getStepMoves(board, kingLocation,directions,turn)

def getKingPsuedolegalMoves(board,kingLocation,turn):
    empty,enemy=getKingMoves(board,kingLocation,turn)
    return empty+enemy

def getKnightMoves(board, knightLocation,turn):
    directions=[(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
    return getStepMoves(board, knightLocation,directions,turn)

def getKnightPsuedolegalMoves(board,knightLocation,turn):
    empty,enemy=getKnightMoves(board,knightLocation,turn)
    return empty+enemy

def canPawnMoveTwoSteps(board, pawnLocation,turn):
    _,pawn_y=pawnLocation
    color='w' if turn else 'b'
    if (color=='w' and pawn_y==6) or (color=='b' and pawn_y==1):
        return True
    else:
        return False

def createPawnMoves(board, pawnLocation,directionList,turn):
    enemy=[]
    empty=[]
    mark_x,mark_y=pawnLocation
    dy=directionList[0][1]
    mark_y+=dy
    if isCoordinateValid(mark_x,mark_y):
        if len(board[mark_y][mark_x])==0:
            empty.append((mark_x,mark_y))
            if canPawnMoveTwoSteps(board, pawnLocation,turn):
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
                if not checkFriendly(board, pawnLocation,(mark_x,mark_y),turn):
                    enemy.append((mark_x,mark_y))

    return empty,enemy

def getPawnMoves(board,pawnLocation,turn):
    directionList=[]
    color='w' if turn else 'b'
    if color=='w':
        directionList=[(-1,-1),(1,-1)]
    else:
        directionList=[(-1,1),(1,1)]
    return createPawnMoves(board, pawnLocation,directionList,turn)

def getPawnPsuedolegalMoves(board, pawnLocation,turn):
    empty,enemy=getPawnMoves(board,pawnLocation,turn)
    return empty+enemy

def getPieceMoves(board,pieceLocation,turn):
    p_x,p_y=pieceLocation
    if board[p_y][p_x][1]=='b':
        return getBishopMoves(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='r':
        return getRookMoves(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='q':
        return getQueenMoves(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='k':
        return getKingMoves(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='n':
        return getKnightMoves(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='p':
        return getPawnMoves(board,pieceLocation,turn)

def getPiecePsuedoLegalMoves(board, pieceLocation,turn):
    piece_x,piece_y=pieceLocation
    if board[piece_y][piece_x][1]=='p':
        return getPawnPsuedolegalMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='k':
        return getKingPsuedolegalMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='q':
        return getQueenPsuedolegalMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='n':
        return getKnightPsuedolegalMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='r':
        return getRookPsuedolegalMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='b':
        return getBishopPsuedolegalMoves(board,pieceLocation,turn)

def squareInCheck(board,squareLocation,turn):
    color='w' if turn else 'b'
    opposite='b' if color=='w' else 'w'
    _,bishop_enemy=getBishopMoves(board,squareLocation,turn)
    _,rook_enemy=getRookMoves(board,squareLocation,turn)
    _,knight_enemy=getKnightMoves(board,squareLocation,turn)
    _,king_enemy=getKingMoves(board,squareLocation,turn)
    _,pawn_enemy=getPawnMoves(board,squareLocation,turn)
    checkFrom=[]
    for location in bishop_enemy:
        loc_x,loc_y=location
        if board[loc_y][loc_x]!='':
            if board[loc_y][loc_x]==(opposite+'b') or board[loc_y][loc_x]==(opposite+'q'):
                checkFrom.append((loc_x,loc_y))
    for location in rook_enemy:
        loc_x,loc_y=location
        if board[loc_y][loc_x]!='':
            if board[loc_y][loc_x]==(opposite+'r') or board[loc_y][loc_x]==(opposite+'q'):
                checkFrom.append((loc_x,loc_y))
    for location in knight_enemy:
        loc_x,loc_y=location
        if board[loc_y][loc_x]!='':
            if board[loc_y][loc_x]==(opposite+'n'):
                checkFrom.append((loc_x,loc_y))
    for location in king_enemy:
        loc_x,loc_y=location
        if board[loc_y][loc_x]!='':
            if board[loc_y][loc_x]==(opposite+'k'):
                checkFrom.append((loc_x,loc_y))
    for location in pawn_enemy:
        loc_x,loc_y=location
        if board[loc_y][loc_x]!='':
            if board[loc_y][loc_x]==(opposite+'p'):
                checkFrom.append((loc_x,loc_y))

    return checkFrom

def findMyKing(board,turn):
    color='w' if turn else 'b'
    for i in range(8):
        for j in range(8):
            if board[j][i]==color+'k':
                return i,j

def kingInCheck(board,turn):
    i,j=findMyKing(board,turn)
    return squareInCheck(board,(i,j),turn)

def movePieceTemporarily(board,current_loc,next_loc):
    curr_x,curr_y=current_loc
    pieceSymbol=board[curr_y][curr_x]
    next_x,next_y=next_loc
    previousOccupier=board[next_y][next_x]
    board[next_y][next_x]=pieceSymbol
    board[curr_y][curr_x]=""

    return previousOccupier

def undoTempMove(board,current_loc,next_loc,previousOccupier):
    curr_x,curr_y=current_loc
    pieceSymbol=board[curr_y][curr_x]
    next_x,next_y=next_loc
    board[next_y][next_x]=pieceSymbol
    board[curr_y][curr_x]=previousOccupier

def getLegalPieceMovesSeperately(board,pieceLocation,turn):
    empty,enemy=getPieceMoves(board,pieceLocation,turn)

    legalEmpty=[]
    legalEnemy=[]
    for emptyCell in empty:
        previousOccupier=movePieceTemporarily(board,pieceLocation,emptyCell)
        if len(kingInCheck(board,turn))==0:
            legalEmpty.append(emptyCell)
        undoTempMove(board,emptyCell,pieceLocation,previousOccupier)
    for enemyCell in enemy:
        previousOccupier=movePieceTemporarily(board,pieceLocation,enemyCell)
        if len(kingInCheck(board,turn))==0:
            legalEnemy.append(enemyCell)
        undoTempMove(board,enemyCell,pieceLocation,previousOccupier)
    return legalEmpty,legalEnemy

def getLegalPieceMoves(board,pieceLocation,turn):
    empty,enemy=getLegalPieceMovesSeperately(board,pieceLocation,turn)
    return empty+enemy

def getAllLegalMovesSeperately(board,turn):
    color='w' if turn else 'b'
    legalEmpty=[]
    legalEnemy=[]
    for i in range(8):
        for j in range(8):
            if board[j][i]!='' and board[j][i][0]==color:
                empty,enemy=getLegalPieceMovesSeperately(board,(i,j),turn)
                legalEnemy+=enemy
                legalEmpty+=empty
    return legalEmpty,legalEnemy

def getAllLegalMoves(board,turn):
    legalEmpty,legalEnemy=getAllLegalMovesSeperately(board,turn)
    return legalEmpty+legalEnemy


def isCheckMate(board,turn):
    king_x,king_y=findMyKing(board,turn)
    if  len(squareInCheck(board,(king_x,king_y),turn))>0:
        legal_moves=getAllLegalMoves(board,turn)
        if len(legal_moves)==0:
            return True
    return False

def isStaleMate(board,turn):
    king_x,king_y=findMyKing(board,turn)
    if  len(squareInCheck(board,(king_x,king_y),turn))==0:
        legal_moves=getAllLegalMoves(board,turn)
        if len(legal_moves)==0:
            return True
    return False