import pygame
from pygame.locals import *
import random

from utils.position import Position

class Ball:
    def __init__(self, screen, radius, speed, bounce_modifier, colour):
        self.screen = screen

        self.position = Position(800, 450)
        self.radius = radius
        self.velocity = Position(-1, 1)
        self.speed = speed
        self.bounce_modifier = bounce_modifier
        self.colour = colour
    
    def change_velocity(self, x, y):
        self.velocity.x += x
        self.velocity.y += y 

    def reverse_velocity_x(self):
        self.velocity.x = -self.velocity.x

        if self.velocity.y > 1.2 or self.velocity.y < -1.2:
            self.velocity.x -= self.bounce_modifier
        elif self.velocity.y < 0.8 or self.velocity.y > -0.8:
            self.velocity.x += self.bounce_modifier
        else:
            self.velocity.x += random.choice([self.bounce_modifier, -self.bounce_modifier])

    def reverse_velocity_y(self):
        self.velocity.y = -self.velocity.y

        if self.velocity.x > 1.2 or self.velocity.x < -1.2:
            self.velocity.y -= self.bounce_modifier
        elif self.velocity.x < 0.8 or self.velocity.x > -0.8:
            self.velocity.y -= self.bounce_modifier
        else:
            self.velocity.y += random.choice([self.bounce_modifier, -self.bounce_modifier])

    def tick(self):
        self.position.x += self.velocity.x * self.speed
        self.position.y += self.velocity.y * self.speed

    def render(self):
        pygame.draw.circle(self.screen, self.colour, self.position.tuple(), self.radius)
