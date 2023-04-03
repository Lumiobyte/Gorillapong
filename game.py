# Double Pong
# The ball is got gorilla
# When gorilla collect banana, player's paddle can get bigger
# Gorilla ball will change colour depending on whose bounce it is 

#pineapple: ball speed faster
#spinach: bigger paddle for some time
#dragonfruit: shoot flame for a strong bounce
#cherry: creates clone of the ball and enemy has to bounce both balls, clone will disappear after some time
#apple: creates apple pillars which ball bounces of
#carrot: choose the direction to shoot
#banana: harder to control paddles for opponent 
#mango: switches the keys for the paddles
#pringles: pringles can spawns where it is picked up
#sushi: makes ball wrapped in seaweed - big rectangle
#popcorn: drops exploding popping popcorn bomb, and if it blows up next to monkey ball, it gets shot off in a direction away from the explosion
#pickle: puts the monkey in a jar, shatters when it hits the next paddle, stuns the paddle for a while
#paint: paint leaves a trail from the ball..
#coffee bean: paddles move faster
#cocoa: everything slow down
#starfruit: shoots out 5 stars in each direction, each star will become a different power up after some time. :thumbsup:
#water: big water bottle that creats a big pool water, and when ball in the water it gets slower. 
#fanta: its orange water that makes the ball goes FASTER............../...
#milk: it spawns a herd of cows that opponent will play breakout with
#adidas: spawn a tick
#celery: spinning paddle celery paddle that spin around 

#score: score
# lives: 3 lives for the plaaaaaaaaaaayr

#score gained from hitting power ups.....
#

import pygame
from pygame.locals import *
import sys
from dataclasses import dataclass
import random

from utils.colours import Colours
from utils import renderutils

pygame.init()
BACKGROUND = (28, 28, 28)
FPS = 147
clock = pygame.time.Clock()

#WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
pygame.display.set_caption("Gorilla Pong")

#####
screens = []

import menus.main_menu as main_menu
screens.append(main_menu.MainMenu(WINDOW, "Gorillapong"))
screens.append(main_menu.MainMenu(WINDOW, "Settings"))

active_screen = 0
render_queue = []
font = pygame.font.SysFont(None, 32)
score_font = pygame.font.SysFont(None, 128)

#####
from objects import paddle, balls

@dataclass
class Player:
    paddle_horizontal: paddle.Paddle
    paddle_vertical: paddle.Paddle
    score: int

player1 = Player(paddle.Paddle(WINDOW, 0, (300, 860), Colours.PLAYER_GREEN), paddle.Paddle(WINDOW, 1, (40, 300), Colours.PLAYER_GREEN), 0)
player2 = Player(paddle.Paddle(WINDOW, 0, (1300, 40), Colours.PLAYER_RED), paddle.Paddle(WINDOW, 1, (1560, 300), Colours.PLAYER_RED), 0)

active_balls = [balls.Ball(WINDOW, 15, 5, 0.5, Colours.BALL)]
player_last_hit = None
bounces = 0
next_powerup_bounces = 6
#####
from objects import powerups

spawned_powerups = []
spawned_powerups.append(powerups.Pineapple(WINDOW))

#####

import math

def collision(rleft, rtop, width, height,   # rectangle definition
              center_x, center_y, radius):  # circle definition
    """ Detect collision between a rectangle and circle. """

    # complete boundbox of the rectangle
    rright, rbottom = rleft + width, rtop + height

    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected

def reset_ball():
    global active_balls # absolute python 2023 

    active_balls = [balls.Ball(WINDOW, 15, 2, 0.1, Colours.BALL)]
    rand = random.randint(0, 3)
    if rand == 1:
        active_balls[0].reverse_velocity_x()
    elif rand == 2:
        active_balls[0].reverse_velocity_y()
    elif rand == 3:
        active_balls[0].reverse_velocity_x()
        active_balls[0].reverse_velocity_y()

