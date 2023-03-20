import pygame
from pygame.locals import *

class Paddle():
    def __init__(self, screen, orientation, starting_pos):

        self.screen = screen
        self.orientation = orientation

        if self.orientation == 0:
            self.paddle_rect = (190, 20)
            self.paddle_pos = starting_pos
        else:
            self.paddle_rect = (20, 190)
            self.paddle_pos = starting_pos

    def move_positive(self):
        if self.orientation == 0:
            self.paddle_pos[0] += 10
        else:
            self.paddle_pos[1] -= 10

    def move_negative(self):
        if self.orientation == 0:
            self.paddle_pos[0] -= 10
        else:
            self.paddle_pos[1] += 10

    def render(self, colour):
        rect = pygame.draw.rect(self.screen, colour, pygame.Rect(self.paddle_pos[0] - self.paddle_rect[0] / 2, self.paddle_pos[1] - self.paddle_rect[1] / 2, *self.paddle_rect))