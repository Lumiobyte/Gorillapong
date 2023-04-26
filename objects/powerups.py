import pygame
from pygame.locals import *
import math
import random

from utils.colours import Colours
from utils.position import Position

class Pineapple():
    def __init__(self, screen):
        self.screen = screen

        self.position = Position(random.randrange(300, 1300), random.randrange(200, 600))
        self.sprite = pygame.image.load('image/pineapple.png')
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 6, self.sprite.get_height() / 6))
        self.col_rect = pygame.Rect(*self.position.tuple(), self.sprite.get_width(), self.sprite.get_height())

        self.speed_increase = 2 # 2

        self.collected = False # has been picked up by player
        self.effected = False # its effect has been applied to the player? 
        self.expired = False
        self.expires_at = -1 # minus one 

    def collect(self, bounces, ball_index):
        self.collected = True
        self.expires_at = bounces + random.randrange(2, 5) #10

    def render(self):
        if not self.collected:
            #pygame.draw.rect(self.screen, Colours.WHITE, self.col_rect) # collision box

            self.screen.blit(self.sprite, self.position.tuple())

            #pygame.draw.circle(self.screen, Colours.WHITE, self.position.tuple(), 5) # top left

class Pickle():
    def __init__(self, screen):
        self.screen = screen

        self.position = Position(random.randrange(200, 1400), random.randrange(100, 700))
        self.sprite = pygame.image.load('image/pickle.png')
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() / 10, self.sprite.get_height() / 10))
        self.jar_sprite = pygame.image.load('image/jar.png')
        self.jar_sprite = pygame.transform.scale(self.jar_sprite, (self.sprite.get_width() / 4, self.sprite.get_height() / 4))
        self.col_rect = pygame.Rect(*self.position.tuple(), self.sprite.get_width(), self.sprite.get_height())

        self.collected = False
        self.effected = False
        self.expired = False
        self.expires_at = -1

        self.collided_ball_index = None

    def collect(self, bounces, ball_index):
        self.collected = True
        self.expires_at = bounces + 3
        self.collided_ball_index = ball_index

    def update_pos(self, pos):
        self.position = pos

    def render(self):
        if not self.collected:
            self.screen.blit(self.sprite, self.position.tuple())

        if self.effected:
            self.screen.blit(self.jar_sprite, self.position.tuple())
