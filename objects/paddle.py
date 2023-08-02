import pygame
from pygame.locals import *

from utils.position import Position
from utils.renderutils import resource_path

class Paddle():
    def __init__(self, screen, orientation, starting_pos, image, paddle_id):

        self.screen = screen
        self.orientation = orientation
        #self.colour = colour

        self.paddle_id = paddle_id

        self.speed = 12
        self.speed_mod = 1 # speed modifier
        self.ai_speed = 10 #4
        self.ai_paddle = False

        self.image = image
        self.sprite = pygame.image.load(resource_path(f'image/{image}.png'))
        self.terminator_sprites = False

        if self.orientation == 0: # Rotate sprite if necessary and position the paddle
            self.sprite = pygame.transform.rotate(self.sprite, 90)
            self.paddle_rect = Position(190, 20)
            self.paddle_pos = Position(*starting_pos)
        else:
            self.paddle_rect = Position(20, 190)
            self.paddle_pos = Position(*starting_pos)

    def move_positive(self, shift = False, distance = None):

        if shift:
            temp_mod = 0.3 # Holding shift causes paddles to move slower
        else:
            temp_mod = 1

        if self.orientation == 0: # If this paddle is horizontal
            if distance: # If a specific distance has been requested, use that 
                self.paddle_pos.x += distance
            elif self.ai_paddle: # AI paddle have different movement speed
                self.paddle_pos.x += self.ai_speed * self.speed_mod * temp_mod
            else:
                self.paddle_pos.x += self.speed * self.speed_mod * temp_mod
        else: # If this paddle is vertical
            if distance: 
                self.paddle_pos.y -= distance
            elif self.ai_paddle: 
                self.paddle_pos.y -= self.ai_speed * self.speed_mod * temp_mod
            else:
                self.paddle_pos.y -= self.speed * self.speed_mod * temp_mod

        self.limit_pos()

    def move_negative(self, shift = False, distance = None):
        """ Move the paddle in the negative coordinate direction """

        if shift:
            temp_mod = 0.3 # Holding shift causes paddles to move slower
        else:
            temp_mod = 1

        if self.orientation == 0: # If this paddle is horizontal
            if distance:
                self.paddle_pos.x -= distance
            elif self.ai_paddle:
                self.paddle_pos.x -= self.ai_speed * self.speed_mod * temp_mod
            else:
                self.paddle_pos.x -= self.speed * self.speed_mod * temp_mod
        else: # If this paddle is vertical
            if distance:
                self.paddle_pos.y += distance
            elif self.ai_paddle:
                self.paddle_pos.y += self.ai_speed * self.speed_mod * temp_mod
            else:
                self.paddle_pos.y += self.speed * self.speed_mod * temp_mod

        self.limit_pos()

    def move_to(self, pos):
        """ Set the paddle position """
        if self.orientation == 0:
            self.paddle_pos.x = pos
        else:
            self.paddle_pos.y = pos

        self.limit_pos()

    def limit_pos(self):
        """ Prevent the paddle's position from going outside of its allowed range """
        if self.orientation == 0:
            if self.paddle_pos.x > 1500:
                self.paddle_pos.x = 1500
            if self.paddle_pos.x < 100:
                self.paddle_pos.x = 100
        else:
            if self.paddle_pos.y > 800:
                self.paddle_pos.y = 800
            if self.paddle_pos.y < 100:
                self.paddle_pos.y = 100

    def render(self):
        #rect = pygame.draw.rect(self.screen, self.colour, pygame.Rect(*self.get_left_top(), self.paddle_rect.x, self.paddle_rect.y))
        #rect = pygame.draw.rect(self.screen, self.colour, pygame.Rect(*self.get_left_top(), self.paddle_rect.x, self.paddle_rect.y))

        self.screen.blit(self.sprite, self.get_left_top())

        # draw bounding points, same as how collisions function calculates them
        """
        pygame.draw.line(self.screen, (255, 255, 255), self.get_left_top(), self.get_left_top())
        rright, rbottom = self.get_left_top()[0] + self.paddle_rect.x, self.get_left_top()[1] + self.paddle_rect.y
        pygame.draw.line(self.screen, (255, 255, 255), (rright, rbottom), (rright, rbottom))
        """
        
    def get_left_top(self):
        """ Return the left and top coordinate of the paddle rectangle """

        return (self.paddle_pos.x - self.paddle_rect.x / 2, self.paddle_pos.y - self.paddle_rect.y / 2)
    
    def swap_sprites(self, activation = False):
        """ Switch between normal and terminator paddle sprite """

        if self.terminator_sprites and activation == False:
            self.sprite = pygame.image.load(resource_path(f'image/{self.image}.png'))
            if self.orientation == 0:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            self.terminator_sprites = False
        elif activation == True:
            self.sprite = pygame.image.load(resource_path(f'image/{self.image}_terminator.png'))
            if self.orientation == 0:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            self.terminator_sprites = True