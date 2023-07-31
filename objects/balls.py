import pygame
from pygame.locals import *
import random
import math

from utils.position import Position
from utils.renderutils import resource_path

class Ball:
    def __init__(self, screen, radius, speed, bounce_modifier, colour, ball_id):
        """ Set up variables """

        self.screen = screen

        self.position = Position(800, 450)
        self.radius = radius
        self.velocity = Position(-1, 1)
        self.default_speed = speed / 2
        self.speed = speed / 2
        self.bounced = False
        self.bounce_modifier = bounce_modifier
        self.colour = colour

        self.sprite = pygame.image.load(resource_path('image/gorilla.png'))

        self.paddle_last_hit = None
        self.in_puddle = False
        self.pringle_last_hit = None

        self.ball_id = ball_id
        self.debug = False
        self.debug_dot = (100, 100)
    
    def change_velocity(self, x, y):
        """ Increment velocity by requested amount """

        self.velocity.x += x
        self.velocity.y += y 

    def reverse_velocity_x(self, paddle_pos = None, paddle_hit = None):
        """ Flip the horizontal direction of the ball (e.g after a collision against a vertical paddle) """
        if paddle_hit is None: # Direct flip (e.g. setting an initial travel direction of a newly spawned ball)
            self.velocity.x = -self.velocity.x

        if paddle_pos: # Flip based on paddle hit
            if self.paddle_last_hit != paddle_hit: # Don't allow consecutive flips on the same paddle. 
                self.velocity.x = -self.velocity.x # Flip x directly
                center_diff = (paddle_pos.y - self.position.y) # The distance the ball hit away from the center of the paddle
                self.velocity.y = (-center_diff / 100) * 1 # Calculate y based on where the ball hit on the paddle to create a non-right angle bounce

                if self.bounced == False: # This sets the ball to full speed if this is its first bounce. It has a halved speed intially so that it's easier to hit serves
                    self.bounced = True
                    self.speed = self.speed * 2

                if self.debug: # Dot at the calculated impact position for debug purposes
                    impact_y = abs(paddle_pos.y - center_diff)
                    self.debug_dot = (paddle_pos.x, impact_y)

        self.paddle_last_hit = paddle_hit

    def reverse_velocity_y(self, paddle_pos = None, paddle_hit = None):
        """ The same procedure as reverse_velocity_x but for the vertical direction (an impact against a horizontal paddle) """
        if paddle_hit is None:
            self.velocity.y = -self.velocity.y

        if paddle_pos:
            if self.paddle_last_hit != paddle_hit:
                self.velocity.y = -self.velocity.y
                center_diff = paddle_pos.x - self.position.x
                self.velocity.x = (-center_diff / 100) * 1

                if self.bounced == False:
                    self.bounced = True
                    self.speed = self.speed * 2

                if self.debug:
                    impact_x = abs(paddle_pos.x - center_diff)
                    self.debug_dot = (impact_x, paddle_pos.y)

        self.paddle_last_hit = paddle_hit

    def tick(self):
        """ This is called every frame. Just moves the ball, and returns the distance moved for statistics purposes """
        if self.speed <= 0: # Lazy fix for getting stuck in bugged water puddles
            self.speed = 5.0
            
        x_delta = (self.velocity.x * self.speed)
        y_delta = (self.velocity.y * self.speed)

        self.position.x += x_delta
        self.position.y += y_delta

        return x_delta + y_delta
    
    def future_position(self, iterations = None): # Potentially add ability to iterate until a certain x or y is reached.
        """ Calculate the ball's position either: 
            - x frames into the future
            - until it reaches the edge of the screen
        """

        x = self.position.x
        y = self.position.y

        if iterations: # Calculate where the ball will be x frames into the future
            for i in range(0, iterations + 1):
                x += (self.velocity.x * self.speed)
                y += (self.velocity.y * self.speed)

            return (x, y)
        
        else: # Calculate where the ball will be when it reaches the line along which paddles travel
            iterate_x = True
            iterate_y = True
            while iterate_x and iterate_y: # (x > 40 and x < 1560) and (y > 40 and y < 860))
                x += (self.velocity.x * self.speed)
                y += (self.velocity.y * self.speed)

                # Method to find out which intercept was reached first 
                if (x < 40 or x > 1560):
                    iterate_x = False
                elif (y < 40 or y > 860):
                    iterate_y = False

            if abs(x - y) > 100: # If the point it reaches one intercept has it more than 100 pixels from the other intercept, the irrelevant paddle will not move
                if iterate_x is False:
                    x = -1 # If x limit is the first reached, the y (vertical) paddle will need to take the bounce, vice versa
                elif iterate_y is False:
                    y = -1

            return Position(x, y)


    def render(self):
        """ Render ball """

        #pygame.draw.circle(self.screen, self.colour, self.position.tuple(), self.radius)
        self.screen.blit(self.sprite, (self.position.tuple()[0] - 15, self.position.tuple()[1] - 15))

        if self.debug: # Indicator dots to help with debugging
            pygame.draw.circle(self.screen, (255, 255, 255), (self.debug_dot[0], self.debug_dot[1]), radius=5)
            pygame.draw.circle(self.screen, (255, 255, 255), self.position.tuple(), radius = 5)