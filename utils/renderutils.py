import pygame
import math 

from utils.position import Position
from utils.colours import Colours

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    origin = Position(*start_pos)
    target = Position(*end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement/length

    for index in range(0, int(length/dash_length), 2):
        start = origin + (slope *    index    * dash_length) # whore 
        end   = origin + (slope * (index + 1) * dash_length)
        pygame.draw.aaline(surf, color, start.tuple(), end.tuple(), width) # change it to non-aa line to have wdith back

def render_lives_ui(screen, font, player1_lives, player2_lives):
    heart_sprite = pygame.transform.scale(pygame.image.load('image/heart.png'), (50, 50))
    heart_sprite = pygame.transform.rotate(heart_sprite, -30.5)

    screen.blit(heart_sprite, (-5, 20))
    screen.blit(heart_sprite, (1530, 800))

    screen.blit(pygame.transform.rotate(font.render(str(player1_lives), True, Colours.WHITE), -30.5), (18, 45))
    screen.blit(pygame.transform.rotate(font.render(str(player2_lives), True, Colours.WHITE), -30.5), (1553, 825))

def lerp(a, b, c):
    return a+(b-a)*c