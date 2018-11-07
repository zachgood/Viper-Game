######################################################################################################################
## simple heuristic
######################################################################################################################

# 1
# first working simple move
def simpleMove1(snakeGame):
    # bestMove = 'q'
    bestMove = 'w'
    smallest = 999
    
    # save head
    saveHead = snakeGame.iHead
    
    # for move in moves
    for m in snakeGame.getMoves():
        # save move
        rowMove = snakeGame.iHead[0]
        colMove = snakeGame.iHead[1]
        
        # set head
        if m == 'w': # up
            rowMove = rowMove-1 if (rowMove != 0) else 9
        elif m == 's': # down
            rowMove = rowMove+1 if (rowMove != 9) else 0
        elif m == 'a': # left
            colMove = colMove-1 if (colMove != 0) else 9
        elif m == 'd': # right
            colMove = colMove+1 if (colMove != 9) else 0
        # set
        snakeGame.iHead = (rowMove, colMove)
        
        
        if snakeGame.getDist() < smallest:
            # if dist is smaller than smallest, set smallest/bestmove
            smallest = snakeGame.getDist()
            bestMove = m
        
        # reset head
        snakeGame.iHead = saveHead
        
    snakeGame.iHead = saveHead
        
    # return best move
    return bestMove

# 2
# Returns list of moves orded (acending) by manhattin distance (of head to apple) achieved by making that move
def getSimpleOrderedMoveList(snakeGame):
    mList = snakeGame.getMoves()
    vList = []
    for m in mList:
        snakeGame.makeMove(m)
        vList = vList + [snakeGame.getUtility()]
        snakeGame.unmakeMove()
    return [x for _,x in sorted(zip(vList,mList))]

def simpleMove2(snakeGame):
    return getSimpleOrderedMoveList(snakeGame)[0]

# 3
# return move thats next in sequence to loop board
def loopingMove(snakeGame):
    #if snakeGame.iHead in [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9)]
    if snakeGame.iHead[0] == snakeGame.iHead[1]:
        return 'd'
    else:
        return 'w'