looping = True
while looping:
    if active_screen != 3:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                pass

            if event.type == MOUSEBUTTONDOWN:
                result = screens[active_screen].process_click(event.pos)
                if result != None:
                    active_screen = result

        if event.type == QUIT or active_screen == -1:
            pygame.quit()
            sys.exit()
        else:
            if active_screen != 3:
                WINDOW.fill(BACKGROUND)
                screens[active_screen].render()
    else:
        ##################################################
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    reset_ball()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #### Input

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            player1.paddle_vertical.move_positive()
        if keys[K_s]:
            player1.paddle_vertical.move_negative()
        if keys[K_a]:
            player1.paddle_horizontal.move_negative()
        if keys[K_d]:
            player1.paddle_horizontal.move_positive()
        
        if keys[K_UP]:
            player2.paddle_vertical.move_positive()
        if keys[K_DOWN]:
            player2.paddle_vertical.move_negative()
        if keys[K_RIGHT]:
            player2.paddle_horizontal.move_positive()
        if keys[K_LEFT]:
            player2.paddle_horizontal.move_negative()

        render_queue += [player1.paddle_vertical, player1.paddle_horizontal, player2.paddle_vertical, player2.paddle_horizontal]

        #### Game loop logic 
        
        out_of_bounds = False # Need to make it per ball, so just one can be popped when it goes out of bounds and not all reset 
        scoring_player = None
        for ball in active_balls:
            ball.tick()

            if ball.position.x < -100 or ball.position.y > 1000:
                out_of_bounds = True
                scoring_player = player2
            elif ball.position.x > 1700 or ball.position.y < -100:
                out_of_bounds = True
                scoring_player = player1


            render_queue.append(ball)

            paddle_collisions = [False, False, False, False]

            if ball.position.x < (200 + ball.radius):
                paddle_collisions[0] = collision(*player1.paddle_vertical.get_left_top(), *player1.paddle_vertical.paddle_rect.tuple(), *ball.position.tuple(), ball.radius)
            if ball.position.x > (1400 - ball.radius):
                paddle_collisions[2] = collision(*player2.paddle_vertical.get_left_top(), *player2.paddle_vertical.paddle_rect.tuple(), *ball.position.tuple(), ball.radius)       
            if ball.position.y < (200 + ball.radius):
                paddle_collisions[1] = collision(*player2.paddle_horizontal.get_left_top(), *player2.paddle_horizontal.paddle_rect.tuple(), *ball.position.tuple(), ball.radius)
            if ball.position.y > (600 - ball.radius):
                paddle_collisions[3] = collision(*player1.paddle_horizontal.get_left_top(), *player1.paddle_horizontal.paddle_rect.tuple(), *ball.position.tuple(), ball.radius)

            if paddle_collisions[0]:
                ball.reverse_velocity_x(player1.paddle_vertical.paddle_pos)
                player_last_hit = player1
                bounces += 1
            elif paddle_collisions[1]:
                ball.reverse_velocity_y(player2.paddle_horizontal.paddle_pos)
                player_last_hit = player2
                bounces += 1
            elif paddle_collisions[2]:
                ball.reverse_velocity_x(player2.paddle_vertical.paddle_pos)
                player_last_hit = player2
                bounces += 1
            elif paddle_collisions[3]:
                ball.reverse_velocity_y(player1.paddle_horizontal.paddle_pos)
                player_last_hit = player1
                bounces += 1

            #### Powerup collisions
            for powerup in spawned_powerups:
                if collision(*powerup.position.tuple(), powerup.col_rect.width, powerup.col_rect.height, *ball.position.tuple(), ball.radius):
                    powerup.collect(bounces)

        #### Powerup processing
        delete_queue = []
        for index, powerup in enumerate(spawned_powerups):

            if powerup.collected:
                if not powerup.effected:
                    if type(powerup) == powerups.Pineapple:
                        #print("yellow")
                        for ball in active_balls:
                            ball.speed = ball.speed + powerup.speed_increase
                        
                    powerup.effected = True
                else:
                    if powerup.expires_at > 0 and powerup.expires_at <= bounces:
                        if type(powerup) == powerups.Pineapple:
                            for ball in active_balls:
                                ball.speed = ball.speed - powerup.speed_increase

                        delete_queue.append(index)
                        
            for index in delete_queue:
                spawned_powerups.pop(index)

        #### Powerup spawning
        if bounces >= next_powerup_bounces:
            
            spawned_powerups.append(powerups.Pineapple(WINDOW)) # make a function that gets a powerup and returns it so it can be appended

            next_powerup_bounces += random.randrange(9, 21)

        #### Respawn check
        if out_of_bounds:
            reset_ball()
            if(player_last_hit):
                scoring_player.score += 1
                player_last_hit = None

        ######## Graphics code ########

        WINDOW.fill(BACKGROUND)

        renderutils.draw_dashed_line(WINDOW, Colours.LIGHT_GREY, (0, 0), (1600, 900), 5, 20)

        score_text_1 = pygame.transform.rotate(score_font.render(str(player1.score), True, Colours.SCORE_GREY), -29)
        score_text_2 = pygame.transform.rotate(score_font.render(str(player2.score), True, Colours.SCORE_GREY), -32)
        score_text_2_rect = score_text_2.get_rect()
        score_text_2_rect.bottomright = (1585, 865)

        WINDOW.blit(score_text_1, (15, 40))
        WINDOW.blit(score_text_2, score_text_2_rect)

        render_queue += spawned_powerups
        for item in render_queue:
            item.render()

        render_queue = []

        WINDOW.blit(font.render("FPS: {}".format(round(clock.get_fps(), 1)), True, Colours.GREY), (5, 875))
        WINDOW.blit(font.render(str(active_balls[0].velocity.tuple()), True, Colours.GREY), (150, 875))
        WINDOW.blit(font.render(str(bounces), True, Colours.GREY), (600, 875))
        WINDOW.blit(font.render(str(active_balls[0].speed), True, Colours.GREY), (550, 875))

        # will need to do some things with last frame time, passing it into the movement funcs, so movement is smooth 
        

    pygame.display.update()
    clock.tick(FPS)