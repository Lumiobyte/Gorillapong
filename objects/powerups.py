import pygame
from pygame.locals import *
import math
import random

from utils.colours import Colours
from utils.position import Position
from utils.renderutils import resource_path

class Pineapple():
    def __init__(self, screen):
        """ Setup variables, import and scale sprite """

        self.screen = screen

        self.position = Position(random.randrange(300, 1300), random.randrange(200, 600))
        self.sprite = pygame.image.load(resource_path('image/pineapple.png'))
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 6, self.sprite.get_height() / 6))
        self.col_rect = pygame.Rect(*self.position.tuple(), self.sprite.get_width(), self.sprite.get_height())

        self.speed_increase = 2 # 2

        self.collected = False # has been picked up by player
        self.effected = False # its effect has been applied to the player? 
        self.expired = False
        self.expires_at = -1 # minus one 

    def collect(self, bounces, ball_index, sound):
        """ When powerup gets collected, configure variables and expiry """

        self.collected = True
        self.expires_at = bounces + random.randrange(2, 5) #10

    def render(self):
        if not self.collected:
            #pygame.draw.rect(self.screen, Colours.WHITE, self.col_rect) # collision box

            self.screen.blit(self.sprite, self.position.tuple())

            #pygame.draw.circle(self.screen, Colours.WHITE, self.position.tuple(), 5) # top left

class Pickle():
    def __init__(self, screen):
        """ Setup variables, import and scale sprite """

        self.screen = screen

        self.position = Position(random.randrange(200, 1400), random.randrange(100, 700))
        self.sprite = pygame.image.load(resource_path('image/pickle.png'))
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 10, self.sprite.get_height() / 10))
        self.jar_sprite = pygame.image.load(resource_path('image/jar.png'))
        self.jar_sprite = pygame.transform.scale(self.jar_sprite, (self.sprite.get_width() / 2.5, self.sprite.get_height() / 2.5))
        self.col_rect = pygame.Rect(*self.position.tuple(), self.sprite.get_width(), self.sprite.get_height())

        self.collected = False
        self.effected = False
        self.expired = False
        self.expires_at = -1

        self.collided_ball_index = None

    def collect(self, bounces, ball_index, sound):
        """ When powerup gets collected, configure variables and expiry """

        self.collected = True
        self.expires_at = bounces + random.randrange(2, 8)
        self.collided_ball_index = ball_index

        sound.pickle_jar_pickup() # Sound effect

    def update_pos(self, pos):
        self.position = pos

    def render(self):
        if not self.collected:
            self.screen.blit(self.sprite, self.position.tuple())

        if self.effected and not self.expired:
            self.screen.blit(self.jar_sprite, (self.position.x - 22, self.position.y - 22))

class Water():
    def __init__(self, screen):
        """ Setup variables, import and scale sprite """

        self.screen = screen

        self.position = Position(random.randrange(500, 1100), random.randrange(250, 550))
        self.sprite = pygame.image.load(resource_path('image/water.png'))
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 10, self.sprite.get_height() / 10))
        self.puddle_sprite = pygame.image.load(resource_path('image/puddle.png'))
        self.puddle_sprite = pygame.transform.scale(self.puddle_sprite, (self.puddle_sprite.get_width() / 3, self.puddle_sprite.get_height() / 3))

        self.col_rect = pygame.Rect(*self.position.tuple(), self.sprite.get_width(), self.sprite.get_height())

        self.collected = False
        self.effected = False
        self.expired = False
        self.expires_at = -1

        self.balls_in_puddle = []
        self.speed_change = -4

    def collect(self, bounces, ball_index, sound):
        """ When powerup gets collected, configure variables and expiry. Then spawn the water puddle sprite """

        self.collected = True
        self.expires_at = bounces + 8

        self.col_rect = pygame.Rect(*self.position.tuple(), self.puddle_sprite.get_width(), self.puddle_sprite.get_height())
        self.position.x -= self.col_rect.width / 2
        self.position.y -= self.col_rect.height / 2

        sound.water_pickup() # Sound effect

    def enter_puddle(self, ball_id):
        self.balls_in_puddle.append(ball_id)
        return self.speed_change
        
    def is_in_puddle(self, ball_id):
        if ball_id in self.balls_in_puddle:
            return True
        else:
            return False
        
    def exit_puddle(self, ball_id):
        if ball_id in self.balls_in_puddle:
            self.balls_in_puddle.remove(ball_id)
            return -self.speed_change
        else:
            return 0 # the ball wasn't in the puddle (according to this object's notes) so we return zero, to prevent erroneous speed changes to the ball

    def render(self):
        if not self.expired:
            if self.collected:
                self.screen.blit(self.puddle_sprite, self.position.tuple())
            else:
                self.screen.blit(self.sprite, self.position.tuple())

