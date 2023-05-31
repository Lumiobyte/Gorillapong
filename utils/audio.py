import pygame

class Audio():
    def __init__(self):
        pygame.mixer.init(channels = 8)

        self.filepath = "./sound/"

        self.pop = pygame.mixer.Sound(self.filepath + 'pop.mp3')
        self.score = pygame.mixer.Sound(self.filepath + 'score.mp3')
        self.loss = pygame.mixer.Sound(self.filepath + 'bad-boosted.wav')

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


        self.menu_music_playing = False
        self.game_music_playing = False

    def play_menu_music(self):
        if not self.menu_music_playing:
            pygame.mixer.music.set_volume(1.5)
            pygame.mixer.music.load(self.filepath + 'mainmenu_music_vapor.wav')
            pygame.mixer.music.play(-1)
            self.menu_music_playing = True
            self.game_music_playing = False

    def play_game_music(self):
        if not self.game_music_playing:
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.load(self.filepath + 'gameplay_music_loop_vapor.wav')
            pygame.mixer.music.play(-1)
            self.game_music_playing = True
            self.menu_music_playing = False
        
    def bounce(self):
        self.pop.play()

    def hit_pringle(self):
        self.crunch.play()

    def pickle_jar_pickup(self):
        self.pickle_pickup.play()
    
    def pickle_jar_break(self):
        self.pickle_smash.play()

    def water_pickup(self):
        #self.water_pour.play()
        pass

    def water_enter(self):
        self.water_entry_splash.play()

    def water_exit(self):
        self.water_exit_splash.play()

    def button_hover(self):
        self.hover.play()

    def button_click(self):
        self.click.play()

    def score_point(self):
        self.score.play()

    def pineapple_pickup(self):
        self.swish_up.play()
    
    def pineapple_expire(self):
        self.swish_down.play()

    def lives_run_out(self):
        self.loss.play()