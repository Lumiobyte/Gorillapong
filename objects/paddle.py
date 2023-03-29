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

        self.limit_pos()

    def move_negative(self):
        if self.orientation == 0:
            self.paddle_pos.x -= 10
        else:
            self.paddle_pos.y += 10

        self.limit_pos()


    def limit_pos(self):
        if self.orientation == 0:
            if self.paddle_pos.x > 1500:
                self.paddle_pos.x = 1500
            if self.paddle_pos.x < 100:
                self.paddle_pos.x = 100
        else:
            if self.paddle_pos.y > 800:
                self.paddle_pos.y = 800
            if self.paddle_pos.y < 100:
                self.paddle_pos.y = 100

    def render(self):
        rect = pygame.draw.rect(self.screen, self.colour, pygame.Rect(*self.get_left_top(), self.paddle_rect.x, self.paddle_rect.y))

        # draw bounding points, same as how collisions function calculates them
        """
        pygame.draw.line(self.screen, (255, 255, 255), self.get_left_top(), self.get_left_top())
        rright, rbottom = self.get_left_top()[0] + self.paddle_rect.x, self.get_left_top()[1] + self.paddle_rect.y
        pygame.draw.line(self.screen, (255, 255, 255), (rright, rbottom), (rright, rbottom))
        """
        
    def get_left_top(self):
        return (self.paddle_pos.x - self.paddle_rect.x / 2, self.paddle_pos.y - self.paddle_rect.y / 2,)