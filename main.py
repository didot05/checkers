# main.py
import sys
import pygame
from pygame.locals import *
import math
from Display import Display
from Board import Board
from Men import Men
from Token import Token
from Game import Game
from AI_Move import AI_Move
from Search import Search
from Constants import *
from Button import Button
from pygame import mixer


fps = int(FPS)

def main():
    """
    To run this checkers program, should run this main.py file.
    """
    pygame.init()
        
    fps_clock = pygame.time.Clock()
    
    # Set the "Checkers" title on the game interface
    pygame.display.set_caption('Checkers')

    main_board = Board()
    main_display = Display()
    
    difficultyButtons = [
        Button('Rules', 60, 20, (420, 20), 5),
        Button('Easy', 60, 20, (60, 20), 5),
        Button('Normal', 60, 20, (180, 20), 5),
        Button('Hard', 60, 20, (300, 20), 5),     
    ]
    
    hintButtons = [
        Button('Hint', 60, 20, (0, 445), 5),   
        Button('No-Hint', 60, 20, (120, 445), 5)
    ]
    
    playButtons = [
        Button('Restart', 60, 20, (240, 445), 5),   
        Button('Quit', 60, 20, (360, 445), 5)
    ]
        
    # Initial value of the checkers game
    mouse_selected = False
    mouse_x = 0
    mouse_y = 0
    spotx = 0
    spoty = 0
    board = main_board.create_board()
    # Human player uses a WHITE token. 
    # If you change 'WHITE' value as 'RED', the position is changed. (Player can handle the WHITE tokens that on the upside on game screen.)
    human_player = Game(RED, True) 
    ai_player = Game(WHITE, False) 
    # AI (WHITE player) uses Minimax-alpha beta algorithm for this game.
    searchAlgo = Search(ai_player, human_player, WHITE) 
    move = AI_Move()
    depthVal = 5
    
    showHighlight = True
        
    # Loop for run the main game.
    while True:
        
        current_player = Game.select_player_with_turn(human_player, ai_player)
        main_display.update_board(board)
        
        # Draw buttons for setting the game difficulty level
        difficultyButtons[0].draw()
        difficultyButtons[1].draw()
        difficultyButtons[2].draw()
        difficultyButtons[3].draw()        
        
        if difficultyButtons[1].pressed is True:
            # Easy - search 3 ahead move
            depthVal = 3
        elif difficultyButtons[2].pressed is True:  
            # Normal - search 5 ahead move  
            depthVal = 5
        elif difficultyButtons[3].pressed is True:
            # Hard - search 7 ahead move
            depthVal = 7    

        # Draw buttons for highliting or not the legal tiles for the user as a hint 
        hintButtons[0].draw()
        hintButtons[1].draw()
        
        if hintButtons[0].pressed is True:
            # Give user the hint of legal goal tile
            showHighlight = True
        if hintButtons[1].pressed is True:
            # Do not Give user the hint of legal goal tile
            showHighlight = False   
        
        playButtons[0].draw()
        playButtons[1].draw()
        
        if playButtons[0].pressed is True:
            # Re-start the game
            main()
        if playButtons[1].pressed is True:
            # Quit the game    
            pygame.quit()
            sys.exit()
        
        # For human player turn.
        if human_player.turn is True:
            # Show the who's turn on the caption of screen
            pygame.display.set_caption("Checkers : Your's turn (Depth value : %d)" % depthVal) 
            # checks whether some token is captured or not.
            is_captured = human_player.is_token_captured(board) 
            main_display.check_game_is_end()

            for event in pygame.event.get():  
                if event.type == pygame.MOUSEMOTION:
                    mouse_y, mouse_x = event.pos
                # Check the token which is selected by mouse or not and confirm the mouse position.
                if event.type == pygame.MOUSEBUTTONUP:
                    spoty, spotx = main_display.draw_spot_selected(board, event.pos[0], event.pos[1])
                    mouse_selected = True
            main_display.highlight_while_thinking(board, main_display, mouse_selected, mouse_y, mouse_x)
            token = board[spoty][spotx]

            if isinstance(token, Token) and token.color == human_player.color and mouse_selected is True:
                possible_moves, capture = token.calc_all_possible_moves(board)
                has_captured = False     
    
                # This While loop for controlling the capture moves. 
                # If there are no capture move exist, this loop is just skipped.
                while any(True in sublist for sublist in possible_moves) and capture is True: 
                    pygame.display.set_caption("You have to do capture the enemy's token.") 
                    # show users the possible captures through highlight. 
                    if showHighlight is True:
                        main_display.highlight_possible_moves(possible_moves)  
                    event = pygame.event.wait()
                    main_display.check_game_is_end()
    
                    if event.type == pygame.MOUSEBUTTONUP:
                        # if the mouse is on top of the token, token is marked.
                        tile_to_move_y, tile_to_move_x = main_display.draw_spot_selected(board, event.pos[0], event.pos[1])

                        if possible_moves[tile_to_move_y][tile_to_move_x] is True:
                            main_display.capture_token_animation(board, tile_to_move_y, tile_to_move_x, token.color, spoty, spotx)
                            token.capture_token(board, tile_to_move_y, tile_to_move_x)
                            spoty, spotx = tile_to_move_y, tile_to_move_x

                            if isinstance(token, Men):
                                token.check_for_king_conversion(board)

                            possible_moves, capture = token.calc_all_possible_moves(board)
                            has_captured = True

                        elif has_captured is False:
                            # return the selection of token. 
                            break  

                # This While loop for controlling the non-capture moves. 
                while any(True in sublist for sublist in possible_moves) and not has_captured and not is_captured:
                    if showHighlight is True:
                        main_display.highlight_possible_moves(possible_moves)
                    event = pygame.event.wait()
                    main_display.check_game_is_end()

                    # if the mouse is on top of the token, token is marked.
                    if event.type == pygame.MOUSEBUTTONUP:  
                        tile_to_move_y, tile_to_move_x = main_display.draw_spot_selected(board, event.pos[0], event.pos[1])

                        if possible_moves[tile_to_move_y][tile_to_move_x] is True:
                            main_display.move_token_animation(board, tile_to_move_y, tile_to_move_x,
                                                              token.color, spoty, spotx)
                            token.make_move(board, tile_to_move_y, tile_to_move_x)
                            spoty, spotx = tile_to_move_y, tile_to_move_x

                            if isinstance(token, Men):
                                token.check_for_king_conversion(board)

                            # End the current turn.
                            human_player.changes_turns(human_player, ai_player)
                            mouse_y, mouse_x = event.pos
                            possible_moves = [[]]
                        else:
                            # return the selection of token.
                            break  

                if has_captured:
                    # the turn should be end after capturing move.
                    # change the turn - from human player to AI player.
                    human_player.changes_turns(human_player, ai_player)
                    mouse_y, mouse_x = event.pos        
                    

        # For AI player turn
        else:  
            # Uses minimax Alpha-Beta algorithm for checkers game
            # minimaxAB(self, depth, maxPlayer, alpha, beta, board) - from Search.py 
            # depth : 5
            # maxPlayer : AI 
            # alpha : -infinite
            # beta : +infinite
            # board : board
            
            # Show the who's turn on the caption of screen
            pygame.display.set_caption("Checkers : AI's turn") 
            
            # Can change the difficulty of the checkers program with handle depth value.
            # current depth value is 5 (normal)
            # minimaxAB(3, True, -math.inf, math.inf, board) > easy mode
            # minimaxAB(5, True, -math.inf, math.inf, board) > normal mode
            # minimaxAB(5, True, -math.inf, math.inf, board) > hard mode
            score, best_move = searchAlgo.minimaxAB(depthVal, True, -math.inf, math.inf, board)
            if best_move[4] is not None:
                move.capture(board, best_move[0], best_move[1], best_move[2], best_move[3], best_move[4])
                main_display.draw_ai_highlight(best_move[0], best_move[1])

                token = board[best_move[0]][best_move[1]]
                if isinstance(token, Men):
                    token.check_for_king_conversion(board)

                can_more_capture_move = token.can_token_capture(board)
                # AI should be able to do multi-leg capture. 
                while can_more_capture_move is True: 
                    # If Ai try to do multi-leg move, show that state on the caption.
                    pygame.display.set_caption("Checkers : AI's multi-leg capture move")
                    # Can change the difficulty of the checkers program with handle depth value by click the button.
                    # current depth value is 5 (normal)
                    # minimaxAB(3, True, -math.inf, math.inf, board) > easy mode
                    # minimaxAB(5, True, -math.inf, math.inf, board) > normal mode
                    # minimaxAB(5, True, -math.inf, math.inf, board) > hard mode
                    score, best_move = searchAlgo.minimaxAB(depthVal, True, math.inf, -math.inf, board)
                    move.capture(board, best_move[0], best_move[1], best_move[2], best_move[3], best_move[4])
                    # short pauses screen for showing players multi-leg moves tiles.
                    pygame.display.update()
                    pygame.time.wait(2500)
                    main_display.draw_ai_highlight(best_move[0], best_move[1])
                    # short pauses screen for showing players multi-leg moves tiles.
                    pygame.display.update()
                    pygame.time.wait(2500)
                    token = board[best_move[0]][best_move[1]]
                    if isinstance(token, Men):
                        token.check_for_king_conversion(board)
                    can_more_capture_move = token.can_token_capture(board)
            # non-capture touple value that does not have any fifth item.
            else:  
                move.move(board, best_move[0], best_move[1], best_move[2], best_move[3])
                main_display.draw_ai_highlight(best_move[0], best_move[1])
                token = board[best_move[0]][best_move[1]]

                if isinstance(token, Men):
                    token.check_for_king_conversion(board)

            # Change the turn - From AI player to human player.
            ai_player.changes_turns(human_player, ai_player)
            pygame.display.update()
            pygame.time.wait(300)

        # Redraw screen. 
        # Wait a clock tick.
        current_player.check_who_win(board, main_display)
        mouse_selected = False
        pygame.display.update()
        fps_clock.tick()


if __name__ == '__main__':
    main()

