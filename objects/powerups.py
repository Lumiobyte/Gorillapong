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
        self.expires_at = -1 # minus one 

    def collect(self, bounces):
        self.collected = True
        self.expires_at = bounces + random.randrange(2, 5) #10

    def render(self):
        if self.collected == False:
            #pygame.draw.rect(self.screen, Colours.WHITE, self.col_rect) # collision box

            self.screen.blit(self.sprite, self.position.tuple())

            #pygame.draw.circle(self.screen, Colours.WHITE, self.position.tuple(), 5) # top left