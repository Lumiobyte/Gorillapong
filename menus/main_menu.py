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
        self.small_font = pygame.font.SysFont(None, 32)

        self.sound = sound

        self.last_pos = (50, 50) # debug feature

        data = database.get_music_sound()
        if data[0] == True:
            music_btn_colour = Colours.ENABLED_GREEN
        else:
            music_btn_colour = Colours.LIGHT_PASTEL_RED
        if data[1] == True:
            sound_btn_colour = Colours.ENABLED_GREEN
        else:
            sound_btn_colour = Colours.LIGHT_PASTEL_RED

        if self.screen_title == "Settings":
            self.buttons = [
                button.Button(self.screen, music_btn_colour, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(125, -70), 240, 100, "MUSIC", 1002, False),
                button.Button(self.screen, sound_btn_colour, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-125, -70), 240, 100, "SOUND", 1003, False),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 70), 240, 100, "Adjust Volume", 1004),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 210), 240, 100, "Back", 0),

                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-110, -180), 200, 60, "1600x900", 1000),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(110, -180), 200, 60, "1280x720", 1001)
            ]
        else:
            self.buttons = [
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-300, -70), 240, 100, "AI Showdown", 5),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, -70), 240, 100, "Play with AI", 4),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(300, -70), 240, 100, "Local Multiplayer", 3),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 70), 240, 100, "Settings", 1),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 210), 240, 100, "Exit", -1),
            ]

        self.sound_vol = 1
        self.music_vol = 1

        self.adjust_volume_menu = False
        w = 300
        h = 60
        self.slider_boxes = [
            pygame.Rect(self.__calc_position(0, 50)[0] - (w / 2), self.__calc_position(0, 50)[1] - (h / 2), w, h),
            pygame.Rect(self.__calc_position(0, -70)[0] - (w / 2), self.__calc_position(0, -70)[1] - (h / 2), w, h)
        ]

        self.slider_buttons = [
            button.Button(self.screen, Colours.SCORE_GREY, Colours.DARK_GREEN, self.__calc_position(0, 50), 52, 52, "", 1005),
            button.Button(self.screen, Colours.SCORE_GREY, Colours.DARK_GREEN, self.__calc_position(0, -70), 52, 52, "", 1006)
        ]

        self.__position_slider_buttons()

        self.slider_texts = [
            self.small_font.render("Music Volume", True, Colours.WHITE),
            self.small_font.render("Sound Volume", True, Colours.WHITE)
        ]
        self.back_button = button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 210), 240, 100, "Back", 1)


    def process_position(self, pos, clicked = False): # Execute actions for clicks directed to this menu

        if self.adjust_volume_menu:
            collided, action = self.back_button.check_collision(self.__map_mouse_position(pos))
            if collided:
                self.back_button.hover()

                if clicked:
                    self.sound.button_click() # Sound effect
                    if action == 1:
                        self.adjust_volume_menu = False 
                        database.set_volume("music_vol", self.music_vol)
                        database.set_volume("sound_vol", self.sound_vol)
                        self.sound.reinit()
                        return action, False
                    
            for btn in self.slider_buttons:
                collided, action = btn.check_collision(self.__map_mouse_position(pos))
                if collided:
                    btn.hover()

                    if clicked:
                        self.sound.button_click() # Sound effect
                    
            if clicked:
                return None, False

        else:
            self.last_pos = pos

            for btn in self.buttons:
                if database.get_resolution != database.get_max_resolution(): # Max res value in database again
                    collided, action = btn.check_collision(self.__map_mouse_position(pos))
                else:
                    collided, action = btn.check_collision(pos)

                if collided:

                    btn.hover()

                    if clicked:
                        self.sound.button_click() # Sound effect
                        if action == 1000:
                            database.set_resolution((1600, 900))
                            force_restart.force_restart("Resolution has been updated to 1600x900")
                        elif action == 1001:
                            database.set_resolution((1280, 720))
                            force_restart.force_restart("Resolution has been updated to 1280x720")
                        elif action == 1002:
                            value = database.toggle_music_sound("music")
                            self.sound.reinit()
                            if value == True:
                                btn.colour = Colours.ENABLED_GREEN
                            else:
                                btn.colour = Colours.LIGHT_PASTEL_RED
                        elif action == 1003:
                            value = database.toggle_music_sound("sound")
                            self.sound.reinit()
                            if value == True:
                                btn.colour = Colours.ENABLED_GREEN
                            else:
                                btn.colour = Colours.LIGHT_PASTEL_RED
                        elif action == 1004:
                            self.adjust_volume_menu = True
                            self.__prep_volume_menu()
                            return None, False
                        else:
                            if action == 4:
                                return 3, True
                            elif action == 5:
                                return 5, True
                            return action, False
                        
            if clicked: # This fix kills me. The entire UI needs a rewrite
                return None, False
            
    def process_hold(self, pos):
        if self.adjust_volume_menu:
            pos = self.__map_mouse_position(pos)
            for i, btn in enumerate(self.slider_buttons):
                collided, action = btn.check_collision(pos)

                if collided:
                    btn.hover()
                    #self.sound.button_click() # Sound effect

                    new_btn_pos = [pos[0], btn.center[1]]
                    limit_left = (self.slider_boxes[i].left + 5 + (btn.w / 2))
                    limit_right = ((self.slider_boxes[i].left + self.slider_boxes[i].width) - 5 - (btn.w / 2))
                    if new_btn_pos[0] < limit_left:
                        new_btn_pos[0] = limit_left
                    elif new_btn_pos[0] > limit_right:
                        new_btn_pos[0] = limit_right

                    btn.move(new_btn_pos)
                    vol = self.__pos_to_volume(btn, self.slider_boxes[i], (limit_left, limit_right))

                    if action == 1005:
                        self.music_vol = vol
                    elif action == 1006:
                        self.sound_vol = vol


    def render(self): # Return render for this menu

        if self.adjust_volume_menu:
            text = self.font.render("Adjust Volume", True, Colours.WHITE)
            self.screen.blit(text, text.get_rect(center = self.__calc_position(0, -350)))

            for i, box in enumerate(self.slider_boxes):
                pygame.draw.rect(self.screen, Colours.WHITE, box)
                pygame.draw.rect(self.screen, Colours.LIGHT_GREY, pygame.Rect(box.left + 6, box.top + 7, (self.slider_buttons[i].center[0] - box.left), (box.height - 14)))
                self.slider_buttons[i].render()
                self.screen.blit(self.slider_texts[i], (box.left + 15, box.top - 28))


            self.back_button.render()
        else:
            text = self.font.render(self.screen_title, True, Colours.WHITE)
            self.screen.blit(text, text.get_rect(center = self.__calc_position(0, -350)))

            for btn in self.buttons:
                btn.render()

            #pygame.draw.circle(self.screen, Colours.PURPLE, (self.last_pos[0], self.last_pos[1]), radius=5) # DEBUG DOT 

    def __prep_volume_menu(self):
        self.slider_texts = []
        result = database.get_music_sound()
        if result[0]:
            self.slider_texts.append(self.small_font.render("Music Volume", True, Colours.ENABLED_GREEN))
        else:
            self.slider_texts.append(self.small_font.render("Music Volume", True, Colours.LIGHT_PASTEL_RED))
        if result[1]:
            self.slider_texts.append(self.small_font.render("Sound Volume", True, Colours.ENABLED_GREEN))
        else:
            self.slider_texts.append(self.small_font.render("Sound Volume", True, Colours.LIGHT_PASTEL_RED))

        self.__position_slider_buttons()

    def __position_slider_buttons(self):

        data = database.get_volume()

        limits1 = ((self.slider_boxes[0].left + 5 + (self.slider_buttons[0].w / 2)), ((self.slider_boxes[0].left + self.slider_boxes[0].width) - 5 - (self.slider_buttons[0].w / 2)))
        limits2 = ((self.slider_boxes[1].left + 5 + (self.slider_buttons[1].w / 2)), ((self.slider_boxes[1].left + self.slider_boxes[1].width) - 5 - (self.slider_buttons[1].w / 2)))

        self.slider_buttons = [
            button.Button(self.screen, Colours.SCORE_GREY, Colours.DARK_GREEN, self.__calc_position(self.__volume_to_pos(data[0], limits1) - (self.screen.get_width() / 2), 50), 52, 52, "", 1005),
            button.Button(self.screen, Colours.SCORE_GREY, Colours.DARK_GREEN, self.__calc_position(self.__volume_to_pos(data[1], limits2) - (self.screen.get_width() / 2), -70), 52, 52, "", 1006)
        ]

    def __pos_to_volume(self, button, slider, limits):
        coord_range = limits[1] - limits[0]

        #vol = 1 / ((button.center[0] - limits[1]) + 0.1)

        vol = 0.0 + ((1.0 - 0.0) / (coord_range)) * (button.center[0] - limits[0])
        
        return round(vol, 3)
    
    def __volume_to_pos(self, vol, limits):
        coord_range = limits[1] - limits[0]

        vol = limits[0] + ((coord_range) / (1.0 - 0.0)) * (vol - 0.0)

        return round(vol)

    def __calc_position(self, w, h):
        return ((self.screen.get_width() / 2) + w, (self.screen.get_height() / 2) + h)
    
    # Should make the database have a max res value so that these aren't hardcoded
    def __map_mouse_position(self, pos):
        #output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)

        res = database.get_resolution()

        x_map = ((1600) / (res[0]) * (pos[0]))
        y_map = ((900) / (res[1]) * (pos[1]))

        return (x_map, y_map)
