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

pygame.init()

BACKGROUND = (74, 74, 74)

FPS = 144
clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Gorilla Pong")

looping = True
while looping:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    WINDOW.fill(BACKGROUND)
    pygame.display.update()
    clock.tick(FPS)
