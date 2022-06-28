# Search.py
from Constants import *
import math
from Token import Token
from Men import Men
from AI_Move import AI_Move
from Game import Game



class Search:
    # Class for search algorithm. 
    # This checkers game using the minimax algorithm for AI with optimization of alpha-beta pruning.
    def __init__(self, ai, player, color):
        self.color = color
        self.player = player
        self.ai = ai

    # The more king tokens have, lead the more advantage to win the game. 
    # Therefore, a high score is given to move that try to reach the king row for becoming a king token.
    def score_token_approach_king_cols(self, board, tile_y, tile_x):
        # Set the score for each token.
        men_score = 15
        # King token should have more score than men token. 
        # Then, AI will try to make more and keep King token to maximise it's score.
        king_score = 45
        high_score_special_position = 1

        if board[tile_y][tile_x] is None:
            return 0
        # check the token reach the king row (The top row and the bottom row) or not.
        if tile_y == len(board) or tile_y == 0:
            high_score_special_position = 1.3
        if isinstance(board[tile_y][tile_x], Men):
            return high_score_special_position * men_score
        else:
            return king_score

    # If the token is located in the leftmost and rightmost col, it is not captured.
    # Therefore, a high score is given to move to go to the vertical cols for keeping number of tokens to win.
    def score_token_approach_vertical_cols(self, board, tile_y, tile_x):
        # Set the score for each token.
        men_score = 15
        # King token should have more score than men token. 
        # Then, AI will try to make more and keep King token to maximise it's score.
        king_score = 45
        high_score_special_position = 1
        
        if board[tile_y][tile_x] is None:
            return 0
        # check the token reach the leftmost or rightmost col or not
        if tile_x == len(board) or tile_x == 0:
            high_score_special_position = 1.3

        if isinstance(board[tile_y][tile_x], Men):
            return high_score_special_position * men_score
        else:
            return king_score

    # Scoring the each token on the board. 
    def scoring_board(self, board, depth):
        # initial state score is 0.
        score = 0
        # Calculating the token's score with considering their position 
        # 1) if there are reach the king's row - can make more king tokens
        # 2) if ther are reach the leftmost or rightmost col - lead more safe for token
        for tile_x in range(len(board)):
            for tile_y in range(len(board)):
                if board[tile_y][tile_x] is not None:
                    if board[tile_y][tile_x].calc_color() == self.color:
                        score = depth + score + (self.score_token_approach_king_cols(board, tile_y, tile_x) 
                                                 + self.score_token_approach_vertical_cols(board, tile_y, tile_x)) / 2
                    else:
                        score = score - depth - (self.score_token_approach_king_cols(board, tile_y, tile_x) 
                                                 + self.score_token_approach_vertical_cols(board, tile_y, tile_x)) / 2
        # Return the calculated score                    
        return score

    # Implement the minimax algorithim that optimize with alpha-beta pruning. 
    def minimaxAB(self, depth, maxPlayer, alpha, beta, board):
        best_move = 0
        move_ai = AI_Move()
    
        if depth == 0 or best_move is None:
            return self.scoring_board(board, depth), best_move
        # Considering the max-Player.
        if maxPlayer:
            best_score = -math.inf
            player, capture_move = self.ai.calc_player(board)
            score = -math.inf

            for leaf_Node in player:
                # Considering capture move.
                if capture_move:
                    move_ai.capture(board, leaf_Node[0], leaf_Node[1], leaf_Node[2], leaf_Node[3], leaf_Node[4])
                    # Considering capture move, especially, 'multi-leg moves'.
                    can_more_capture_move = board[leaf_Node[0]][leaf_Node[1]].can_token_capture(board)
                    if can_more_capture_move:
                        score, player = self.minimaxAB(depth - 1, True, alpha, beta, board) # Point of entry into the recursion
                        if score >= best_score:
                            best_score = score
                            best_move = leaf_Node
                    # only once capture move
                    else: 
                        score, player = self.minimaxAB(depth - 1, False, alpha, beta, board) # Point of entry into the recursion
                        if score >= best_score:
                            best_score = score
                            best_move = leaf_Node
                    move_ai.undo_capture(board, leaf_Node[0], leaf_Node[1], leaf_Node[2], leaf_Node[3], leaf_Node[4])
                # Considering non-capture move.
                else:  
                    move_ai.move(board, leaf_Node[0], leaf_Node[1], leaf_Node[2], leaf_Node[3])

                    score, player = self.minimaxAB(depth - 1, False, alpha, beta, board) # Point of entry into the recursion
                    if score >= best_score:
                        best_score = score
                        best_move = leaf_Node

                    move_ai.undo_move(board, leaf_Node[0], leaf_Node[1], leaf_Node[2], leaf_Node[3])
                # MAX updates alpha if current value is larger than alpha.
                alpha = max(alpha, score)
                if alpha >= beta:
                    break # *β cut-off*
            return score, best_move
        
        # Considering the min-Player.
        else: 
            best_score = math.inf
            score = math.inf
            player, capture_move = self.player.calc_player(board)

            for leaf_Node in player:
                # Considering capture move.
                if capture_move is True:
                    move_ai.capture(board, leaf_Node[0], leaf_Node[1], leaf_Node[2], leaf_Node[3], leaf_Node[4])
                    # Considering capture move, especially, 'multi-leg moves'.
                    can_more_capture_move = board[leaf_Node[0]][leaf_Node[1]].can_token_capture(board)
                    if can_more_capture_move:
                        score, player = self.minimaxAB(depth - 1, False, alpha, beta, board) # Point of entry into the recursion
                        if score < best_score: 
                            best_score = score
                            best_move = leaf_Node
                    # only once capture move
                    else:  
                        score, player = self.minimaxAB(depth - 1, True, alpha, beta, board) # Point of entry into the recursion
                        if score <= best_score:
                            best_score = score
                            best_move = leaf_Node

                    move_ai.undo_capture(board, leaf_Node[0], leaf_Node[1], leaf_Node[2], leaf_Node[3], leaf_Node[4])
                # Considering non-capture move.
                else:  
                    move_ai.move(board, leaf_Node[0], leaf_Node[1], leaf_Node[2], leaf_Node[3])
                    score, player = self.minimaxAB(depth - 1, True, alpha, beta, board) # Point of entry into the recursion
                    if score <= best_score:
                        best_score = score
                        best_move = leaf_Node
                    move_ai.undo_move(board, leaf_Node[0], leaf_Node[1], leaf_Node[2], leaf_Node[3])
                # MIN updates beta if current value is less than beta.
                beta = min(beta, score) 
                if alpha >= beta:
                    break # *α cut-off*

            return score, best_move


