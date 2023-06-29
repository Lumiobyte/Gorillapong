import pygame

from utils import database

class Audio():
    def __init__(self):
        pygame.mixer.init(channels = 8)

        self.filepath = "./sound/"

        data = database.get_volume()
        self.music_vol = data[0]
        self.sound_vol = data[1]

        data = database.get_music_sound()
        self.music_enabled = data[0]
        self.sound_enabled = data[1]

        self.menu_music_playing = False
        self.game_music_playing = False

        self.pop = pygame.mixer.Sound(self.filepath + 'pop.mp3')
        self.pop.set_volume(self.sound_vol)
        self.score = pygame.mixer.Sound(self.filepath + 'score.mp3')
        self.score.set_volume(self.sound_vol)
        self.loss = pygame.mixer.Sound(self.filepath + 'bad.wav')
        self.loss.set_volume(self.sound_vol)

        self.crunch = pygame.mixer.Sound(self.filepath + 'crunch.wav')
        self.crunch.set_volume(self.sound_vol)
        self.pickle_pickup = pygame.mixer.Sound(self.filepath + 'glassclink.wav')
        self.pickle_pickup.set_volume(self.sound_vol)
        self.pickle_smash = pygame.mixer.Sound(self.filepath + 'jarsmash.wav')
        self.pickle_smash.set_volume(self.sound_vol)
        self.water_pour = pygame.mixer.Sound(self.filepath + 'waterpour.wav')
        self.water_pour.set_volume(self.sound_vol)
        self.water_entry_splash = pygame.mixer.Sound(self.filepath + 'watersplash.wav')
        self.water_entry_splash.set_volume(self.sound_vol)
        self.water_exit_splash = pygame.mixer.Sound(self.filepath + 'watersplashdrip.wav')
        self.water_exit_splash.set_volume(self.sound_vol)
        self.swish_up = pygame.mixer.Sound(self.filepath + 'swishup.wav')
        self.swish_up.set_volume(self.sound_vol)
        self.swish_down = pygame.mixer.Sound(self.filepath + 'swishdown.flac')
        self.swish_down.set_volume(self.sound_vol)
        self.computer_on = pygame.mixer.Sound(self.filepath + 'computeractivate.mp3')
        self.computer_on.set_volume(self.sound_vol)
        self.computer_off = pygame.mixer.Sound(self.filepath + 'computerfail.mp3')
        self.computer_off.set_volume(self.sound_vol)
        self.paint_splash = pygame.mixer.Sound(self.filepath + 'paint.wav')
        self.paint_splash.set_volume(self.sound_vol)

        self.hover = pygame.mixer.Sound(self.filepath + 'hover.wav')
        self.hover.set_volume(self.sound_vol)
        self.click = pygame.mixer.Sound(self.filepath + 'select.mp3')
        self.click.set_volume(self.sound_vol)

        self.countdown_beep_sound = pygame.mixer.Sound(self.filepath + 'countdown_beep.wav')
        self.countdown_beep_sound.set_volume(self.sound_vol)

    def reinit(self):
        pygame.mixer.music.stop()
        self.__init__()
        self.play_menu_music()

    def play_menu_music(self):
        if not self.menu_music_playing and self.music_enabled:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(self.music_vol * 1.8)
            pygame.mixer.music.load(self.filepath + 'mainmenu_music_vapor.wav')
            pygame.mixer.music.play(-1)
            self.menu_music_playing = True
            self.game_music_playing = False

    def play_game_music(self):
        if not self.game_music_playing and self.music_enabled:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(self.music_vol * 0.6)
            pygame.mixer.music.load(self.filepath + 'gameplay_music_loop_vapor.wav')
            pygame.mixer.music.play(-1)
            self.game_music_playing = True
            self.menu_music_playing = False

    def play_comp_music(self):
        if not self.game_music_playing and self.music_enabled:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(self.music_vol * 0.6)
            pygame.mixer.music.load(self.filepath + 'comp_music.wav')
            pygame.mixer.music.play(-1)
            self.game_music_playing = True
            self.menu_music_playing = False
        
    def stop_music(self):
        pygame.mixer.music.stop()
        self.game_music_playing = False
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

    def computer_pickup(self):
        if self.sound_enabled:
            self.computer_on.play()

    def countdown_beep(self):
        if self.sound_enabled:
            self.countdown_beep_sound.play()