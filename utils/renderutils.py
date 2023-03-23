import pygame
import math 

from utils.position import Position

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    origin = Position(*start_pos)
    target = Position(*end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement/length

    for index in range(0, int(length/dash_length), 2):
        start = origin + (slope *    index    * dash_length)
        end   = origin + (slope * (index + 1) * dash_length)
        pygame.draw.line(surf, color, start.tuple(), end.tuple(), width)