import pygame
from pygame.locals import *
import sys

from menus import button, force_restart
from utils import database
from utils.colours import Colours

class MainMenu():

    def __init__(self, window, display_screen, title, sound):
        self.screen = window
        self.screen_title = title
        self.display_screen = display_screen
        self.title_font = pygame.font.SysFont(None, 74)
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)

        self.sound = sound

        self.last_pos = (50, 50) # debug feature

        # goriller sproit
        # poigaim.image.lode()
        self.gorilla_ball = pygame.image.load('image/gorilla.png')

        data = database.get_music_sound()
        if data[0] == True:
            music_btn_colour = Colours.ENABLED_GREEN
        else:
            music_btn_colour = Colours.LIGHT_PASTEL_RED
        if data[1] == True:
            sound_btn_colour = Colours.ENABLED_GREEN
        else:
            sound_btn_colour = Colours.LIGHT_PASTEL_RED

        data = database.get_stats_toggle()
        if data:
            stats_btn_colour = Colours.ENABLED_GREEN
        else:
            stats_btn_colour = Colours.LIGHT_PASTEL_RED

        if self.screen_title == "Settings":
            self.buttons = [
                button.Button(self.screen, stats_btn_colour, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(290, -100), 60, 60, "", 1005, False),
                button.Button(self.screen, music_btn_colour, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-110, -100), 60, 60, "", 1002, False),
                button.Button(self.screen, sound_btn_colour, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-110, -30), 60, 60, "", 1003, False),
                button.Button(self.screen, Colours.WHITE, Colours.ORANGEY_YELLOW, self.__calc_position(0, 70), 240, 100, "Adjust Volume", 1004),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_RED, self.__calc_position(0, 270), 240, 100, "Back", 0),

                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-450, -80), 200, 60, "1600x900", 1000),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-450, 0), 200, 60, "1280x720", 1001),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-450, 80), 200, 60, "Fullscreen", 999)
            ]
            self.texts = [
                ["Graphics", Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-450, -190), self.font],
                ["Audio", Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, -190), self.font],
                ["Other", Colours.LIGHT_PASTEL_GREEN, self.__calc_position(450, -190), self.font],
                ["Toggle music", Colours.WHITE, self.__calc_position(10, -100), self.small_font],
                ["Toggle sound", Colours.WHITE, self.__calc_position(10, -30), self.small_font],
                ["Show stats for nerds", Colours.WHITE, self.__calc_position(450, -100), self.small_font]
            ]
        else:
            self.buttons = [
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-160, -80), 285, 100, "AI Showdown", 5),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-160, 40), 285, 100, "Play with AI", 4),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(160, -80), 285, 100, "Local Multiplayer", 3),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(160, 40), 285, 100, "Competitive", 7),
                button.Button(self.screen, Colours.WHITE, Colours.ORANGEY_YELLOW, self.__calc_position(-110, 180), 200, 70, "Settings", 1),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_RED, self.__calc_position(110, 180), 200, 70, "Exit", -1),
                button.Button(self.screen, Colours.WHITE, Colours.ORANGEY_YELLOW, self.__calc_position(700, 400), 180, 80, "Credits", 6)
            ]
            self.texts = []

        #self.info_text_font = pygame.font.SysFont()
        self.hovered_button = 0
        self.info_texts = {
            0: "",
            5: "Watch two bots face off in an epic Double Pong 1v1!",
            4: "No friends? No worries! Play against Ed Townsend, our friendly Double Pong AI!",
            3: "Duel your friends in the Double Pong arena!",
            1: "Contracted malaria? Don't forget to configue your settings!",
            -1: "Sorry to see you go :(",
            6: "See the wonderful people behind the game!",
            1000: "Change resolution to 1600x900",
            1001: "Change resolution to 1280x720",
            999: "Use Fullscreen mode (BETA)",
            1002: "Toggle music",
            1003: "Toggle sound",
            1004: "Adjust volume levels",
            1005: "Shows various debug information at the bottom of the game window",
            7: "Local multiplayer with higher stakes and a competitive experience"
        }

        self.credits_back_button = button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(700, 400), 180, 80, "Back", 0)

        data = database.get_volume()
        self.music_vol = data[0]
        self.sound_vol = data[1]

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

        self.version = "v0.15"
        self.version_text = self.font.render(self.version, True, Colours.WHITE)

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

            self.hovered_button = 0

            for btn in self.buttons:
                if database.get_resolution() != database.get_max_resolution(): # Max res value in database again
                    collided, action = btn.check_collision(self.__map_mouse_position(pos))
                else:
                    collided, action = btn.check_collision(pos)

                if collided:

                    btn.hover()

                    self.hovered_button = btn.button_action

                    if clicked:
                        self.sound.button_click() # Sound effect
                        if action == 999:
                            database.set_resolution((0, 0))
                            force_restart.force_restart("Resolution has been updated to Fullscreen")
                        elif action == 1000:
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
                        elif action == 1005:
                            value = database.toggle_stats_toggle()
                            if value:
                                btn.colour = Colours.ENABLED_GREEN
                            else:
                                btn.colour = Colours.LIGHT_PASTEL_RED
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
            self.screen.blit(self.version_text, (20, 850))
            text = self.title_font.render(self.screen_title, True, Colours.WHITE)
            self.screen.blit(text, text.get_rect(center = self.__calc_position(0, -350)))
            if self.screen_title == "Gorillapong":
                self.screen.blit(self.gorilla_ball, (self.__calc_position(-107, -364)))

            for btn in self.buttons:
                btn.render()
            
            for text in self.texts: # 0: the text itself, 1: text colour, 2: text position (already centered), 3: font object
                r_text = text[3].render(text[0], True, text[1])
                self.screen.blit(r_text, r_text.get_rect(center = text[2]))

            info_text = self.small_font.render(self.info_texts[self.hovered_button], True, Colours.WHITE)
            self.screen.blit(info_text, info_text.get_rect(center = self.__calc_position(0, 400)))

            #pygame.draw.circle(self.screen, Colours.PURPLE, (self.last_pos[0], self.last_pos[1]), radius=5) # DEBUG DOT 

    def process_render_credits_screen(self, pos, clicked = False):
        
        text = self.font.render("Credits", True, Colours.ORANGEY_YELLOW)
        self.screen.blit(text, text.get_rect(center = self.__calc_position(-200, -135)))

        self.screen.blit(self.font.render("Evan Partridge", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, -150))
        self.screen.blit(self.small_font.render("did everything", True, Colours.WHITE), self.__calc_position(0, -115))

        self.screen.blit(self.font.render("James Mathieson", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, -70))
        self.screen.blit(self.small_font.render("emotional support and debugging", True, Colours.WHITE), self.__calc_position(0, -35))

        self.screen.blit(self.font.render("Oliver Alcaraz", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, 10))
        self.screen.blit(self.small_font.render("knows lerp math", True, Colours.WHITE), self.__calc_position(0, 45))

        self.screen.blit(self.font.render("Bray Croke", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, 90))
        self.screen.blit(self.small_font.render("some contribution to the main menu", True, Colours.WHITE), self.__calc_position(0, 125))

        #self.screen.blit(self.font.render(f"Gorillapong {self.version}", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, 180))
        self.screen.blit(self.small_font.render(f"Gorillapong {self.version}", True, Colours.WHITE), self.__calc_position(-257, -115))

        if self.credits_back_button.check_collision(self.__map_mouse_position(pos))[0]:
            self.credits_back_button.hover()

            if clicked:
                self.sound.button_click() # Sound effect
                return 0

        self.credits_back_button.render()

        return None


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

        if self.display_screen:
            res = self.display_screen.get_size()
        else:
            res = self.screen.get_size()

        x_map = ((1600) / (res[0]) * (pos[0]))
        y_map = ((900) / (res[1]) * (pos[1]))

        return (x_map, y_map)
