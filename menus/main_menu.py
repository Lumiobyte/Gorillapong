import pygame
from pygame.locals import *
import sys

from menus import button

class MainMenu():

    def __init__(self, window):
        self._window = window

        self.buttons = [button.Button(self._window, (255, 255, 255), 10, 10, 50, 25)]

    def process_click(self, pos): # Execute actions for clicks directed to this menu
        for btn in self.buttons:
            if btn.check_collision(pos):
                print("collide")
                break

    def render(self): # Return render for this menu
        for btn in self.buttons:
            btn.render()