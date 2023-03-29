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

        self.debug = True
        self.debug_dot = (100, 100)
    
    def change_velocity(self, x, y):
        self.velocity.x += x
        self.velocity.y += y 

    def reverse_velocity_x(self, paddle_pos = None):
        self.velocity.x = -self.velocity.x

        if paddle_pos:
            center_diff = (paddle_pos.y - self.position.y)
            self.velocity.y = (-center_diff / 100) * 1

            if self.debug:
                impact_y = abs(paddle_pos.y - center_diff)
                self.debug_dot = (paddle_pos.x, impact_y)

    def reverse_velocity_y(self, paddle_pos = None):
        self.velocity.y = -self.velocity.y

        if paddle_pos:
            center_diff = paddle_pos.x - self.position.x
            self.velocity.x = (-center_diff / 100) * 1

            if self.debug:
                impact_x = abs(paddle_pos.x - center_diff)
                self.debug_dot = (impact_x, paddle_pos.y)

    def tick(self):
        self.position.x += (self.velocity.x * self.speed)
        self.position.y += (self.velocity.y * self.speed)

    def render(self):
        pygame.draw.circle(self.screen, self.colour, self.position.tuple(), self.radius)

        if self.debug:
            pygame.draw.circle(self.screen, (255, 255, 255), (self.debug_dot[0], self.debug_dot[1]), radius=5)
