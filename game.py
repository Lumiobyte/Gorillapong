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

from utils.colours import Colours

pygame.init()
BACKGROUND = (74, 74, 74)
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

#####
from objects import paddle

@dataclass
class Player:
    paddle_horizontal: paddle.Paddle
    paddle_vertical: paddle.Paddle

player1 = Player(paddle.Paddle(WINDOW, 0, [300, 840]), paddle.Paddle(WINDOW, 1, [40, 300]))
player2 = Player(paddle.Paddle(WINDOW, 0, [1300, 840]), paddle.Paddle(WINDOW, 1, [1540, 300]))

#####

looping = True
while looping:
    if active_screen != 3:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                pass

            if event.type == MOUSEBUTTONDOWN:
                result = screens[active_screen].process_click(event.pos)
                print(result)
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
                pass

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

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

        WINDOW.fill(BACKGROUND)

        player1.paddle_vertical.render(Colours.GREEN)
        player1.paddle_horizontal.render(Colours.GREEN)

        player2.paddle_vertical.render(Colours.RED)
        player2.paddle_horizontal.render(Colours.RED)

        # will need to do some things with last frame time, passing it into the movement funcs, so movement is smooth
        

    pygame.display.update()
    clock.tick(FPS)