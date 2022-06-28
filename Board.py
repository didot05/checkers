# Board.py
import Men
from Constants import *



class Board:
    # Class for initial Board of checkers game.
    def __init__(self):
        self.size_board = int(SIZE_BOARD)
    # Draw a checkers 2D board with 8 col and 8 rows.
    def create_board(self):
        # Make an empty 2D list & Men token objects on the board.
        new_board = [[None for j in range(self.size_board)] for i in range(self.size_board)]
        for i in range(self.size_board // 2 - 1):
            for j in range(0, self.size_board, 2):
                # Give the WHITE (for ai) tokens for initial state of checkers game.
                new_board[i][j + i % 2] = Men.Men(i, j + i % 2, WHITE)
        for i in range(self.size_board // 2 + 1, self.size_board):
            for j in range(0, self.size_board, 2):
                # Give the RED (for player) tokens for initial state of checkers game.
                new_board[i][j + i % 2] = Men.Men(i, j + i % 2, RED)
        # Return the 2D board structure data and positions of Men token objects.        
        return new_board
