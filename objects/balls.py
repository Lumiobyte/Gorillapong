import pygame
from pygame.locals import *
import random
import math

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

    def reverse_velocity_x(self, paddle_pos = None):
        self.velocity.x = -self.velocity.x

        if paddle_pos:
            self.velocity.y = self.velocity.y * (abs(paddle_pos.y - self.position.y) / 190) # 190 = paddle height...
            print(str(paddle_pos.y) + " " + str(self.position.y))

        """
        if self.velocity.y > 1.2 or self.velocity.y < -1.2:
            self.velocity.x -= self.bounce_modifier
        elif self.velocity.y < 0.8 or self.velocity.y > -0.8:
            self.velocity.x += self.bounce_modifier
        else:
            self.velocity.x += random.choice([self.bounce_modifier, -self.bounce_modifier])
        """

    def reverse_velocity_y(self, paddle_pos = None):
        self.velocity.y = -self.velocity.y

        if paddle_pos:
            self.velocity.x = self.velocity.x * (abs(paddle_pos.x - self.position.x) / 190) 
            print(str(paddle_pos.x) + " " + str(self.position.x))

        """
        if self.velocity.x > 1.2 or self.velocity.x < -1.2:
            self.velocity.y -= self.bounce_modifier
        elif self.velocity.x < 0.8 or self.velocity.x > -0.8:
            self.velocity.y -= self.bounce_modifier
        else:
            self.velocity.y += random.choice([self.bounce_modifier, -self.bounce_modifier])
        """

    def tick(self):
        self.position.x += int(self.velocity.x * self.speed)
        self.position.y += int(self.velocity.y * self.speed)

    def render(self):
        pygame.draw.circle(self.screen, self.colour, self.position.tuple(), self.radius)
