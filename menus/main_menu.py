import pygame
from pygame.locals import *
import sys

from menus import button
from utils.colours import Colours

class MainMenu():

    def __init__(self, window):
        self.screen = window
        self.font = pygame.font.SysFont(None, 48)

        self.buttons = [button.Button(self.screen, (255, 255, 255), 10, 10, 50, 25)]

    def process_click(self, pos): # Execute actions for clicks directed to this menu
        for btn in self.buttons:
            if btn.check_collision(pos):
                print("collide")
                break

    def render(self): # Return render for this menu

        text = self.font.render("Gorillapong", True, Colours.WHITE)
        self.screen.blit(text, text.get_rect(center = self.__calc_center(2, 8)))

        for btn in self.buttons:
            btn.render()

    def __calc_center(self, w, h):
        return (self.screen.get_width() / w, self.screen.get_height() / h)
