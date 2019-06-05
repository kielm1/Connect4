from pickle import TRUE
from pprint import pprint
import config as c
import numpy as np
import pygame
import time
import random
import sys
import math



# ==================================================#
#                                                  #
#   INTERFACE PLAYER                               #
#                                                  #
# ==================================================#
class Player:
    pass
#     def setStartState(self):
#         raise NotImplementedError("You should have implemented this")

#    def setFirstPlayer(self):
#        raise NotImplementedError("You should have implemented this")

    #
#    def setSecondPlayer(self):
#        raise NotImplementedError("You should have implemented this")


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

# ==================================================#
#                                                  #
#   INTERFACE GAMESTATE                            #
#                                                  #
# ==================================================#
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
        self.board = []
        self.setStartState()

    def setStartState(self):
        return np.zeros((c.ROWS, c.COLS))


class Board:
    # 7x6 Game Board
    #
    # 0 . . . . . . .
    # 1 . . . . . . .
    # 2 . . . . . . .
    # 3 . . . . . . .
    # 4 . . . . . . .
    # 5 . . . . . . .
    #   0 1 2 3 4 5 6
    #

    def __init__(self):
        self.board = self.create_board(c.ROWS, c.COLS)
        self.state = ConnectFourState()
        #self.reset()
        self.draw_board()

    def reset(self):
        """
        Sets up an empty 7X6 board
        :return:
        """
        self.board = self.state.setStartState()

    def __len__(self):
        return len(self.board)

    def create_board(self, rows, cols):
        """
        creates empty Connect 4 Board
        :param rows: num of rows
        :param cols: num of cols
        :return: empty board
        """
        self.board = []
        for row in range(rows):
            board_row = []
            for col in range(cols):
                board_row.append(c.EMPTY)
            self.board.append(board_row)
        return self.board

    def draw_board(self):
        """ Prints Connect 4 board """
        labels = "1234567"
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print("", " ".join(labels))

    def drop_piece(self, input, piece):
        """
        Drops piece at specified col, return board if succeeds, False otherwise
        """
        for row in self.board:
            for col in self.board:
                peek = self.peek(input)

                if row[input] == c.EMPTY:
                    row[input] = piece
                    return True
        return False

    def is_col_full(self):
        pass

    def peek(self, col):
        """
        returns the top empty position of the given column
        :param col:
        :return:
        """
        # check param col
        #if col < 0 or col > 6:
        #    raise ValueError('Paramteter col must be between 0 and 6')
        for row in self.board:
            if row[col] == c.EMPTY:
                row[col] = 'test'
                return row[col]
        return 0



class ConnectFourPlayer(Player):

    def __init__(self):
        pass


class GameManager():

    def __init__(self):
        pass


if __name__ == "__main__":
    board = Board()

    board.drop_piece(1, c.PLAYER_PIECE)
    board.draw_board()

    time.sleep(2)
    board.drop_piece(2, c.PLAYER_PIECE)
    board.draw_board()

    time.sleep(2)
    board.drop_piece(5, c.PLAYER_PIECE)
    board.draw_board()