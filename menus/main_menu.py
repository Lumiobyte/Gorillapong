import pygame
from pygame.locals import *
import sys
import os
import datetime

from menus import button, force_restart
from utils import database, renderutils
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
                button.Button(self.screen, stats_btn_colour, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(340, 300), 60, 60, "", 1005, False),
                button.Button(self.screen, music_btn_colour, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-110, -100), 60, 60, "", 1002, False),
                button.Button(self.screen, sound_btn_colour, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-110, -30), 60, 60, "", 1003, False),
                button.Button(self.screen, Colours.WHITE, Colours.ORANGEY_YELLOW, self.__calc_position(0, 70), 240, 100, "Adjust Volume", 1004),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_RED, self.__calc_position(0, 270), 240, 100, "Back", 0),

                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-450, -80), 200, 60, "1600x900", 1000),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-450, 0), 200, 60, "1280x720", 1001),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-450, 80), 200, 60, "Fullscreen", 999),

                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(390, -100), 130, 60, "Casual", 1010),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(540, -100), 130, 60, "Comp", 1011)
            ]
            self.texts = [
                ["Graphics", Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-450, -190), self.font],
                ["Audio", Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, -190), self.font],
                ["Gameplay", Colours.LIGHT_PASTEL_GREEN, self.__calc_position(460, -190), self.font],
                ["Toggle music", Colours.WHITE, self.__calc_position(10, -100), self.small_font],
                ["Toggle sound", Colours.WHITE, self.__calc_position(10, -30), self.small_font],
                ["Show stats for nerds", Colours.WHITE, self.__calc_position(500, 300), self.small_font]
            ]
        else:
            self.buttons = [
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-160, -80), 285, 100, "AI Showdown", 5),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-160, 40), 285, 100, "Play with AI", 4),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(160, -80), 285, 100, "Local Multiplayer", 3),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(160, 40), 285, 100, "Competitive", 7),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-210, 180), 190, 70, "Statistics", 8),
                button.Button(self.screen, Colours.WHITE, Colours.ORANGEY_YELLOW, self.__calc_position(0, 180), 190, 70, "Settings", 1),
                button.Button(self.screen, Colours.WHITE, Colours.LIGHT_RED, self.__calc_position(210, 180), 190, 70, "Exit", -1),
                button.Button(self.screen, Colours.WHITE, Colours.ORANGEY_YELLOW, self.__calc_position(700, 400), 180, 80, "Credits", 6)
            ]
            self.texts = []

        # Only for settings menu but putting them here is an easy way to fix errors
        self.variant_0_texts = [
            ["Score goal:", Colours.WHITE, self.__calc_position(310, 0), self.small_font],
            ["Ball speed:", Colours.WHITE, self.__calc_position(310, 60), self.small_font],
            ["Powerups:", Colours.WHITE, self.__calc_position(310, 120), self.small_font],
            ["AI difficulty:", Colours.WHITE, self.__calc_position(310, 180), self.small_font]
        ]

        self.variant_0_buttons = [
            button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(580, 10), 135, 30, "Value", 2000, font = self.small_font),
            button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(580, 70), 135, 30, "Value 2", 2001, font = self.small_font),
            button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(580, 130), 135, 30, "Value 3", 2002, font = self.small_font),
            button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(580, 190), 135, 30, "Value 4", 2003, font = self.small_font)
        ]

        self.variant_1_texts = [
            ["Score goal:", Colours.WHITE, self.__calc_position(310, 0), self.small_font],
            ["Ball speed:", Colours.WHITE, self.__calc_position(310, 60), self.small_font],
            ["Serve miss:", Colours.WHITE, self.__calc_position(310, 120), self.small_font],
            ["Ball speed up:", Colours.WHITE, self.__calc_position(310, 180), self.small_font]
        ]

        self.variant_1_buttons = [
            button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(580, 10), 135, 30, "Value", 2100, font = self.small_font),
            button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(580, 70), 135, 30, "Value 2", 2101, font = self.small_font),
            button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(580, 130), 135, 30, "Value 3", 2102, font = self.small_font),
            button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(580, 190), 135, 30, "Value 4", 2103, font = self.small_font)
        ]

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
            8: "Lifetime statistics from all play sessions",
            1000: "Change resolution to 1600x900",
            1001: "Change resolution to 1280x720",
            999: "Use Fullscreen mode (BETA)",
            1002: "Toggle music",
            1003: "Toggle sound",
            1004: "Adjust volume levels",
            1005: "Shows various debug information at the bottom of the game window",
            7: "Local multiplayer with higher stakes and a competitive experience",
            1010: "Gameplay settings for casual modes",
            1011: "Gameplay settings for competitive mode",
            2000: "The amount of points needed to win",
            2001: "The speed of the ball",
            2002: "Amount of powerups that spawn on the play field",
            2003: "Difficulty of the AI in Player VS AI mode",
            2100: "The amout of points needed to win",
            2101: "The speed of the ball",
            2102: "The penalty for missing a serve when the ball respawns",
            2103: "Enable the ball speed to slowly increase over time"
        }

        self.gameplay_settings_menu_variant = 0 # 0 = casual, 1 = comp

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
        self.__setup_gameplay_setting_buttons()

        self.version = "v0.17"
        self.version_text = self.font.render(self.version, True, Colours.WHITE)

        self.slider_texts = [
            self.small_font.render("Music Volume", True, Colours.WHITE),
            self.small_font.render("Sound Volume", True, Colours.WHITE)
        ]
        self.back_button = button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(0, 210), 240, 100, "Back", 1)

        self.stats_screen_playtime_options = ['total', 'ai vs ai', 'player vs ai', 'multiplayer', 'competitive']
        self.playtime_selected = 0


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
                        elif action == 1010:
                            self.gameplay_settings_menu_variant = 0
                        elif action == 1011:
                            self.gameplay_settings_menu_variant = 1
                        else:
                            if action == 4:
                                return 3, True
                            elif action == 5:
                                return 5, True
                            return action, False
                        
            if self.gameplay_settings_menu_variant == 0:
                for btn in self.variant_0_buttons:
                    self.__process_gameplay_settings_button(btn, pos, clicked)
            else:
                for btn in self.variant_1_buttons:
                    self.__process_gameplay_settings_button(btn, pos, clicked)
                        
            if clicked: # This fix kills me. The entire UI needs a rewrite
                return None, False
            
    def __process_gameplay_settings_button(self, btn, pos, clicked):
        if database.get_resolution() != database.get_max_resolution(): # Max res value in database again
            collided, action = btn.check_collision(self.__map_mouse_position(pos))
        else:
            collided, action = btn.check_collision(pos)

        if collided:
            btn.hover()
            self.hovered_button = action

            if clicked:
                self.sound.button_click()

                if action == 2000:
                    new_title = database.change_gameplay_setting("casual_score_goal")
                elif action == 2001:
                    new_title = database.change_gameplay_setting("casual_ball_speed")
                elif action == 2002:
                    new_title = database.change_gameplay_setting("casual_powerups")
                elif action == 2003:
                    new_title = database.change_gameplay_setting("casual_ai_difficulty")
                elif action == 2100:
                    new_title = database.change_gameplay_setting("comp_score_goal")
                elif action == 2101:
                    new_title = database.change_gameplay_setting("comp_ball_speed")
                elif action == 2102:
                    new_title = database.change_gameplay_setting("comp_serve_miss_penalty")
                elif action == 2103:
                    new_title = database.change_gameplay_setting("comp_ball_speedup")

                print(action)
                print(new_title)

                btn.title = new_title
            
            
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

            if self.screen_title == "Settings":

                res = database.get_resolution()
                if res == 0:
                    pygame.draw.rect(self.screen, Colours.ENABLED_GREEN, pygame.Rect(self.buttons[7].button_rect.left - 5, self.buttons[7].button_rect.top - 5, 210, 70), 5)
                elif res == (1600, 900):
                    pygame.draw.rect(self.screen, Colours.ENABLED_GREEN, pygame.Rect(self.buttons[5].button_rect.left - 5, self.buttons[5].button_rect.top - 5, 210, 70), 5)
                elif res == (1280, 720):
                    pygame.draw.rect(self.screen, Colours.ENABLED_GREEN, pygame.Rect(self.buttons[6].button_rect.left - 5, self.buttons[6].button_rect.top - 5, 210, 70), 5)

                pygame.draw.rect(self.screen, Colours.SCORE_GREY, pygame.Rect(1070, 415, 400, 285))
                if self.gameplay_settings_menu_variant == 0:
                    pygame.draw.polygon(self.screen, Colours.SCORE_GREY, ((1165, 415), (1215, 415), (1190, 390)))
                    for text in self.variant_0_texts:
                        self.screen.blit(text[3].render(text[0], True, text[1]), text[2])
                    for btn in self.variant_0_buttons:
                        btn.render()
                else:
                    pygame.draw.polygon(self.screen, Colours.SCORE_GREY, ((1315, 415), (1365, 415), (1340, 390)))
                    for text in self.variant_1_texts:
                        self.screen.blit(text[3].render(text[0], True, text[1]), text[2])
                    for btn in self.variant_1_buttons:
                        btn.render()

            #pygame.draw.circle(self.screen, Colours.PURPLE, (self.last_pos[0], self.last_pos[1]), radius=5) # DEBUG DOT 

    def process_render_credits_screen(self, pos, clicked = False):
        
        text = self.font.render("Credits", True, Colours.ORANGEY_YELLOW)
        self.screen.blit(text, text.get_rect(center = self.__calc_position(-200, -135)))

        self.screen.blit(self.font.render("Evan Partridge", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, -150))
        self.screen.blit(self.small_font.render("gameplay programming", True, Colours.WHITE), self.__calc_position(0, -115))

        self.screen.blit(self.font.render("James Mathieson", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, -70))
        self.screen.blit(self.small_font.render("chief vision officer and sprite artist", True, Colours.WHITE), self.__calc_position(0, -35))

        self.screen.blit(self.font.render("Oliver Alcaraz", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, 10))
        self.screen.blit(self.small_font.render("implemented lerp for ai paddles", True, Colours.WHITE), self.__calc_position(0, 45))

        self.screen.blit(self.font.render("Bray Croke", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, 90))
        self.screen.blit(self.small_font.render("ui design", True, Colours.WHITE), self.__calc_position(0, 125))

        self.screen.blit(self.font.render("Freesound Contributors", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, 170))
        self.screen.blit(self.small_font.render("game music and sound effects", True, Colours.WHITE), self.__calc_position(0, 205))
        
        #freesound_credits_button = button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(40, 245), 80, 30, "see all", 0, font = self.small_font)
        freesound_credits_button = button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(450, 185), 90, 30, "see all", 0, font = self.small_font)

        #self.screen.blit(self.font.render(f"Gorillapong {self.version}", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(0, 180))
        self.screen.blit(self.small_font.render(f"Gorillapong {self.version}", True, Colours.WHITE), self.__calc_position(-257, -115))

        if self.credits_back_button.check_collision(self.__map_mouse_position(pos))[0]:
            self.credits_back_button.hover()

            if clicked:
                self.sound.button_click() # Sound effect
                return 0
            
        if freesound_credits_button.check_collision(self.__map_mouse_position(pos))[0]:
            freesound_credits_button.hover()

            if clicked:
                self.sound.button_click() # Sound effect
                try:
                    os.startfile('sound_credits.txt')
                except:
                    pass
                return 6

        self.credits_back_button.render()
        freesound_credits_button.render()

        return None
    
    def process_render_statistics_screen(self, pos, clicked):

        statistics = database.get_all_stats()

        playtimes = [
            renderutils.format_timedelta(datetime.timedelta(seconds = statistics['total_playtime'])),
            renderutils.format_timedelta(datetime.timedelta(seconds = statistics['playtime_0'])),
            renderutils.format_timedelta(datetime.timedelta(seconds = statistics['playtime_1'])),
            renderutils.format_timedelta(datetime.timedelta(seconds = statistics['playtime_2'])),
            renderutils.format_timedelta(datetime.timedelta(seconds = statistics['playtime_3']))
        ]

        text = self.font.render("Statistics", True, Colours.ORANGEY_YELLOW)
        self.screen.blit(text, text.get_rect(center = self.__calc_position(0, -350)))

        self.screen.blit(self.font.render("Playtime", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(-550, -200))
        self.screen.blit(self.font.render(playtimes[self.playtime_selected], True, Colours.WHITE), self.__calc_position(-530, -160))

        self.screen.blit(self.font.render("Total Ball Pixels Travelled", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(-550, -70))
        self.screen.blit(self.font.render(str(round(statistics['total_pixels_travelled'])) + " px", True, Colours.WHITE), self.__calc_position(-530, -30))

        self.screen.blit(self.font.render("Total Bounces", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(-550, 70))
        self.screen.blit(self.font.render(str(statistics['total_bounces']), True, Colours.WHITE), self.__calc_position(-530, 110))

        self.screen.blit(self.font.render("Total Powerups Collected", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(-550, 200))
        self.screen.blit(self.font.render(str(statistics['total_powerups']), True, Colours.WHITE), self.__calc_position(-530, 240))

        self.screen.blit(self.font.render("Total Serves Missed", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(200, -200))
        self.screen.blit(self.font.render(str(statistics['serves_missed']), True, Colours.WHITE), self.__calc_position(220, -160))

        self.screen.blit(self.font.render("Total Points Scored", True, Colours.LIGHT_PASTEL_GREEN), self.__calc_position(200, -70))
        self.screen.blit(self.font.render(f"Yellow: {statistics['total_points_scored_p1']}", True, Colours.PLAYER_YELLOW), self.__calc_position(220, -30))
        self.screen.blit(self.font.render(f"Green: {statistics['total_points_scored_p2']}", True, Colours.PLAYER_GREEN), self.__calc_position(225, 10))

        playtime_gamemode_button = button.Button(self.screen, Colours.WHITE, Colours.LIGHT_PASTEL_GREEN, self.__calc_position(-320, -185), 150, 30, self.stats_screen_playtime_options[self.playtime_selected], 0, font = self.small_font)
        reset_stats_button = button.Button(self.screen, Colours.WHITE, Colours.LIGHT_RED, self.__calc_position(-630, 400), 320, 80, "Reset Statistics", 0)

        if self.credits_back_button.check_collision(self.__map_mouse_position(pos))[0]:
            self.credits_back_button.hover()

            if clicked:
                self.sound.button_click() # Sound effect
                return 0
            
        
        if playtime_gamemode_button.check_collision(self.__map_mouse_position(pos))[0]:
            playtime_gamemode_button.hover()

            if clicked:
                self.sound.button_click() # Sound effect
                self.playtime_selected += 1
                if self.playtime_selected > 4:
                    self.playtime_selected = 0

        if reset_stats_button.check_collision(self.__map_mouse_position(pos))[0]:
            reset_stats_button.hover()

            if clicked:
                self.sound.button_click() # Sound effect
                database.reset_stats()
    
        self.credits_back_button.render()
        playtime_gamemode_button.render()
        reset_stats_button.render()

        return None
    
    def __setup_gameplay_setting_buttons(self):
        counter = 0
        for setting_title in database.get_all_gameplay_settings():
            if counter > 3:
                self.variant_1_buttons[counter - 4].title = setting_title
            else:
                #print(self.variant_0_buttons[counter].title)
                self.variant_0_buttons[counter].title = setting_title
                #print(setting_title)
                #print(counter)

            counter += 1

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
