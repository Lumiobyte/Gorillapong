import os
import sys
import pygame
from pygame.locals import *
import time

from utils import database
from utils.colours import Colours
from utils.renderutils import check_exe

def force_restart(note):
    """ This is used to restart the game after a resolution change. It will attempt to do so once automatically, but otherwise, notifies the user. """

    restart_attempted = False

    clock = pygame.time.Clock()
    if database.get_resolution() == pygame.FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(database.get_resolution())
    font = pygame.font.SysFont(None, 48)

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(Colours.BG_GREY)

        if restart_attempted:
            screen.blit(font.render("It is necessary to restart the game.", True, Colours.PLAYER_RED), (50, 100))
            screen.blit(font.render("Press ESC key to exit the game.", True, Colours.WHITE), (50, 140))
        else:
            screen.blit(font.render("Please wait...", True, Colours.WHITE), (50, 140))

        screen.blit(font.render(note, True, Colours.PLAYER_GREEN), (50, 240))

        pygame.display.update()
        clock.tick(147)

        if not restart_attempted:
            # Try to restart game automatically
            try:
                time.sleep(2) # Hopefully will be enough time for the telemetry logs to be sent
                os.execl(sys.executable, sys.executable, *sys.argv)
            except:
                restart_attempted = True
                # If it fails, inform the user to do it manually

            
