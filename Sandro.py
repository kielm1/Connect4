from pickle import TRUE
from pprint import pprint
import config as c
import numpy as np
import time
import random
import sys
import math

#==================================================#
#                                                  #
#   INTERFACE PLAYER                               #
#                                                  #
#==================================================#
class Player:
    #def setStartState(self):
    #     raise NotImplementedError("You should have implemented this")
    #
     def setFirstPlayer(self):
         raise NotImplementedError("You should have implemented this")
    #
     def setSecondPlayer(self):
         raise NotImplementedError("You should have implemented this")
    #
    # def setThirdPlayer(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def getNextMove(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def isLegalMove(self, mv):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def doMove(self, mv):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def isStateTerminal(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def firstPlayerToMove(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def secondPlayerToMove(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def firstPlayerToWin(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def secondPlayerToWin(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def showGamestate(self):
    #     raise NotImplementedError("You should have implemented this")

#==================================================#
#                                                  #
#   INTERFACE GAMESTATE                            #
#                                                  #
#==================================================#
class Gamestate:

     def setStartState(self):
         raise NotImplementedError("You should have implemented this")
    #
    # def getAllMoves(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def possibleMove(self, mv):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def hasNextMove(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def getNextMove(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def doMove(self, mv):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def undoMove(self, mv):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def getAllChildStates(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def hasNextChild(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def getNextChild(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def getChild(self, mv):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def firstPlayerToMove(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def secondPlayerToMove(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def isTerminal(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def firstPlayerToWin(self):
    #     raise NotImplementedError("You should have implemented this")
    #
    # def secondPlayerToWin(self):
    #     raise NotImplementedError("Not implemented")
    #
    # def draw(self):
    #     raise NotImplementedError("Not implemented")
    #
    # def getMoveHistory(self):
    #     raise NotImplementedError("Not implemented")
    #
    # def getStateHistory(self):
    #     raise NotImplementedError("Not implemented")

class ConnectFourState(Gamestate):

    def __init__(self):
        pass

    def setStartState(self):
        return np.zeros((c.ROWS, c.COLS))




class Board:
    # 7x6 Game Board
    #
    # 5 . . . . . . .
    # 4 . . . . . . .
    # 3 . . . . . . .
    # 2 . . . . . . .
    # 1 . . . . . . .
    # 0 . . . . . . .
    #   0 1 2 3 4 5 6
    #

    def __init__(self):
        self.board = []
        self.state = ConnectFourState()
        self.reset()
        self.drawBoard()

    def reset(self):
        """
        Sets up an empty 7X6 board
        :return:
        """
        self.board = self.state.setStartState()

    def drawBoard(self):
        pprint(self.board)



class ConnectFourPlayer(Player):

    def __init__(self):
        pass

    def setFirstPlayer(self):
        self.firstplayer = TRUE

    def setSecondPlayer(self):
        self.secondplayer = TRUE

class GameManager():

    def __init__(self):
        pass

if __name__ == "__main__":
    board = Board()