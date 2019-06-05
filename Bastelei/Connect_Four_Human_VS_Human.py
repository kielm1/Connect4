import numpy as np
import time
import random
import sys
import math
import pygame



# Status of gamefield
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
PLAYER2 = 1
EMPTY = 0
PLAYER_PIECE = 1
PLAYER2_PIECE = 2


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
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def doMove(board, row, col, piece):
	board[row][col] = piece

def possibleMove(board, col):
	return board[ROW_COUNT-1][col] == 0

def getNextOpenRaw(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def printTerminal(board):
	print(np.flip(board, 0))


def winningMove(board, piece):  # Check if there is a Four-in-a-row

	# Checkw vertical locations for for FourInARow
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
				c] == piece:
				return True

	# Checks horizontal locations for FourInARow
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
				c + 3] == piece:
				return True

	# Check negatively sloped diaganols for FourInARow
	for c in range(COLUMN_COUNT - 3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
				c + 3] == piece:
				return True

	# Check positively sloped diaganols for FourInARow
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
				c + 3] == piece:
				return True

def evaluateLine(line, piece): #line: A Line of four piece, connected either Horicontal, vertical or diagonal
	score = 0
	enemyPiece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		enemyPiece = PLAYER2_PIECE
	if line.count(piece) == 4:
		score += scorecard[0]
	elif line.count(piece) == 3 and line.count(EMPTY) == 1:
		score += scorecard[1]
	elif line.count(piece) == 2 and line.count(EMPTY) == 2:
		score += scorecard[2]

	if line.count(enemyPiece) == 3 and line.count(EMPTY) == 1: # Attention Needed, Hat manchmal Aussete, muss wohl noch hoch
		score -= scorecard[3]

	return score

def evaluate(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			line = row_array[c:c + 4]
			score += evaluateLine(line, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			line = col_array[r:r + 4]
			score += evaluateLine(line, piece)

	## Score sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			line = [board[r + i][c + i] for i in range(4)]
			score += evaluateLine(line, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			line = [board[r + 3 - i][c + i] for i in range(4)]
			score += evaluateLine(line, piece)

	return score

def isTerminal(board): # Checks if one Player won or no Moves are left
	return winningMove(board, PLAYER_PIECE) or winningMove(board, PLAYER2_PIECE) or len(getAllMoves(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	validLocations = getAllMoves(board)  #Get all possible Locations
	is_terminal = isTerminal(board)	# Check if theres a move left
	if depth == 0 or is_terminal:			# Break condition
		if is_terminal:
			if winningMove(board, PLAYER2_PIECE):
				return (None, 100000000000000)
			elif winningMove(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, evaluate(board, PLAYER2_PIECE)) #Return the Score

	if maximizingPlayer:
		value = -math.inf
		column = random.choice(validLocations) #If all options are equal, take a random choice
		for col in validLocations:	# Go through all the possible Colums
			row = getNextOpenRaw(board, col)
			b_copy = board.copy()
			doMove(b_copy, row, col, PLAYER2_PIECE) # Drop the AI piece on the temp Board
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1] # Run the minmax with depth -1 and Minimizing player, get the score
			if new_score > value: #S tore the newScore and the colum if its bigger than the old one
				value = new_score
				column = col
			alpha = max(alpha, value) # Define new Alpha when lesser than the newScore
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(validLocations) #If all options are equal, take a random choice
		for col in validLocations:
			row = getNextOpenRaw(board, col)
			b_copy = board.copy()
			doMove(b_copy, row, col, PLAYER_PIECE) # Drop the Human piece on the temp Board
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1] #Run the minmax again with depth -1 and Maximizing player
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value) # Define new Beta when greater than the newScore
			if alpha >= beta:
				break
		return column, value


#Return an array with all possible COLUMS to set a stone
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
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == PLAYER2_PIECE:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = setStartState()
gameOver = False

pygame.init()



screen = pygame.display.set_mode(size)
printGUI(board)
pygame.display.update()
myfont = pygame.font.SysFont("helvetica", 48)

turn = random.randint(PLAYER, PLAYER2) # Randomly choose the starting player

while not gameOver: #Game Loop

	# Human Player Input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER: 
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else:
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if possibleMove(board, col):
					row = getNextOpenRaw(board, col)

					if turn == PLAYER:
						doMove(board, row, col, PLAYER_PIECE)
						if winningMove(board, PLAYER_PIECE):
							label = myfont.render("Player 1 wins!!", 1, RED)
							screen.blit(label, (40, 10))
							gameOver = True

					else:
						doMove(board, row, col, PLAYER2_PIECE)
						if winningMove(board, PLAYER2_PIECE):
							label = myfont.render("Player 2 wins!!", 1, RED)
							screen.blit(label, (40, 10))
							gameOver = True


					turn += 1
					turn = turn % 2 #Turn even => Human, Turn odd => AI


					#printTerminal(board)
					printGUI(board)

			else:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if possibleMove(board, col):
					row = getNextOpenRaw(board, col)
					doMove(board, row, col, PLAYER2_PIECE)

					if winningMove(board, PLAYER2_PIECE):
						label = myfont.render("Player 2 wins!!", 1, RED)
						screen.blit(label, (40,10))
						gameOver = True

					turn += 1
					turn = turn % 2 #Turn even => Human, Turn odd => AI

					#printTerminal(board)
					printGUI(board)


	if gameOver:
		print("The game is over!")
		pygame.time.wait(10000)