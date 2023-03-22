import pygame
from pygame.locals import *

from utils.position import Position

class Ball:
    def __init__(self, screen, radius, speed, colour):
        self.screen = screen

        self.position = Position(500, 500)
        self.radius = radius
        self.velocity = Position(-1, 1)
        self.speed = speed
        self.colour = colour
    
    def change_velocity(self, x, y):
        self.velocity.x += x
        self.velocity.y += y 

    def reverse_velocity_x(self):
        self.velocity.x = -self.velocity.x

    def reverse_velocity_y(self):
        self.velocity.y = -self.velocity.y

    def tick(self):
        self.position.x += self.velocity.x * self.speed
        self.position.y += self.velocity.y * self.speed

    def render(self):
        pygame.draw.circle(self.screen, self.colour, self.position.tuple(), self.radius)
