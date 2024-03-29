import pygame
import math
import os
import sys

from utils.position import Position
from utils.colours import Colours

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    """ This function draws the diagonal dashed line across the playing field. """
    origin = Position(*start_pos)
    target = Position(*end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement / length

    for index in range(0, int(length / dash_length), 2): # Iterate over requested length drawing short lines
        start = origin + (slope * index * dash_length) 
        end   = origin + (slope * (index + 1) * dash_length)
        pygame.draw.aaline(surf, color, start.tuple(), end.tuple(), width) # change it to non-aa line to have width back

def render_lives_ui(screen, font, player1_lives, player2_lives):
    """ This function renders the lives display in the game window. The UI element consists of a heart graphic, rotated to align with the diagonal centerline,
        and the number of lives rendered on top of the heart graphic, also rotated. """
    heart_sprite = pygame.transform.scale(pygame.image.load(resource_path('image/heart.png')), (50, 50))
    heart_sprite = pygame.transform.rotate(heart_sprite, -30.5)

    screen.blit(heart_sprite, (-5, 20))
    screen.blit(heart_sprite, (1530, 800))

    screen.blit(pygame.transform.rotate(font.render(str(player1_lives), True, Colours.WHITE), -30.5), (18, 45))
    screen.blit(pygame.transform.rotate(font.render(str(player2_lives), True, Colours.WHITE), -30.5), (1553, 825))

def lerp(a, b, c):
    """ Linear interpolation enables smooth movement of an object between two points a and b at speed c. It's used for AI's paddles.
        The return value of this function is the number of pixels the AI paddle should move in that frame """
    return a+(b-a)*c

def format_timedelta(duration):
    """ Convert a datetime.timedelta to human readable hours, minutes, and seconds """
    seconds = duration.total_seconds()
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s" # Don't show 0 hours 

def check_exe():
    """ Returns true if the script is running as an executable """

    try:
        base_path = sys._MEIPASS
        return True
    except Exception:
        return False

def resource_path(relative_path):
    """ Helper to get filepaths to game assets """
    try:
        base_path = sys._MEIPASS # Get the temporary assets folder created by the PyInstaller executable 
    except Exception:
        base_path = os.path.abspath(".") # Not running as compiled, search files normally

    return os.path.join(base_path, relative_path)