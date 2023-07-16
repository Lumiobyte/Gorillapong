import pygame
from pygame.locals import *

from utils.colours import Colours


class Button():
    """ This class contains button related variables e.g. display text, colours, size/shape, etc. 
        It also contains logic to process collisions and render itself. """
    def __init__(self, window, colour, hover_colour, center, w, h, title, action, support_hover = True, font = None):
        self.screen = window

        self.colour = colour
        self.hover_colour = hover_colour
        self.hovered = False
        self.title = title
        self.center = center
        self.w = w
        self.h = h
        self.button_rect = pygame.Rect(center[0] - (w / 2), center[1] - (h / 2), w, h) # Center coordinates are provided but rect defined from top left; conversion is needed
        self.button_action = action

        self.support_hover = support_hover # Changing colour on hover can be disabled, e.g. if the button was greyed out/unavailable

        if font: # If font was provided when the object was created, use that instead
            self.font = font
        else:
            self.font = pygame.font.SysFont(None, 48)

    def hover(self):
        """ This function is called by the main menu when mouse pointer collides with button rect but the user does not click - a 'hover'. 
            Here we just set the variable to true if hovering is enabled, and then the button colour is rendered accordingly in render() """
        if self.support_hover:
            self.hovered = True

    def check_collision(self, pos):
        """ Check collision between the mouse pointer coordinates and the button rectangle """
        return self.button_rect.collidepoint(pos), self.button_action
    
    def move(self, pos):
        """ Redefine the button rect when new center coordinates are provided """
        self.center = pos
        self.button_rect = pygame.Rect(self.center[0] - (self.w / 2), self.center[1] - (self.h / 2), self.w, self.h)
    
    def render(self):
        """ Renders button and its label text """
        if self.hovered:
            pygame.draw.rect(self.screen, self.hover_colour, self.button_rect)
        else:
            pygame.draw.rect(self.screen, self.colour, self.button_rect)
        text = self.font.render(self.title, True, Colours.BLACK)
        self.screen.blit(text, text.get_rect(center = (self.center[0], self.center[1])))

        self.hovered = False # Set hover to false, as the main menu will update it back to true if the mouse is still over the button next frame