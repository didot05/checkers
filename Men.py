# Men.py
from Constants import *
from Token import Token
from King import King



class Men(Token):
    # Class for men token.
    # For men token's move different from King token.
    def __init__(self, posy, posx, color):
        # Constructor of the men class.
        super().__init__(posy, posx, color)
        # if the token's color is white(used by AI player), since white token's position is top side of the board, direction becomes -1 (go down)
        if self.color == WHITE:
            self.direction = -1
        # if the token's color is black(used by human player), since white token's position is down side of the board, direction becomes +1 (go up)
        else:
            self.direction = 1
        self.size_board = int(SIZE_BOARD)

    # Check that there are possible capture move exist or not on given tile. 
    def is_capture_available(self, board, tile_y, tile_x):
        token_position_y = self.posy - self.direction
        token_position_x = int((self.posx + tile_x) / 2)
        if abs(self.posx - tile_x) == 2 and self.posy - tile_y == 2 * self.direction and not isinstance(board[tile_y][tile_x], Token):
            if isinstance(board[token_position_y][token_position_x], Token) and board[token_position_y][token_position_x].calc_color() != self.color:
                return True
            else:
                return False
        else:
            return False
    
    # If the men token reach some rule(ex. reach to the king col), men token becomes King token.     
    def king_conversion_men(self, board):
        board[self.posy][self.posx] = King(self.posy, self.posx, self.color)      

    # Function for capturing the enemy's token.
    # Update the Board data structure and token's position data (posy, posx) according to capturing move made.
    def capture_token(self, board, tile_y, tile_x):        
        captured_token_position_y = self.posy - self.direction
        captured_token_position_x = int((self.posx + tile_x) / 2)
        
        # Regicide; if men token manages to capture a king, it is instantly become a king. 
        # check the captured token is King token or not.   
        if(isinstance(board[captured_token_position_y][captured_token_position_x], King)):
            # remove the token on the ([captured_token_position_y][captured_token_position_x]) tile if that is captured. 
            board[captured_token_position_y][captured_token_position_x] = None
            board[self.posy][self.posx], board[tile_y][tile_x] = board[tile_y][tile_x], board[self.posy][self.posx]
            # Update the token's position data (posy, posx).
            self.posy = tile_y
            self.posx = tile_x
            # Regicide; if men token captured King token, men token can be the King token.
            self.king_conversion_men(board) 
        
        # non-Regicide
        else:
            # remove the token on the ([captured_token_position_y][captured_token_position_x]) tile if that is captured. 
            board[captured_token_position_y][captured_token_position_x] = None
            # Update the token's position data (posy, posx).
            board[self.posy][self.posx], board[tile_y][tile_x] = board[tile_y][tile_x], board[self.posy][self.posx]
            self.posy = tile_y
            self.posx = tile_x

    # Check that the men token should become King token or not.
    def check_for_king_conversion(self, board): #def check_for_king_conversion(self, board):
        # if WHITE men token reach to the King col become a white king token with king_conversion_men func
        if self.posy == self.size_board - 1 and self.color is WHITE:
            self.king_conversion_men(board)
        # if RED men token reach to the King col become a RED king token with king_conversion_men func    
        elif self.posy == 0 and self.color is RED:
            self.king_conversion_men(board) 
               
        




