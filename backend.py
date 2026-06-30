# Checks if selected piece color corrosponds with the turn
# Meaning during white's turn black pieces can't be selected and vice versa
#
# Returns (bool)
def isMyTurn(board,pieceLocation,turn):
    piece_x,piece_y=pieceLocation
    if (turn==1 and board[piece_y][piece_x][0]=='w') or (turn==0 and board[piece_y][piece_x][0]=='b'):
        return True
    else:
        return False

# Checks if there is a pawn to promote
#
# Returns (bool)
def pawnToPromote(board):
    if 'wp' in board[0] or 'bp' in board[7]:
        return True
    return False

# Finds which pawn is yet to promote
#
# Returns (pawnToPromoteLocation)
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

# Moves a piece from current location to next location
#
# Returns new Turn
def movePiece(board, current_loc, next_loc,turn):
    curr_x,curr_y=current_loc
    pieceSymbol=board[curr_y][curr_x]
    next_x,next_y=next_loc
    board[next_y][next_x]=pieceSymbol
    board[curr_y][curr_x]=""

    turn^=1
    return turn

# Checks if 2 cells have friendly pieces.
# 1. But If one of the cell is empty:
#   1.1. consider empty cell as occupied by the color whose turn is it right now
#
# Returns (bool)
def checkFriendly(board,piece1_loc,piece2_loc,turn):
    p1_x,p1_y=piece1_loc
    p2_x,p2_y=piece2_loc
    if board[p1_y][p1_x]!='':
        return True if board[p1_y][p1_x][0] == board[p2_y][p2_x][0] else False
    else:
        color='w' if turn else 'b'
        return True if color == board[p2_y][p2_x][0] else False

# Checks if coordinates are inside chess grid
#
# Returns (bool)
def isCoordinateValid(x,y):
    if x<0 or x>7 or y<0 or y>7:
        return False
    return True

# Creates moves for pieces who create rays for moves. i.e Rook, Queen, Bishop
# Keeps going in all direction until goes out of bounds, hits an enemy or friendly piece there
# If square is empty append into emptyList
# Skip if friedly
# If square is enemy append into enemyList
#
# Returns (emptyCellList, enemyCellList)
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

# Returns all BISHOP moves seperated into empty and enemy. 
# Moves can be ILLEGAL
def getBishopMovesSeperately(board, bishopLocation,turn):
    directions=[(1,1),(1,-1),(-1,-1),(-1,1)]
    return getLinearMoves(board,bishopLocation,directions,turn)

# Returns all BISHOP moves NOT seperated into empty and enemy. 
# Moves can be ILLEGAL
def getBishopMoves(board,bishopLocation,turn):
    enemy,empty=getBishopMovesSeperately(board,bishopLocation,turn)
    return enemy+empty

# Returns all ROOK moves seperated into empty and enemy. 
# Moves can be ILLEGAL
def getRookMovesSeperately(board, rookLocation,turn):
    directions=[(1,0),(-1,0),(0,1),(0,-1)]
    return getLinearMoves(board,rookLocation,directions,turn)

# Returns all ROOK moves NOT seperated into empty and enemy. 
# Moves can be ILLEGAL
def getRookMoves(board,rookLocation,turn):
    enemy,empty=getRookMovesSeperately(board,rookLocation,turn)
    return enemy+empty

# Returns all QUEEN moves seperated into empty and enemy. 
# Moves can be ILLEGAL
def getQueenMovesSeperately(board, queenLocation,turn):
    directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]
    return getLinearMoves(board,queenLocation,directions,turn)

# Returns all QUEEN moves NOT seperated into empty and enemy. 
# Moves can be ILLEGAL
def getQueenMoves(board,queenLocation,turn):
    enemy,empty=getQueenMovesSeperately(board,queenLocation,turn)
    return enemy+empty

# Creates moves for pieces who take only 1 step in each respective direction. i.e Knight, King
# If square is empty append into emptyList
# Skip if friedly
# If square is enemy append into enemyList
#
# Returns (emptyCellList, enemyCellList)
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

# Returns all KING moves seperated into empty and enemy. 
# Moves can be ILLEGAL
def getKingMovesSeperately(board, kingLocation,turn):
    directions=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]
    return getStepMoves(board, kingLocation,directions,turn)

# Returns all KING moves NOT seperated into empty and enemy. 
# Moves can be ILLEGAL
def getKingMoves(board,kingLocation,turn):
    empty,enemy=getKingMovesSeperately(board,kingLocation,turn)
    return empty+enemy

