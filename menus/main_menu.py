import pygame
from pygame.locals import *
import sys

from menus import button
from utils.colours import Colours

class MainMenu():

    def __init__(self, window):
        self.screen = window
        self.font = pygame.font.SysFont(None, 48)

        self.buttons = [
            button.Button(self.screen, Colours.WHITE, self.__calc_position(0, -70), 240, 100, "Play"),
            button.Button(self.screen, Colours.WHITE, self.__calc_position(0, 70), 240, 100, "Settings"),
            button.Button(self.screen, Colours.WHITE, self.__calc_position(0, 210), 240, 100, "Exit"),
        ]

    def process_click(self, pos): # Execute actions for clicks directed to this menu
        for btn in self.buttons:
            if btn.check_collision(pos):
                print("collide")
                break

    def render(self): # Return render for this menu

        text = self.font.render("Gorillapong", True, Colours.WHITE)
        self.screen.blit(text, text.get_rect(center = self.__calc_position(0, -350)))

        for btn in self.buttons:
            btn.render()

    def __calc_position(self, w, h):
        return ((self.screen.get_width() / 2) + w, (self.screen.get_height() / 2) + h)
