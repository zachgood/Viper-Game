import pandas as pd
import numpy as np
import pickle
import matplotlib
import matplotlib.pyplot as plt
from random import randint

from IPython.display import clear_output
import sys, select

class Snake(object):
    
    def __init__(self):
        self.board = np.zeros((10, 10), dtype=str)    # 10x10 board
        self.board[:] = ' '                           # set white space
        self.iApple = (randint(0,8), randint(0,9))    # set index of apple '#'  - anywhere but bottom row
        self.iHead = (9, randint(0,9))                # set index of head  'O'  - anywhere on bottom row
        self.aBody = []                               # set indexs of body '+'  - empty to start
        self.hitAppleOnLastMove = False               # keep track of last move - used in move head
        self.stateList = [self.getState()]            # keep track of all states/moves - used in move/unmakemove
    
    # NOTE: state list is managed by make move and unmake move exclusively  
    def getState(self):
        return (self.iApple, self.iHead, tuple(self.aBody), self.hitAppleOnLastMove)
    
    # NOTE: state list is managed by make move and unmake move exclusively
    def setState(self, state):
        self.iApple = state[0]
        self.iHead = state[1]
        self.aBody = list(state[2])
        self.hitAppleOnLastMove = state[3]

# GETS ------------
    # returns (row,col) of head
    def getHead(self):
        return self.iHead
    
    # returns (row,col) of apple
    def getApple(self):
        return self.iApple
    
    # returns length of body (i.e. count apples eatten)
    def getBodyLength(self):
        return len(self.aBody)

# SETS ------------ (should prob be private)
    # places pieces in their spot on the board. only used before printing
    def setupBoard(self):
        self.board[:] = ' '                # set all to empty
        self.board[self.iApple] = '#'      # place apple
        for part in self.aBody:
            self.board[part] = '+'         # place body part - needs to be before head for case when apple is eatten
        self.board[self.iHead] = 'O'       # place head
        return self
    
    # sets apple at random empty spot
    def setRandomApple(self):
        newiApple = (randint(0,9), randint(0,9))
        # make sure new apple is set to empty spot
        while( (newiApple in self.aBody) or (newiApple == self.iHead) ):
            newiApple = (randint(0,9), randint(0,9))
        self.iApple = newiApple # set apple - anywhere but bottom row
        return self
    
    # is in charge of moving entire snake forward one space.
    def moveHead(self, move):
        if self.iHead == move: # TODO: ADD CASE FOR WHEN MOVE IS SAME AS IHEAD i.e. move wasnt made
            return self
        hitApple = (move == self.iApple)               # True if move makes snake eat apple. False otherwise
        hitBody = (move in self.aBody)                 # True if move makes snake hit body. False otherwise
        # TODO: maybe add case for collision
        #if hitBody:
            #raise ValueError('HIT BODY - GAME OVER!')
        
        if not self.hitAppleOnLastMove:
            self.aBody = [self.iHead] + self.aBody         # move front of body forward one space
            self.aBody = self.aBody[:-1]                   # move back of body forward one space
        if hitApple:
            self.hitAppleOnLastMove = True
            self.aBody = [move] + self.aBody           # add body part at move
            self.setRandomApple()                      # move apple to new random location if apple was eatten
        else:
            self.hitAppleOnLastMove = False
        
        self.iHead = move
        return self

    
# MOVES ------------
    # returns valid moves (up, down, left, right) that dont cause collision
    def getMoves(self):
        # return ['w','s','a','d']
        validMoves = []
        
        curRow = self.iHead[0]
        curCol = self.iHead[1]
        
        rowUp = curRow-1 if (curRow != 0) else 9
        rowDown = curRow+1 if (curRow != 9) else 0
        colLeft = curCol-1 if (curCol != 0) else 9
        colRight = curCol+1 if (curCol != 9) else 0
        
        if (rowUp, curCol) not in self.aBody:
            validMoves += ['w']
        if (rowDown, curCol) not in self.aBody:
            validMoves += ['s']
        if (curRow, colLeft) not in self.aBody:
            validMoves += ['a']
        if (curRow, colRight) not in self.aBody:
            validMoves += ['d']

        return validMoves
    
    def makeMove(self, move):
        rowMove = self.iHead[0]
        colMove = self.iHead[1]
        
        if move == 'q': # quit
            raise ValueError('YOU QUIT THE GAME! SCORE:', len(self.aBody))
            
        elif move == 'p': # print current state of board
            self.printState()
            return self
            
        elif move == 'h': # print moves and navigation options
            self.printMoves()
            self.printNav()
            return self
        
        elif move == 'u': # unmake last move
            self.unmakeMove()
            return self
            
        elif move == 'w': # up
            rowMove = rowMove-1 if (rowMove != 0) else 9
                
        elif move == 's': # down
            rowMove = rowMove+1 if (rowMove != 9) else 0
                
        elif move == 'a': # left
            colMove = colMove-1 if (colMove != 0) else 9
                
        elif move == 'd': # right
            colMove = colMove+1 if (colMove != 9) else 0
        
        if move in ['w', 's', 'a', 'd']:
            self.moveHead((rowMove, colMove))
            self.stateList = [self.getState()] + self.stateList
            self.stateList = self.stateList[:50] # keep max of 50 states in list
        return self
    
    # Will set game back one state
    def unmakeMove(self):
        if len(self.stateList) == 1:
            raise ValueError("Snake Game Error: Cant unmake move from first state!")
        self.setState(self.stateList[1])
        self.stateList = self.stateList[1:]
        self.stateList = self.stateList[:50] # keep max of 50 states in list
        return self
    
    