# Returns all KNIGHT moves seperated into empty and enemy. 
# Moves can be ILLEGAL
def getKnightMovesSeperately(board, knightLocation,turn):
    directions=[(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
    return getStepMoves(board, knightLocation,directions,turn)

# Returns all KNIGHT moves NOT seperated into empty and enemy. 
# Moves can be ILLEGAL
def getKnightMoves(board,knightLocation,turn):
    empty,enemy=getKnightMovesSeperately(board,knightLocation,turn)
    return empty+enemy

# checks if a pawn can move 2 steps
#
# Returns (bool)
def canPawnMoveTwoSteps(board, pawnLocation,turn):
    _,pawn_y=pawnLocation
    color='w' if turn else 'b'
    if (color=='w' and pawn_y==6) or (color=='b' and pawn_y==1):
        return True
    else:
        return False

# Creates pawn moves
# 1. Move forward possible number of steps.
#   1.1. if empty append into emptyList
#   1.2. Stop if friendly or enemy piece there
# 2. Move 1 step diagnol on respective side
#   2.1. if enemy then append else do nothing
#
# returns (emptyList,enemyList)
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

# Returns all PAWN moves seperated into empty and enemy. 
# Moves can be ILLEGAL
def getPawnMovesSeperately(board,pawnLocation,turn):
    directionList=[]
    color='w' if turn else 'b'
    if color=='w':
        directionList=[(-1,-1),(1,-1)]
    else:
        directionList=[(-1,1),(1,1)]
    return createPawnMoves(board, pawnLocation,directionList,turn)

# Returns all PAWN moves NOT seperated into empty and enemy. 
# Moves can be ILLEGAL
def getPawnMoves(board, pawnLocation,turn):
    empty,enemy=getPawnMovesSeperately(board,pawnLocation,turn)
    return empty+enemy

# Wrapper function that selects function to get moves for any particular piece seperated into empty and enemy 
# Moves can be ILLEGAL
def getPieceMovesSeperately(board,pieceLocation,turn):
    p_x,p_y=pieceLocation
    if board[p_y][p_x][1]=='b':
        return getBishopMovesSeperately(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='r':
        return getRookMovesSeperately(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='q':
        return getQueenMovesSeperately(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='k':
        return getKingMovesSeperately(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='n':
        return getKnightMovesSeperately(board,pieceLocation,turn)
    elif board[p_y][p_x][1]=='p':
        return getPawnMovesSeperately(board,pieceLocation,turn)

# Wrapper function that selects function to get moves for any particular piece NOT seperated into empty and enemy 
# Moves can be ILLEGAL
def getPieceMoves(board, pieceLocation,turn):
    piece_x,piece_y=pieceLocation
    if board[piece_y][piece_x][1]=='p':
        return getPawnMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='k':
        return getKingMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='q':
        return getQueenMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='n':
        return getKnightMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='r':
        return getRookMoves(board,pieceLocation,turn)
    elif board[piece_y][piece_x][1]=='b':
        return getBishopMoves(board,pieceLocation,turn)

# Checks if a cell is in check
# Generate rook, bishop, knight, king and pawn move
# if in a move set of piece_x from the cell, same piece but with opposite color is found then that enemy piece is checking me
# check for opposite queen should be checked in bishop and rook moves
#
# Returns (squareListFromWhichCheckCame)
def cellInCheck(board,squareLocation,turn):
    color='w' if turn else 'b'
    opposite='b' if color=='w' else 'w'
    _,bishop_enemy=getBishopMovesSeperately(board,squareLocation,turn)
    _,rook_enemy=getRookMovesSeperately(board,squareLocation,turn)
    _,knight_enemy=getKnightMovesSeperately(board,squareLocation,turn)
    _,king_enemy=getKingMovesSeperately(board,squareLocation,turn)
    _,pawn_enemy=getPawnMovesSeperately(board,squareLocation,turn)
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

# Finds the king of color whose turn is it right now
#
# Returns (kingLocation)
def findMyKing(board,turn):
    color='w' if turn else 'b'
    for i in range(8):
        for j in range(8):
            if board[j][i]==color+'k':
                return i,j

# checks if the king of color whose turn is it right now is in check
#
# Returns (squareListFromWhichCheckCame)
def kingInCheck(board,turn):
    i,j=findMyKing(board,turn)
    return cellInCheck(board,(i,j),turn)

# Temporarily moves a piece to a new location.
#
# Returns (previousOccupierOfCellWherePieceMovedTo)
def movePieceTemporarily(board,current_loc,next_loc):
    curr_x,curr_y=current_loc
    pieceSymbol=board[curr_y][curr_x]
    next_x,next_y=next_loc
    previousOccupier=board[next_y][next_x]
    board[next_y][next_x]=pieceSymbol
    board[curr_y][curr_x]=""

    return previousOccupier

# Undo Temporarily moves 
# Places piece to squre it came from and previous occupier of the cell back 
def undoTempMove(board,current_loc,next_loc,previousOccupier):
    curr_x,curr_y=current_loc
    pieceSymbol=board[curr_y][curr_x]
    next_x,next_y=next_loc
    board[next_y][next_x]=pieceSymbol
    board[curr_y][curr_x]=previousOccupier

# returns legal moves for a particular Piece seperated into empty and enemy
# First find all its move
# Now check each move.
# If taking a move leaves my king in check skip it otherwise put it in legalMoves
# Moves must be LEGAL
def getLegalPieceMovesSeperately(board,pieceLocation,turn):
    empty,enemy=getPieceMovesSeperately(board,pieceLocation,turn)

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

# returns legal moves for a particular Piece NOT seperated into empty and enemy
# Moves must be LEGAL
def getLegalPieceMoves(board,pieceLocation,turn):
    empty,enemy=getLegalPieceMovesSeperately(board,pieceLocation,turn)
    return empty+enemy

# returns legal moves for a all Pieces of the color with current turn seperated into empty and enemy
# Moves must be LEGAL
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

# returns legal moves for a all Pieces of the color with current turn NOT seperated into empty and enemy
# Moves must be LEGAL
def getAllLegalMoves(board,turn):
    legalEmpty,legalEnemy=getAllLegalMovesSeperately(board,turn)
    return legalEmpty+legalEnemy


# Checks if checkmate 
# if king in check and no legal moves checkmate otherwise not checkmate
#
# Returns (bool)
def isCheckMate(board,turn):
    king_x,king_y=findMyKing(board,turn)
    if  len(cellInCheck(board,(king_x,king_y),turn))>0:
        legal_moves=getAllLegalMoves(board,turn)
        if len(legal_moves)==0:
            return True
    return False

# Checks if stalemate 
# if king not in check and no legal moves stalemate otherwise not stalemate
#
# Returns (bool)
def isStaleMate(board,turn):
    king_x,king_y=findMyKing(board,turn)
    if  len(cellInCheck(board,(king_x,king_y),turn))==0:
        legal_moves=getAllLegalMoves(board,turn)
        if len(legal_moves)==0:
            return True
    return False