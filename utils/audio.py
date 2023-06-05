import pygame

from utils import database

class Audio():
    def __init__(self):
        pygame.mixer.init(channels = 8)

        self.filepath = "./sound/"

        self.pop = pygame.mixer.Sound(self.filepath + 'pop.mp3')
        self.score = pygame.mixer.Sound(self.filepath + 'score.mp3')
        self.loss = pygame.mixer.Sound(self.filepath + 'bad.wav')

        self.crunch = pygame.mixer.Sound(self.filepath + 'crunch.wav')
        self.pickle_pickup = pygame.mixer.Sound(self.filepath + 'glassclink.wav')
        self.pickle_smash = pygame.mixer.Sound(self.filepath + 'jarsmash.wav')
        self.water_pour = pygame.mixer.Sound(self.filepath + 'waterpour.wav')
        self.water_entry_splash = pygame.mixer.Sound(self.filepath + 'watersplash.wav')
        self.water_exit_splash = pygame.mixer.Sound(self.filepath + 'watersplashdrip.wav')
        self.swish_up = pygame.mixer.Sound(self.filepath + 'swishup.wav')
        self.swish_down = pygame.mixer.Sound(self.filepath + 'swishdown.flac')

        self.hover = pygame.mixer.Sound(self.filepath + 'hover.wav')
        self.click = pygame.mixer.Sound(self.filepath + 'select.mp3')

        self.menu_music_vol = 1.5 # database.get * 1.5
        self.game_music_vol = 0.3 # database.get * 0.5

        data = database.get_music_sound()
        self.music_enabled = data[0]
        self.sound_enabled = data[1]

        self.menu_music_playing = False
        self.game_music_playing = False

    def reinit(self):
        pygame.mixer.music.stop()
        self.__init__()
        self.play_menu_music()

    def play_menu_music(self):
        pygame.mixer.music.stop()

        if not self.menu_music_playing and self.music_enabled:
            pygame.mixer.music.set_volume(self.menu_music_vol)
            pygame.mixer.music.load(self.filepath + 'mainmenu_music_vapor.wav')
            pygame.mixer.music.play(-1)
            self.menu_music_playing = True
            self.game_music_playing = False

    def play_game_music(self):
        pygame.mixer.music.stop()

        if not self.game_music_playing and self.music_enabled:
            pygame.mixer.music.set_volume(self.game_music_vol)
            pygame.mixer.music.load(self.filepath + 'gameplay_music_loop_vapor.wav')
            pygame.mixer.music.play(-1)
            self.game_music_playing = True
            self.menu_music_playing = False
        
    def bounce(self):
        if self.sound_enabled:
            self.pop.play()

    def hit_pringle(self):
        if self.sound_enabled:
            self.crunch.play()

    def pickle_jar_pickup(self):
        if self.sound_enabled:
            self.pickle_pickup.play()
    
    def pickle_jar_break(self):
        if self.sound_enabled:
            self.pickle_smash.play()

    def water_pickup(self):
        if self.sound_enabled:
            #self.water_pour.play()
            pass

    def water_enter(self):
        if self.sound_enabled:
            self.water_entry_splash.play()

    def water_exit(self):
        if self.sound_enabled:
            self.water_exit_splash.play()

    def button_hover(self):
        if self.sound_enabled:
            self.hover.play()

    def button_click(self):
        if self.sound_enabled:
            self.click.play()

    def score_point(self):
        if self.sound_enabled:
            self.score.play()

    def pineapple_pickup(self):
        if self.sound_enabled:
            self.swish_up.play()
    
    def pineapple_expire(self):
        if self.sound_enabled:
            self.swish_down.play()

    def lives_run_out(self):
        if self.sound_enabled:
            self.loss.play()