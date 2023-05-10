import pygame
from pygame.locals import *

from utils.colours import Colours

# Add button highlights on hover
class Button():
    def __init__(self, window, colour, hover_colour, center, w, h, title, action):
        self.screen = window

        self.colour = colour
        self.hover_colour = hover_colour
        self.hovered = False
        self.title = title
        self.center = center
        self.button_rect = pygame.Rect(center[0] - (w / 2), center[1] - (h / 2), w, h)
        self.button_action = action

        self.font = pygame.font.SysFont(None, 48)

    def hover(self):
        self.hovered = True

    def check_collision(self, pos):
        return self.button_rect.collidepoint(pos), self.button_action
    
    def render(self):
        if self.hovered:
            pygame.draw.rect(self.screen, self.hover_colour, self.button_rect)
        else:
            pygame.draw.rect(self.screen, self.colour, self.button_rect)
        text = self.font.render(self.title, True, Colours.BLACK)
        self.screen.blit(text, text.get_rect(center = (self.center[0], self.center[1])))

        self.hovered = False