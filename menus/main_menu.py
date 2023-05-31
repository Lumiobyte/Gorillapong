import pygame
from pygame.locals import *
import sys

from menus import button, force_restart
from utils import database
from utils.colours import Colours

class MainMenu():

    def __init__(self, window, title, sound):
        self.screen = window
        self.screen_title = title
        self.font = pygame.font.SysFont(None, 48)

        self.sound = sound

        self.last_pos = (50, 50) # debug feature

        if self.screen_title == "Settings":
            self.buttons = [
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, -70), 240, 100, "Placeholder", 1),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 70), 240, 100, "Placeholder", 1),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 210), 240, 100, "Back", 0),

                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-110, -180), 200, 60, "1600x900", 1000),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(110, -180), 200, 60, "1280x720", 1001)
            ]
        else:
            self.buttons = [
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-150, -70), 240, 100, "Play with AI", 4),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(150, -70), 240, 100, "Local Multiplayer", 3),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 70), 240, 100, "Settings", 1),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 210), 240, 100, "Exit", -1),
            ]

    def process_position(self, pos, clicked = False): # Execute actions for clicks directed to this menu

        self.last_pos = pos

        for btn in self.buttons:
            if database.get_resolution != database.get_max_resolution(): # Max res value in database again
                collided, action = btn.check_collision(self.__map_mouse_position(pos))
            else:
                collided, action = btn.check_collision(pos)

            if collided:

                btn.hover()

                if clicked:
                    self.sound.button_click()
                    if action == 1000:
                        database.set_resolution((1600, 900))
                        force_restart.force_restart("Resolution has been updated to 1600x900")
                    elif action == 1001:
                        database.set_resolution((1280, 720))
                        force_restart.force_restart("Resolution has been updated to 1280x720")
                    else:
                        if action == 4:
                            return 3, True
                        return action, False
                    
        if clicked: # This fix kills me. The entire UI needs a rewrite
            return None, False

    def render(self): # Return render for this menu

        text = self.font.render(self.screen_title, True, Colours.WHITE)
        self.screen.blit(text, text.get_rect(center = self.__calc_position(0, -350)))

        for btn in self.buttons:
            btn.render()

        #pygame.draw.circle(self.screen, Colours.PURPLE, (self.last_pos[0], self.last_pos[1]), radius=5) # DEBUG DOT 

    def __calc_position(self, w, h):
        return ((self.screen.get_width() / 2) + w, (self.screen.get_height() / 2) + h)
    
    # Should make the database have a max res value so that these aren't hardcoded
    def __map_mouse_position(self, pos):
        #output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)

        res = database.get_resolution()

        x_map = ((1600) / (res[0]) * (pos[0]))
        y_map = ((900) / (res[1]) * (pos[1]))

        return (x_map, y_map)