# SEARCH HELPERS ---------------
    # returns manhattan dist btw head & apple. returns big number if collisioin occured
    def getDist(self):
        return abs(self.iApple[0] - self.iHead[0]) + abs(self.iApple[1] - self.iHead[1])
    
    # Returns True if hit apple or hit body
    def isOver(self):
        return len(self.getMoves()) == 0
    
    # Utility used in negamax
    def getUtility(self):
        if self.hitAppleOnLastMove:
            return 0
        elif self.iHead in self.aBody:
            return 9999
        else:
            return self.getDist()
    

# GRAPHICS -----------------
    # Print state of game - used for debugging
    def printState(self):
        print('Apple is at', self.iApple)
        print('Head is at', self.iHead)
        print('Body is at', self.aBody)
        
    def printLogo(self):
        print('████████████████████████████████████████████████████████████████████████████████████████████████████')
        print('██████████████████████   + + + + + + + + + + + + + + + + + + + + + + + + + +  ██████████████████████')
        print('██████████████████████   +  =======  ||\   ||     //\\\     || // ||=====   +  ██████████████████████')
        print('██████████████████████   +  ||       ||\\\  ||    //  \\\    ||//  ||        +  ██████████████████████')    
        print('██████████████████████   +  =======  || \\\ ||   //====\\\   ||/   ||====    +  ██████████████████████')    
        print('██████████████████████   +        || ||  \\\||  //      \\\  ||\\\  ||        +  ██████████████████████')    
        print('██████████████████████   +  =======  ||   \|| //        \\\ || \\\ ||=====   +  ██████████████████████')    
        print('██████████████████████   + + + + + + + + + + + + + + + + + + + + + + O  #     ██████████████████████')
        print('█████████████████████████████████████████████████████████████████████████████████████████████ ® 2018')


    def printGameInfo(self):
        info = []
        # objective 
        info.append('█ OBJECTIVE: make snake eat apples')
        # rules
        info.append('\n█ RULES: ')
        info.append('\t1. for every apple eatten, the snake will grow a body part')
        info.append('\t2. dont run into body, game over')
        # pices
        info.append('\n█ PICES: ')
        info.append('\tsnake = "O"')
        info.append('\tapple = "#"')
        info.append('\tbody = "+"')
        
        for line in info:
            print(line)
        self.printMoves()
        self.printNav()
        return
    
    def printMoves(self):
        info = []
        # moves
        info.append('\n█ MOVES: note - press enter (return) after each move (change later) ')
        info.append('\t"w" - move up')
        info.append('\t"s" - move down')
        info.append('\t"a" - move left')
        info.append('\t"d" - move right')
        for line in info:
            print(line)
        return
        
    def printNav(self):
        info = []
        # game navigation
        info.append('\n█ START GAME: "g"')
        info.append('█ QUIT GAME: "q"')
        info.append('█ PRINT STATE: "p"')
        info.append('█ HELP: "h"')
        info.append('█ RESTART GAME: "r"')
        for line in info:
            print(line)
        return
        
        
    # To string
    def __str__(self):
        self.setupBoard() # place all pieces on board
        top = '______________________\n' # should i add new line?
        bottom = '\n⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻' # should i add new line?
        boardData = []
        rowIndex = 0
        for row in self.board:
            boardData.append('| {} {} {} {} {} {} {} {} {} {} |'.format(*row))
            rowIndex += 1
        printBoard = top + '\n'.join(boardData) + bottom
        return printBoard