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

    def render(self):
        pygame.draw.rect(self.screen, Colours.WHITE, self.col_rect)
        self.screen.blit(self.sprite, self.position.tuple())
        pygame.draw.circle(self.screen, Colours.WHITE, self.position.tuple(), 5)