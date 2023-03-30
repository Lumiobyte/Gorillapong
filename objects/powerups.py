import pygame
from pygame.locals import *
import math
import random

from utils.colours import Colours
from utils.position import Position

class Pineapple():
    def __init__(self, screen):
        self.screen = screen

        self.location = Position(random.randrange(300, 1300), random.randrange(200, 600))

        self.sprite = pygame.image.load('image/pineapple.png')
        self.sprite = #resize

    def render(self):
        self.screen.blit(self.sprite, self.location.tuple())
        pygame.draw.circle(self.screen, Colours.WHITE, self.location.tuple(), 5)
        