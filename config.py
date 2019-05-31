
#KI Settings
DEPTH = 5 # Difficulty => How deep shall the AI search

# The score for:
# - [0]: line of 4 own Pieces
# - [1]: line of 3 own Pieces and 1 empty
# - [2]: line of 2 own Pieces and 2 empty
# - [3]: line of 3 enemy Pieces and 1 empty (counts negative)

scorecard = [1000, 5, 2, 7]
# Original Scorecard: Spielt gut, hat aber selten Aussetzter beim erkennen von horizontalen 4er
# scorecard = [1000, 5, 2, 4]

# Status of gamefield
ROWS = 6
COLS = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2


# Display Settings
SQUARESIZE = 70
width = COLS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
# Colors
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)