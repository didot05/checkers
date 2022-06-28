# Display.py
import pygame
from pygame.locals import *
import sys
from Token import Token
from Constants import *
import Men
import King
from Game import *



class Display:
    # Class for user interface for display game status for user.
    # Initialize of each value from Constants.py.
    def __init__(self):
        self.size_board = int(SIZE_BOARD)
        self.size_tile = int(SIZE_TILE)
        self.window_width = int(WIDTH)
        self.window_height = int(HEIGHT)
        self.surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.margin_x = int((self.window_height - (self.size_board * self.size_tile)) / 2)
        self.margin_y = int((self.window_width - (self.size_board * self.size_tile)) / 2) 
        self.font_size = int(FONT_SIZE) 
        self.font = pygame.font.Font(None, self.font_size)

    # Calculate the top-left corner positions (x,y) of given tile. 
    def calc_top_left_corner(self, tile_y, tile_x):
        # tile_y: value of Board vertical position, same as row number in board 2D-list.
        # tile_x: value of Board horizontal position, same as column number in board 2D-list.
        top_left_x_pos = self.margin_y + (self.size_tile * tile_x)
        top_left_y_pos = self.size_tile * tile_y 
        return (top_left_y_pos, top_left_x_pos)

    # Draw the square tiles for checkers game with pygame.draw.rect func.
    def draw_tile(self, tile_y, tile_x):
        top_left_y_pos, top_left_x_pos = self.calc_top_left_corner(tile_y, tile_x)
        pygame.draw.rect(self.surface, DARKRED, (top_left_x_pos, top_left_y_pos, self.size_tile, self.size_tile))

    # Draw empty board for checkers games.
    def draw_empty_board(self):
        # Draw black colored base-board.
        self.surface.fill(BLACK)
        self.board_dim = self.size_board * self.size_tile
        # (0, 0) position is the start position of board and it is top-left on the screen.
        top_left_y_pos, top_left_x_pos = self.calc_top_left_corner(0, 0)
        # Draw black tile on white base-board which composed the checkers board.
        pygame.draw.rect(self.surface, BLACK, (top_left_x_pos, top_left_y_pos, self.board_dim, self.board_dim))

        count = 0
        for tile_y in range(self.size_board):
            for tile_x in range(self.size_board):
                if count % 2 == 0:
                    self.draw_tile(tile_y, tile_x)
                count += 1
            count += 1   

    # Draw men token for checkers game.
    # Each men token object in which is drawn with .blit func on given tile.
    def draw_men(self, tile_y, tile_x, color):
        top_left_y_pos, top_left_x_pos = self.calc_top_left_corner(tile_y, tile_x)
        if (color is WHITE):
            self.surface.blit(WHITEMEN, (top_left_x_pos - 15, top_left_y_pos - 15))
        else:
            self.surface.blit(REDMEN, (top_left_x_pos - 15, top_left_y_pos - 15))

    # Mark King token with crown inside the normal token for distinguishing from the men token.
    def draw_king_mark(self, tile_y, tile_x):
        top_left_y_pos, top_left_x_pos = self.calc_top_left_corner(tile_y, tile_x)
        # Draw the crown inside the King token with .blit func on the token.  
        self.surface.blit(CROWN, (top_left_x_pos - 15, top_left_y_pos - 15))       

    # Set the each token to the tiles on the board.
    def tokens_on_board(self, board):
        for tile_y in range(len(board)):
            for tile_x in range(len(board[0])):
                # Set the men tokens on the board.
                if isinstance(board[tile_y][tile_x], Men.Men):
                    self.draw_men(tile_y, tile_x, board[tile_y][tile_x].calc_color())
                # Set the king tokens on the board.    
                elif isinstance(board[tile_y][tile_x], King.King):
                    self.draw_men(tile_y, tile_x, board[tile_y][tile_x].calc_color())
                    self.draw_king_mark(tile_y, tile_x)

    # In the case of a token is clicked(selected) through a mouse, 
    # a spot is drawn on that for distinguishing it from other tokens.
    def draw_spot_selected(self, board, pos_x_mouse, pos_y_mouse):
        for tile_y in range(len(board)):
            for tile_x in range(len(board)):
                top_left_y_pos, top_left_x_pos = self.calc_top_left_corner(tile_y, tile_x)
                # Show the spot on it with pygame.Rect() func.
                tile_Rect = pygame.Rect(top_left_x_pos, top_left_y_pos, self.size_tile, self.size_tile)
                # Change the pixel(x, y) positions to the board(x, y) positions (e.g. board: board data structure)
                if tile_Rect.collidepoint(pos_x_mouse, pos_y_mouse):
                    return tile_y, tile_x
        return None, None

    # Draw the highlight on the tile which selected by the player with yellow square outlines.  
    def draw_player_highlight(self, tile_y, tile_x):
        top_left_y_pos, top_left_x_pos = self.calc_top_left_corner(tile_y, tile_x)
        pygame.draw.rect(self.surface, YELLOW, (top_left_x_pos, top_left_y_pos, self.size_tile - 3, self.size_tile - 3), 3)

    # Draw the highlight on the tile which selected by the ai with yellow square outlines. 
    def draw_ai_highlight(self, tile_y, tile_x):
        top_left_y_pos, top_left_x_pos = self.calc_top_left_corner(tile_y, tile_x)
        pygame.draw.rect(self.surface, YELLOW, (top_left_x_pos, top_left_y_pos, self.size_tile - 3, self.size_tile - 3), 3)
    
    # Draw the highlight on the tile where the token can move on with yellow square border.     
    def highlight_possible_moves(self, possible_moves):
        for tile_y in range(len(possible_moves)):
            for tile_x in range(len(possible_moves)):
                # Check the it is valid move or not.
                if possible_moves[tile_y][tile_x] is True:
                    self.draw_player_highlight(tile_y, tile_x)
                else:
                    state_message = self.font.render("You should select the valid tile to move on.", True, WHITE)
                    self.surface.blit(state_message, (20, 500))
                        
        # Update the current state to the screen.            
        pygame.display.update()

    # Update the board state.
    def update_board(self, board):
        # Call empty board.
        self.draw_empty_board()
        # Call all tokens on the board currently.
        self.tokens_on_board(board)

    def move_token_animation(self, board, tile_y, tile_x, color, posy, posx):
        """
        : board: board data structure
        : tile_y: Board vertical position at move's goal
        : tile_x: Board horizontal position at move's goal
        : color: color of given men
        : posy: The vertical(y) pos value of token's current position on the board.
        : posx: The horizontal(x) pos value of token's current position on the board.
        """
        self.draw_men(tile_y, tile_x, color)
        self.draw_tile(posy, posx)
        if isinstance(board[posy][posx], King.King):
            self.draw_king_mark(tile_y, tile_x)

    def capture_token_animation(self, board, tile_y, tile_x, color, posy, posx):
        captured_token_x = int((tile_x + posx) * 0.5)
        if tile_y < posy:
            captured_token_y = posy - 1
        else:
            captured_token_y = posy + 1
        self.draw_men(tile_y, tile_x, color)
        # If the token is King token, the token should have the king mark. (have crown inside the token)
        if isinstance(board[posy][posx], King.King):
            self.draw_king_mark(tile_y, tile_x)
        self.draw_tile(posy, posx)
        self.draw_tile(captured_token_y, captured_token_x)
        pygame.display.update()

    # Short interface for checkers game end with winner message
    def show_who_win(self, color): 
        myfont = pygame.font.SysFont(None, 30)
        end_message = myfont.render("Checkers Game End!", True, BLACK)
        pygame.display.set_caption("Game End")
        if(color is RED): 
            game_outcome_message = myfont.render("Congratulations! You win!", True, BLACK)
        else:
            game_outcome_message = myfont.render("   Try Again! AI win!", True, BLACK)    
        while True:
            # Fill the interface with the winner's color (Player - RED / AI - WHITE)
            self.surface.fill(color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.surface.blit(end_message, (140, 130))
            self.surface.blit(game_outcome_message, (140, 230))
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()   
    
    # Shut down the game if escape keys or quit event input to the game.
    def check_game_is_end(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shut_down()
            pygame.event.post(event)
        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_ESCAPE:
                self.shut_down()
            pygame.event.post(event)

    # Shut down the program.
    def shut_down(self):
        pygame.quit()
        sys.exit()

    # If player keep hovering, just keep the highlight square to tiles that not selected yet on the board.
    def highlight_while_thinking(self, board, display, mouse_selected, mouse_y, mouse_x):
        # Check the tile is selected or not.
        if mouse_selected == False:
            tile_y, tile_x = display.draw_spot_selected(board, mouse_y, mouse_x)
            state_message = self.font.render("Keep thinking ...", True, WHITE)
            self.surface.blit(state_message, (20, 500))
            if tile_y != None and tile_x != None:
                display.draw_player_highlight(tile_y, tile_x)     
                 