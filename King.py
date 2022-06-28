# King.py
from Constants import *
from Token import Token



class King(Token):
    # Class for King token. 
    # For King token's advanced move different from men token.
    def is_capture_available(self, board, tile_y, tile_x):
        if tile_y < self.posy:
            token_position_y = self.posy - 1
        else:
            token_position_y = self.posy + 1
        token_position_x = int((self.posx + tile_x) / 2)

        if abs(self.posx - tile_x) == 2 and abs(self.posy - tile_y) == 2 and not isinstance(board[tile_y][tile_x], Token):
            if isinstance(board[token_position_y][token_position_x], Token) and board[token_position_y][token_position_x].calc_color() != self.color:
                return True
            else:
                return False
        else:
            return False

    # func for capturing move.
    def capture_token(self, board, tile_y, tile_x):
        if tile_y < self.posy:
            token_position_y = self.posy - 1
        else:
            token_position_y = self.posy + 1
        token_position_x = int((self.posx + tile_x) / 2)
        # remove the token on the ([token_position_y][token_position_x]) tile if that is captured. 
        board[token_position_y][token_position_x] = None
        board[self.posy][self.posx], board[tile_y][tile_x] = board[tile_y][tile_x], board[self.posy][self.posx]
        self.posy = tile_y
        self.posx = tile_x

    # Confirm the it is valid move or not.
    def is_possible_move(self, board, tile_y, tile_x):
        if isinstance(board[tile_y][tile_x], Token):
            return False
        if abs(self.posy - tile_y) == 1 and abs(self.posx - tile_x) == 1:
            return True
        else:
            return False
        