# Token.py
from Constants import *



class Token:
    # Class for handle the general value for token.
    def __init__(self, posy, posx, color):
        self.posy = posy
        self.posx = posx
        self.color = color
        # if the token's color is white(used by AI player), since white token's position is top side of the board, direction becomes -1 (go down)
        if self.color == WHITE:
            self.direction = -1 # row - 1 
        # if the token's color is black(used by human player), since white token's position is down side of the board, direction becomes +1 (go up)    
        else:
            self.direction = 1 # row + 1 

    # return the color value of the token.
    def calc_color(self):
        return self.color

    # Calculate the possible moves of tokens on given tile through iterate sublists of the board.
    def calc_possible_moves(self, board):
        # store the each position of possible moves.
        possible_moves = []
        for tile_x in range(len(board)):
            column = []
            for tile_y in range(len(board)):
                proper_move = board[self.posy][self.posx].is_possible_move(board, tile_x, tile_y)
                column.append(proper_move)
            possible_moves.append(column)
        return possible_moves

    # Calculate the possible capture moves of tokens on given tile through iterate sublists of the board.
    def calc_possible_captures(self, board):
        # store the each position of possible capture moves.
        possible_captures = []
        for tile_x in range(len(board)):
            column = []
            for tile_y in range(len(board)):
                proper_capture = board[self.posy][self.posx].is_capture_available(board, tile_x, tile_y)
                column.append(proper_capture)
            possible_captures.append(column)
        return possible_captures

    # Calculate the all possible moves of tokens on given tile through iterate sublists of the board.
    # Return the boolean value that is indicate the capturing move is possible or not.
    def calc_all_possible_moves(self, board):
        # Get the possible captures move.
        possible_captures = self.calc_possible_captures(board)
        if any(True in sublist for sublist in possible_captures):
            capture = True
            return possible_captures, capture
        # Get the possible move.
        else:
            possible_moves = self.calc_possible_moves(board)
            capture = False
            return possible_moves, capture

    # Check the whether the move is valid or not.
    def is_possible_move(self, board, tile_y, tile_x):
        if isinstance(board[tile_y][tile_x], Token):
            return False
        if self.posy - tile_y == self.direction and abs(self.posx - tile_x) == 1:
            return True
        else:
            return False

    # Update the state of board data structure and the token's updated position.
    def make_move(self, board, tile_y, tile_x):
        board[self.posy][self.posx], board[tile_y][tile_x] = board[tile_y][tile_x], board[self.posy][self.posx]
        self.posy = tile_y
        self.posx = tile_x

    def can_token_capture(self, board):
        possible_captures = []
        for tile_x in range(len(board)):
            column = []
            for tile_y in range(len(board)):
                proper_capture = board[self.posy][self.posx].is_capture_available(board, tile_x, tile_y)
                column.append(proper_capture)
            possible_captures.append(column)

        if any(True in sublist for sublist in possible_captures):
            return True
        else:
            return False


