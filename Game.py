# Game.py
from Constants import *
import Men
from Token import Token
from pygame import mixer


class Game:
    # Class for handling the general rules for checkers game.
    def __init__(self, color, turn):
        self.turn = turn
        self.color = color        

    # Confirm the each player's turn.
    def calc_player_turn(self):
        return self.turn

    # Check the who (player or ai) win the checkers game.
    # After confirming, this checkers game show the screen with a message containing who is the winner.
    def check_who_win(self, board, main_interface):
        current_board = [y for x in board for y in x]
        tokens = [token for token in current_board if isinstance(token, Token) and token.calc_color() != self.color]
        # There are two goal state exist for checkers game 
        # 1) Human player has zero checkers token left.
        # 2) AI player has zero checkers token left. 
        if not tokens:
            main_interface.show_who_win(self.color)

    # Look at the board and check there are any player's tokens is captured or not. 
    def is_token_captured(self, board):
        # list for captures tokens.
        all_captures = []
        for tile_x in range(len(board)):
            for tile_y in range(len(board)):
                if isinstance(board[tile_y][tile_x], Token) and board[tile_y][tile_x].calc_color() == self.color:
                    possible_captures = board[tile_y][tile_x].calc_possible_captures(board)
                    current_possible_captures = [y for x in possible_captures for y in x]
                    all_captures.append(current_possible_captures)
        if any(True in sublist for sublist in all_captures):
            # case - Captured tokens exist
            return True
        else:
            # case - No captured tokens
            return False

    @classmethod
    def select_player_with_turn(cls, player1, player2):
        players = (player1, player2)
        for player in players:
            if player.turn is True:
                return player

    # Convert the turns of game.
    def changes_turns(self, player1, player2):
        players = [player1, player2]
        # Sound effect for placing the token
        mixer.music.load('assets/tokenPlaced.wav')
        for player in players:
            player.turn = not player.turn
            mixer.music.play()

    # Calculate the valid moves of tokens.
    def calc_moves_of_token(self, board, posy, posx):
        token_captures = []
        token_moves = []
        possible_moves, capture = board[posy][posx].calc_all_possible_moves(board)
        for x_move in range(len(possible_moves)):
            for y_move in range(len(possible_moves)):
                if possible_moves[y_move][x_move] is True and capture is True:
                        captured_token_x = int((posx + x_move) / 2)
                        if y_move < posy:
                            captured_token_y = posy - 1
                        else:
                            captured_token_y = posy + 1

                        capture_positions = (y_move, x_move, posy, posx, board[captured_token_y][captured_token_x])
                        token_captures.append(capture_positions)

                elif possible_moves[y_move][x_move] is True and capture is False:
                    move_positions = (y_move, x_move, posy, posx, None)
                    token_moves.append(move_positions)
        # If there are no valid capturing move exist, they just should move the token in valid way. 
        if not token_captures:
            capture = False
            return token_moves, capture
        # If there are valid capturing move exist, they have to do so. 
        # ; Forced Capture
        else:
            capture = True
            return token_captures, capture

    # Calculate the all valid players moves; capturing moves & not capturing moves
    def calc_player(self, board):
        player_captures = []
        player_moves = []
        for tile_x in range(len(board)):
            for tile_y in range(len(board)):
                if isinstance(board[tile_y][tile_x], Token) and board[tile_y][tile_x].calc_color() == self.color:
                    move_parameters, capture_move = self.calc_moves_of_token(board, tile_y, tile_x)
                    if capture_move is True:
                        player_captures.extend(move_parameters)
                    else:
                        player_moves.extend(move_parameters)

        if not player_captures:
            capture_move = False
            return player_moves, capture_move
        else:
            capture_move = True
            return player_captures, capture_move



