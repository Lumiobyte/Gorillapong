import pygame
from pygame.locals import *

from utils.position import Position

class Paddle():
    def __init__(self, screen, orientation, starting_pos, colour):

        self.screen = screen
        self.orientation = orientation
        self.colour = colour

        if self.orientation == 0:
            self.paddle_rect = Position(190, 20)
            self.paddle_pos = Position(*starting_pos)
        else:
            self.paddle_rect = Position(20, 190)
            self.paddle_pos = Position(*starting_pos)

    def move_positive(self):
        if self.orientation == 0:
            self.paddle_pos.x += 10
        else:
            self.paddle_pos.y -= 10

    def move_negative(self):
        if self.orientation == 0:
            self.paddle_pos.x -= 10
        else:
            self.paddle_pos.y += 10

    def render(self):
        rect = pygame.draw.rect(self.screen, self.colour, pygame.Rect(*self.get_left_top(), self.paddle_rect.x, self.paddle_rect.y))

    def get_left_top(self):
        return (self.paddle_pos.x - self.paddle_rect.x / 2, self.paddle_pos.y - self.paddle_rect.y / 2,)