import pygame
from pygame.locals import *

class Button():
    def __init__(self, window, colour, t, l, w, h):
        self.screen = window

        self.colour = colour
        self.button_rect = pygame.Rect(t, l, w, h)

    def check_collision(self, pos):
        return self.button_rect.collidepoint(pos)
    
    def render(self):
        pygame.draw.rect(self.screen, self.colour, self.button_rect)