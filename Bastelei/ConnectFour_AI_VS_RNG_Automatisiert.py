import numpy as np

import random

import math
import pygame

'''

Two AI's play C4. Just a testclass with no GUI. 


'''

#How many rounds shall the bots play?
AMOUNT_ROUND = 10

#AI Settings
DEPTH_AI1 = 4  # How deep shall the AI1 search

scorecardAI1 = [1000, 5, 3, 5]
# The score for:
# - [0]: line of 4 own Pieces
# - [1]: line of 3 own Pieces and 1 empty
# - [2]: line of 2 own Pieces and 2 empty
# - [3]: line of 3 enemy Pieces and 1 empty (counts negative)
# Original Scorecard: Spielt gut, hat aber selten Aussetzter beim erkennen von horizontalen 4er
# scorecard = [1000, 5, 2, 4]
print("The Settings are: Depth Ai1:", DEPTH_AI1, " AI 2 is random:")


# Status of gamefield
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = 0
AI1_PIECE = 1
AIRng_PIECE = 2


# Display Settings
SQUARESIZE = 70
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
# Colors
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)


def setStartState():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def doMove(board, row, col, piece):
    board[row][col] = piece


def possibleMove(board, col):
    return board[ROW_COUNT - 1][col] == 0


def getNextOpenRaw(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def printTerminal(board):
    print(np.flip(board, 0))


def winningMove(board, piece):  # Check if there is a Four-in-a-row
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def evaluateLine(line, piece):
    score = 0
    enemyPiece = AI1_PIECE
    scorecard = scorecardAI1



    if piece == AI1_PIECE:
        enemyPiece = AIRng_PIECE
    if line.count(piece) == 4:
        score += scorecard[0]
    elif line.count(piece) == 3 and line.count(EMPTY) == 1:
        score += scorecard[1]
    elif line.count(piece) == 2 and line.count(EMPTY) == 2:
        score += scorecard[2]

    if line.count(enemyPiece) == 3 and line.count(
            EMPTY) == 1:  # Attention Needed, Hat manchmal Aussete, muss wohl noch hoch
        score -= scorecard[3]

    return score


def evaluate(board, piece):
    score = 0

    ## Score center column => Counts more since
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3   # Seems bad

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            line = row_array[c:c + 4]
            score += evaluateLine(line, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            line = col_array[r:r + 4]
            score += evaluateLine(line, piece)

    ## Score sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            line = [board[r + i][c + i] for i in range(4)]
            score += evaluateLine(line, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            line = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluateLine(line, piece)

    return score


def isTerminal(board):  # Checks if one Player won or no Moves are left
    return winningMove(board, AI1_PIECE) or winningMove(board, AIRng_PIECE) or len(getAllMoves(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    validLocations = getAllMoves(board)  # Get all possible Locations
    is_terminal = isTerminal(board)  # Check if theres a move left
    if depth == 0 or is_terminal:  # Break condition
        if is_terminal:
            if winningMove(board, AIRng_PIECE):
                return (None, 100000000000000)
            elif winningMove(board, AI1_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, evaluate(board, AIRng_PIECE))  # Return the Score

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(validLocations)  # If all options are equal, take a random choice
        for col in validLocations:  # Go through all the possible Colums
            row = getNextOpenRaw(board, col)
            b_copy = board.copy()
            doMove(b_copy, row, col, AIRng_PIECE)  # Drop the AI piece on the temp Board
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[
                1]  # Run the minmax with depth -1 and Minimizing player, get the score
            if new_score > value:  # S tore the newScore and the colum if its bigger than the old one
                value = new_score
                column = col
            alpha = max(alpha, value)  # Define new Alpha when lesser than the newScore
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(validLocations)  # If all options are equal, take a random choice
        for col in validLocations:
            row = getNextOpenRaw(board, col)
            b_copy = board.copy()
            doMove(b_copy, row, col, AI1_PIECE)  # Drop the AI piece on the temp Board
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[
                1]  # Run the minmax again with depth -1 and Maximizing player
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)  # Define new Beta when greater than the newScore
            if alpha >= beta:
                break
        return column, value


# Return an array with all possible COLUMS to set a stone
def getAllMoves(board):
    validLocations = []
    for col in range(COLUMN_COUNT):
        if possibleMove(board, col):
            validLocations.append(col)

    return validLocations


def pickBestMove(board, piece):
    validLocations = getAllMoves(board)
    best_score = -10000
    best_col = random.choice(validLocations)
    for col in validLocations:
        row = getNextOpenRaw(board, col)
        tempBoard = board.copy()
        doMove(tempBoard, row, col, piece)
        score = evaluate(tempBoard, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def printGUI(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == AI1_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AIRng_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()




roundcounter= 1
wincounterAI1 = 0
wincounterAI2 = 0

#Gameloop
for x in range(1,AMOUNT_ROUND):

    print ("round ", x)

    turn = 0  # No random turns for AI vs AI
    board = setStartState()
    gameOver = False

    pygame.init()

    while not gameOver:  # Game Loop

        # Human Player Input
        # AI 1 Input
        if turn == PLAYER and not gameOver:
            col, minimax_score = minimax(board, DEPTH_AI1, -math.inf, math.inf, True)

            if possibleMove(board, col):
                row = getNextOpenRaw(board, col)
                doMove(board, row, col, AI1_PIECE)

                if winningMove(board, AI1_PIECE):
                    wincounterAI1 = wincounterAI1+1
                    # Don't print anything => to much spam
                    #print("AI 1 Sieg mit folgender Stellung:")
                    #printTerminal(board)
                    gameOver = True

                # printTerminal(board)
                # printGUI(board)

                turn += 1
                turn = turn % 2

        # AI 2 Input
        if turn == AI and not gameOver:
            validLocations = getAllMoves(board)
            col = random.choice(validLocations)
            row = getNextOpenRaw(board, col)
            doMove(board, row, col, AIRng_PIECE)

            if winningMove(board, AIRng_PIECE):
                wincounterAI2 = wincounterAI2 + 1
                print("OOOBACHT: Random AI Sieg !!! Anzahl Siege: ", wincounterAI2, "! mit folgender Stellung:")
                printTerminal(board)
                gameOver = True

                # printTerminal(board)
                # printGUI(board)
            turn += 1
            turn = turn % 2  # Turn even => Human, Turn odd => AI

        if gameOver:
            #
            #print("Runde beendet. AI1:", wincounterAI1, "  AI2:", wincounterAI2)
            #pygame.time.wait(10000)
            board = setStartState()

print("finished. AI1 Wins:" ,wincounterAI1, " RNG Wins: ", wincounterAI2)