class Pringle():
    def __init__(self, screen, powerup_id):
        """ Setup variables, import and scale sprite """

        self.screen = screen

        self.powerup_id = powerup_id

        self.position = Position(random.randrange(500, 1100), random.randrange(250, 550))
        self.sprite = pygame.image.load(resource_path('image/pringles.png'))
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 10, self.sprite.get_height() / 10))

        self.col_rect = pygame.Rect(*self.position.tuple(), self.sprite.get_width(), self.sprite.get_height())

        self.collected = False
        self.effected = False
        self.expired = False
        self.expires_at = -1

    def collect(self, bounces, ball_index, sound):
        """ When powerup gets collected, configure variables and expiry. Then spawn the pringle wall rectangle """

        self.collected = True
        self.expires_at = bounces + 10

        self.col_rect = pygame.Rect(self.position.x + 15, self.position.y + 15, 20, 170)
        
    def render(self):
        if not self.expired:
            if self.collected:
                pygame.draw.rect(self.screen, Colours.PRINGLE_WALL, self.col_rect)
            else:
                self.screen.blit(self.sprite, self.position.tuple())

# AFTER GAMEPLAY TESTING, WE DECIDED THAT THIS POWERUP WASN'T MUCH FUN
# IT'S CURRENTLY UNOBTAINABLE WITHIN THE GAME
# THE ONLY WAY TO ACCESS IT IS MANUALLY CHANGE THE CODE
# I LEFT ITS CLASS AND LOGIC HERE ANYWAY
class Computer():
    def __init__(self, screen):
        """ Setup variables, import and scale sprite """

        self.screen = screen

        self.position = Position(random.randrange(400, 1200), random.randrange(200, 600))
        self.sprite = pygame.image.load(resource_path('image/calc.png'))
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 14, self.sprite.get_height() / 14))

        self.col_rect = pygame.Rect(*self.position.tuple(), self.sprite.get_width(), self.sprite.get_height())

        self.collected = False
        self.effected = False
        self.expired = False
        self.expires_at = -1

    def collect(self, bounces, ball_index, sound):
        """ When powerup gets collected, configure variables and expiry """

        self.collected = True
        self.expires_at = bounces + 10

        sound.computer_pickup() # Sound effect

    def render(self):
        """ Draw appropriate powerup sprite """

        if not self.collected:
            self.screen.blit(self.sprite, self.position.tuple())

# THIS POWERUP WAS NEVER COMPLETED
class Paint():
    def __init__(self, screen):
        self.screen = screen
        
        self.position = Position(random.randrange(200, 1400), random.randrange(150, 650))
        self.sprite = pygame.image.load(resource_path('image/paint.png'))
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 10, self.sprite.get_height() / 10))

        self.col_rect = pygame.Rect(*self.position.tuple(), self.sprite.get_width(), self.sprite.get_height())

        self.collected = False
        self.effected = False
        self.expired = False
        self.expires_at = -1

    def collect(self, bounces, ball_index, sound):
        self.collected = True
        self.expires_at = bounces + 10

        sound.paint_pickup()

    def render(self):
        if not self.collected:
            self.screen.blit(self.sprite, self.position.tuple())