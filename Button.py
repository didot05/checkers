# Button.py
import pygame, sys
from Constants import *
from pygame.locals import *



screen = pygame.display.set_mode((500,500))
class Button:
    # Class for making a GUI button on the screen.
    def __init__(self, message, width, height, pos, elevation):
    	#Core attributes 
		
	    self.pressed = False
	    self.elevation = elevation
	    self.dynamic_elecation = elevation
	    self.original_y_pos = pos[1]

	    # top rectangle 
	    self.top_rect = pygame.Rect(pos, (width, height))
	    self.top_color = DARKBLUE

		# bottom rectangle 
	    self.bottom_rect = pygame.Rect(pos, (width, height))
	    self.bottom_color = DEEPBLUE
		# message
	    self.message_surf = pygame.font.Font(None, 20).render(message, True, WHITE)
	    self.message_rect = self.message_surf.get_rect(center = self.top_rect.center)

    def draw(self):
		# elevation logic 
	    self.top_rect.y = self.original_y_pos - self.dynamic_elecation
	    self.message_rect.center = self.top_rect.center 

	    self.bottom_rect.midtop = self.top_rect.midtop
	    self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
     
	    pygame.draw.rect(screen, DEEPBLUE, self.bottom_rect, 2)    
	    pygame.draw.rect(screen, DARKBLUE, self.top_rect, 2)
	    screen.blit(self.message_surf, self.message_rect)
	    self.show_rule() 
      
    def show_rule(self): 
        self.font = pygame.font.Font(None, 20)
        mouse_pos = pygame.mouse.get_pos()
        state_message_1 = self.font.render("Rule 1. You can handle your men token with a diagonal move forward.", True, WHITE)
        state_message_2 = self.font.render("Rule 2. You can handle your king token with a backward move also.", True, WHITE)
        state_message_3 = self.font.render("Rule 3. If you can capture an enemy token, then you have to do so.", True, WHITE)
        state_message_4 = self.font.render("Rule 4. You can upgraded men token as king token to reach king cols.", True, WHITE)
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = BRIGHTRED
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                
                if self.pressed == True:
                    screen.blit(state_message_1, (20, 490))
                    screen.blit(state_message_2, (20, 510))
                    screen.blit(state_message_3, (20, 530))
                    screen.blit(state_message_4, (20, 550))
                    pygame.display.update()
                    event = pygame.event.wait()
                    self.pressed = False      
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = DARKBLUE
            
   
        