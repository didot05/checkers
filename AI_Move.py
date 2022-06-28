# AI_Move.py
from Men import Men
from King import King



class AI_Move:
    # Class for calculating the valid move of AI player.
    def __init__(self):
        pass
    
    # Confirm that if there are possible capture moves exist or not on a given tile.
    # If there are possible capture moves exist, calculate the position of the captured token and capture token.
    def capture(self, board, goal_y, goal_x, posy, posx, captured_token):
         # remove the token on the ([captured_token_position_y][captured_token_position_x]) tile which is captured. 
        board[captured_token.posy][captured_token.posx] = None
        board[posy][posx], board[goal_y][goal_x] = board[goal_y][goal_x], board[posy][posx]
        # Update the position of capture token.                                                                     
        board[goal_y][goal_x].posy = goal_y
        board[goal_y][goal_x].posx = goal_x

    # Calculate the position of the token after move.
    def move(self, board, goal_y, goal_x, posy, posx):
        board[posy][posx], board[goal_y][goal_x] = board[goal_y][goal_x], board[posy][posx]
        # Update the position of current token after valid move. 
        board[goal_y][goal_x].posy = goal_y
        board[goal_y][goal_x].posx = goal_x

    # Memorize the position of token before simulating move with minimax-alphabeta algorithm.
    def undo_move(self, board, goal_y, goal_x, posy, posx):
        board[posy][posx], board[goal_y][goal_x] = board[goal_y][goal_x], board[posy][posx]
        board[posy][posx].posy = posy
        board[posy][posx].posx = posx

    # Memorize the position of token before simulating capture-move with minimax-alphabeta algorithm.
    def undo_capture(self, board, goal_y, goal_x, posy, posx, captured_token):
          board[captured_token.posy][captured_token.posx] = captured_token
          board[posy][posx], board[goal_y][goal_x] = board[goal_y][goal_x], board[posy][posx]
          board[posy][posx].posy = posy
          board[posy][posx].posx = posx
