import pygame
from pygame.locals import *
import sys

from menus import button
from utils.colours import Colours

class MainMenu():

    def __init__(self, window, title):
        self.screen = window
        self.screen_title = title
        self.font = pygame.font.SysFont(None, 48)

        if self.screen_title == "Settings":
            self.buttons = [
                button.Button(self.screen, Colours.WHITE, self.__calc_position(0, -70), 240, 100, "Placeholder", 1),
                button.Button(self.screen, Colours.WHITE, self.__calc_position(0, 70), 240, 100, "Placeholder", 1),
                button.Button(self.screen, Colours.WHITE, self.__calc_position(0, 210), 240, 100, "Back", 0),
            ]
        else:
            self.buttons = [
                button.Button(self.screen, Colours.WHITE, self.__calc_position(0, -70), 240, 100, "Play", 3),
                button.Button(self.screen, Colours.WHITE, self.__calc_position(0, 70), 240, 100, "Settings", 1),
                button.Button(self.screen, Colours.WHITE, self.__calc_position(0, 210), 240, 100, "Exit", -1),
            ]

    def process_click(self, pos): # Execute actions for clicks directed to this menu
        for btn in self.buttons:
            collided, action = btn.check_collision(pos)
            if collided:
                return action

    def render(self): # Return render for this menu

        text = self.font.render(self.screen_title, True, Colours.WHITE)
        self.screen.blit(text, text.get_rect(center = self.__calc_position(0, -350)))

        for btn in self.buttons:
            btn.render()

    def __calc_position(self, w, h):
        return ((self.screen.get_width() / 2) + w, (self.screen.get_height() / 2) + h)
