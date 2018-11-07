from SnakeHeuristics import getSimpleOrderedMoveList
from SnakeHeuristics import simpleMove2

# Performs an iterative deepening negamax search.  Returns best move for current state and value assosicated
def negamaxIDS(game, maxDepth):
    bestValue = 999999
    bestMove = 'q'
    # bestMove = game.getMoves()[0]
    for depth in range(1, maxDepth+1):
        value, move = negamax(game, depth)
        
        if value == 0: # Found winning move, so return it
            return value, move
        elif value < bestValue: # Found a new best move
            bestValue = value
            bestMove = move

    if bestMove == 'q' or bestMove == None:
        return 666, simpleMove2(game)
    else:
        return bestValue, bestMove


# Returns the best move for the current state of the game and the value associated
def negamax(game, depthLeft):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None  # call to negamax knows the move

    bestValue = 999999
    bestMove = None
    for move in getSimpleOrderedMoveList(game):
        game.makeMove(move)
        value, _ = negamax(game, depthLeft-1)
        game.unmakeMove()
        
        if value < bestValue:
            bestValue = value
            bestMove = move
    
    return bestValue, bestMove