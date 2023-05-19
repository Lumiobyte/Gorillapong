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
import traceback

from utils.colours import Colours
from utils import renderutils, database

pygame.init()
BACKGROUND = (28, 28, 28)
FPS = 147
clock = pygame.time.Clock()

max_resolution = database.get_max_resolution()

if database.get_resolution() == max_resolution:
    WINDOW = pygame.display.set_mode(max_resolution)
    SCREEN = None
else:
    WINDOW = pygame.Surface(max_resolution)
    SCREEN = pygame.display.set_mode(database.get_resolution())

pygame.display.set_caption("Gorilla Pong")

""" This is unnecessary, since resolution can only be switched on the main menu and doing so forces a game restart.
def switch_resolution(new_res):
    global WINDOW
    global SCREEN

    if new_res == max_resolution:
        WINDOW = pygame.display.set_mode(new_res)
    else:
        WINDOW = pygame.Surface(max_resolution)
        SCREEN = pygame.display.set_mode(new_res)

    database.set_resolution(new_res) # TEMPORARY FOR TESTING.
"""

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
    score = 0
    lives = 3

player1 = Player(paddle.Paddle(WINDOW, 0, (300, 860), Colours.PLAYER_GREEN, 0), paddle.Paddle(WINDOW, 1, (40, 300), Colours.PLAYER_GREEN, 1))
player2 = Player(paddle.Paddle(WINDOW, 0, (1300, 40), Colours.PLAYER_RED, 2), paddle.Paddle(WINDOW, 1, (1560, 300), Colours.PLAYER_RED, 3))

active_balls = [balls.Ball(WINDOW, 15, 5, 0.5, Colours.BALL, 0)]
player_last_hit = None
bounces = 0
next_powerup_bounces = 6
powerup_spawn_counter = 0 # Useful for any powerups that need a unique ID

player_who_died = 0 # hacky way to implement deaths to lives
#####
from objects import powerups

spawned_powerups = []
spawned_powerups.append(powerups.Water(WINDOW))

#####

current_frame_ticks = 0
last_frame_ticks = 0
time_delta = 0

#####

ai = False # Whether the AI is enabled or not
player1_ai = False # Can only be changed manually in the code. Causes blue player to be controlled by AI as well.
aim_randomiser = 1 # Determines where the AI will attempt to land the ball on its paddles. 0 = one corner 1 = middle 2 = other corner
repredict = True # Allow AI to make another prediction as to where the ball will land

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
    global spawned_powerups
    global repredict

    repredict = True

    delete_queue = []
    for powerup in spawned_powerups:
        if powerup.collected:
            delete_queue.append(powerup)

    for obj in delete_queue:
        spawned_powerups.remove(obj)

    active_balls = [balls.Ball(WINDOW, 15, 5, 0.1, Colours.BALL, 0)] # 5
    rand = random.randint(0, 3)
    if rand == 1:
        active_balls[0].reverse_velocity_x()
    elif rand == 2:
        active_balls[0].reverse_velocity_y()
    elif rand == 3:
        active_balls[0].reverse_velocity_x()
        active_balls[0].reverse_velocity_y()

def get_new_powerup(spawn_index = None):
    global bounces
    global powerup_spawn_counter

    if spawn_index:
        spawn_rand = spawn_index
    else:
        spawn_rand = random.randint(1, 4)

    powerup_spawn_counter += 1

    if spawn_rand == 1:
        return powerups.Pineapple(WINDOW)
    elif spawn_rand == 2:
        return powerups.Pickle(WINDOW)
    elif spawn_rand == 3:
        return powerups.Water(WINDOW)
    elif spawn_rand == 4:
        return powerups.Pringle(WINDOW, powerup_spawn_counter)

try: # NEVER DO THIS!!!!!!!!
    looping = True
    while looping:
        if active_screen != 3:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pass

                if event.type == MOUSEBUTTONDOWN:
                    result, ai_toggle = screens[active_screen].process_position(event.pos, True)
                    if result != None:
                        active_screen = result

                        player1.lives = 3
                        player2.lives = 3
                        spawned_powerups = []

                        ai = ai_toggle
                        player2.paddle_horizontal.ai_paddle = ai_toggle
                        player2.paddle_vertical.ai_paddle = ai_toggle
                        repredict = True

            if event.type == QUIT or active_screen == -1:
                pygame.quit()
                sys.exit()
            else:
                if active_screen != 3:
                    screens[active_screen].process_position(pygame.mouse.get_pos())
                    WINDOW.fill(BACKGROUND)
                    screens[active_screen].render()
                    if player_who_died != 0:
                        WINDOW.blit(font.render(f"Player {player_who_died} died!", True, Colours.WHITE), (600, 300))
        else:

            last_frame_ticks = current_frame_ticks
            current_frame_ticks = pygame.time.get_ticks()
            time_delta = (current_frame_ticks - last_frame_ticks) / 4 # quarter it so that the effect on speed is not so extreme

            ##################################################
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        reset_ball()

                    if event.key == K_1:
                        spawned_powerups.append(get_new_powerup(1))
                    elif event.key == K_2:
                        spawned_powerups.append(get_new_powerup(2))
                    elif event.key == K_3:
                        spawned_powerups.append(get_new_powerup(3))
                    elif event.key == K_4:
                        spawned_powerups.append(get_new_powerup(4))

                    if event.key == K_BACKSPACE:
                        active_screen = 0 # Back to main menu
                        #pygame.quit()
                        #sys.exit()

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            #### Death Check - return to menu. This will 100% break if they try to play again without restarting the program

            if player1.lives <= 0:
                player_who_died = 1
                active_screen = 0
            elif player2.lives <= 0:
                player_who_died = 2
                active_screen = 0

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
            
            if ai:
                pass # DO NUFFIN 
            else:
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
            for i, ball in enumerate(active_balls):

                if ai: # Ed Townsend

                    if repredict:
                        impact_pos = ball.future_position(None)

                        # This method will result in the irrelevant paddle still jiggling slightly upon reprediction.
                        # A check that stops aim randomiser from being applied to irrelevant paddles would fix it.
                        if impact_pos.x == -1:
                            impact_pos.x = player2.paddle_horizontal.paddle_pos.x
                        if impact_pos.y == -1:
                            impact_pos.y = player2.paddle_vertical.paddle_pos.y
                        
                        divisor = random.randint(21, 25) / 10 # Add some flavor to corner shots by hitting different parts of the paddle
                        if aim_randomiser == 0:
                            impact_pos.x -= player2.paddle_horizontal.paddle_rect.x / divisor
                            impact_pos.y -= player2.paddle_vertical.paddle_rect.y / divisor
                        elif aim_randomiser == 2:
                            impact_pos.x += player2.paddle_horizontal.paddle_rect.x / divisor
                            impact_pos.y += player2.paddle_vertical.paddle_rect.y / divisor

                        repredict = False

                    new_x = renderutils.lerp(player2.paddle_horizontal.paddle_pos.x, impact_pos.x, 8/FPS)
                    new_y = renderutils.lerp(player2.paddle_vertical.paddle_pos.y, impact_pos.y, 8/FPS)

                    if abs(player2.paddle_horizontal.paddle_pos.x - new_x) > player2.paddle_horizontal.ai_speed:
                        if new_x > player2.paddle_horizontal.paddle_pos.x:
                            new_x = player2.paddle_horizontal.paddle_pos.x + player2.paddle_horizontal.ai_speed
                        else:
                            new_x = player2.paddle_horizontal.paddle_pos.x - player2.paddle_horizontal.ai_speed

                    if abs(player2.paddle_vertical.paddle_pos.y - new_y) > player2.paddle_vertical.ai_speed:
                        if new_y > player2.paddle_vertical.paddle_pos.y:
                            new_y = player2.paddle_vertical.paddle_pos.y + player2.paddle_vertical.ai_speed
                        else:
                            new_y = player2.paddle_vertical.paddle_pos.y - player2.paddle_vertical.ai_speed
                            
                    # Using paddle function allows paddle to manage its movement limits (prevents going off screen)
                    player2.paddle_horizontal.move_to(new_x)
                    player2.paddle_vertical.move_to(new_y)

                # Inaccessible from the game UI, can only be activated by setting the variable in the code
                if player1_ai: # Francis Sinclair
                    divisor = random.randint(21, 25) / 10 # Add some flavor to corner shots by hitting different parts of the paddle
                    if aim_randomiser == 0:
                        impact_x = player1.paddle_horizontal.paddle_pos.x - player1.paddle_horizontal.paddle_rect.x / divisor
                        impact_y = player1.paddle_vertical.paddle_pos.y - player1.paddle_vertical.paddle_rect.y / divisor
                    elif aim_randomiser == 1:
                        impact_x = player1.paddle_horizontal.paddle_pos.x
                        impact_y = player1.paddle_vertical.paddle_pos.y
                    elif aim_randomiser == 2:
                        impact_x = player1.paddle_horizontal.paddle_pos.x + player1.paddle_horizontal.paddle_rect.x / divisor
                        impact_y = player1.paddle_vertical.paddle_pos.y + player1.paddle_vertical.paddle_rect.y / divisor


                    if impact_x > ball.position.x:
                        player1.paddle_horizontal.move_negative()
                    else:
                        player1.paddle_horizontal.move_positive()
                    
                    if impact_y > ball.position.y:
                        player1.paddle_vertical.move_positive()
                    else:
                        player1.paddle_vertical.move_negative()

                ball.tick()

                # For testing
                #ball.position.x = pygame.mouse.get_pos()[0]
                #ball.position.y = pygame.mouse.get_pos()[1]

                if ball.position.x < -100 or ball.position.y > 1000:
                    out_of_bounds = True
                    scoring_player = player2
                elif ball.position.x > 1700 or ball.position.y < -100:
                    out_of_bounds = True
                    scoring_player = player1

                # We add balls to render queue later so that they are not behind powerups e.g. water puddle
                #render_queue.append(ball)

                paddle_collisions = [False, False, False, False]

                if ball.position.x < (200 + ball.radius):
                    paddle_collisions[0] = collision(*player1.paddle_vertical.get_left_top(), *player1.paddle_vertical.paddle_rect.tuple(), *ball.position.tuple(), ball.radius)
                if ball.position.x > (1400 - ball.radius):
                    paddle_collisions[2] = collision(*player2.paddle_vertical.get_left_top(), *player2.paddle_vertical.paddle_rect.tuple(), *ball.position.tuple(), ball.radius)       
                if ball.position.y < (200 + ball.radius):
                    paddle_collisions[1] = collision(*player2.paddle_horizontal.get_left_top(), *player2.paddle_horizontal.paddle_rect.tuple(), *ball.position.tuple(), ball.radius)
                if ball.position.y > (600 - ball.radius):
                    paddle_collisions[3] = collision(*player1.paddle_horizontal.get_left_top(), *player1.paddle_horizontal.paddle_rect.tuple(), *ball.position.tuple(), ball.radius)

                paddle_hit = None

                if paddle_collisions[0]:
                    ball.reverse_velocity_x(player1.paddle_vertical.paddle_pos, player1.paddle_vertical.paddle_id)
                    player_last_hit = player1
                    bounces += 1
                    paddle_hit = player1.paddle_vertical
                    ball.pringle_last_hit = None
                    repredict = True
                elif paddle_collisions[1]:
                    ball.reverse_velocity_y(player2.paddle_horizontal.paddle_pos, player2.paddle_horizontal.paddle_id)
                    player_last_hit = player2
                    bounces += 1
                    paddle_hit = player2.paddle_horizontal
                    ball.pringle_last_hit = None
                    repredict = True
                elif paddle_collisions[2]:
                    ball.reverse_velocity_x(player2.paddle_vertical.paddle_pos, player2.paddle_vertical.paddle_id)
                    player_last_hit = player2
                    bounces += 1
                    paddle_hit = player2.paddle_vertical
                    ball.pringle_last_hit = None
                    repredict = True
                elif paddle_collisions[3]:
                    ball.reverse_velocity_y(player1.paddle_horizontal.paddle_pos, player1.paddle_horizontal.paddle_id)
                    player_last_hit = player1
                    bounces += 1
                    paddle_hit = player1.paddle_horizontal
                    ball.pringle_last_hit = None
                    repredict = True

                if ai:
                    if paddle_hit == player2.paddle_vertical or paddle_hit == player2.paddle_horizontal:
                        # It may be necessary to ensure that one of the human's paddles has been hit before allowing AI to make this choice again
                        aim_randomiser = random.randint(0, 2)

                #### Powerup collisions
                for powerup in spawned_powerups:
                    if collision(*powerup.position.tuple(), powerup.col_rect.width, powerup.col_rect.height, *ball.position.tuple(), ball.radius):
                        if powerup.collected:
                            if type(powerup) == powerups.Water and powerup.effected and not powerup.expired:
                                if not powerup.is_in_puddle(ball.ball_id) and not ball.in_puddle:
                                    if not ball.bounced:
                                        ball.speed = 1
                                        ball.bounced = True
                                        powerup.enter_puddle(ball.ball_id) 
                                    else:
                                        ball.speed = ball.speed + powerup.enter_puddle(ball.ball_id)
                                    ball.in_puddle = True
                                else:
                                    next_position = ball.future_position(1)
                                    if not collision(*powerup.position.tuple(), powerup.col_rect.width, powerup.col_rect.height, *next_position, ball.radius) and ball.in_puddle:
                                        ball.speed = ball.speed + powerup.exit_puddle(ball.ball_id)
                                        ball.in_puddle = False
                            if type(powerup) == powerups.Pringle and powerup.effected and not powerup.expired:
                                if collision(*powerup.position.tuple(), powerup.col_rect.width, powerup.col_rect.height, *ball.position.tuple(), ball.radius):
                                    if ball.pringle_last_hit != powerup.powerup_id:
                                        ball.reverse_velocity_x()
                                        repredict = True
                                        ball.pringle_last_hit = powerup.powerup_id
                        else:
                            powerup.collect(bounces, i)

            #### Powerup processing
            delete_queue = []
            for index, powerup in enumerate(spawned_powerups):

                if powerup.collected and not powerup.expired:
                    if not powerup.effected:
                        if type(powerup) == powerups.Pineapple:
                            #print("yellow")
                            for ball in active_balls:
                                ball.speed = ball.speed + powerup.speed_increase
                        elif type(powerup) == powerups.Pickle:
                                powerup.update_pos(active_balls[i].position)

                                """
                                if player_last_hit: # prevent crashes when nobody has hit before the powerup was collected
                                    player_last_hit.lives -= 1 # since powerups are not working as intended, just take off a life for hitting a pickle at all
                                """
                        elif type(powerup) == powerups.Water:
                            pass
                        elif type(powerup) == powerups.Pringle:
                            pass

                        powerup.effected = True
                    else:
                        if powerup.expires_at > 0 and powerup.expires_at <= bounces:
                            #print(f"{powerup} is ready to expire.")
                            if type(powerup) == powerups.Pineapple:
                                for ball in active_balls:
                                    ball.speed = ball.speed - powerup.speed_increase
                            elif type(powerup) == powerups.Pickle:
                                player_last_hit.lives -= 1
                            elif type(powerup) == powerups.Water:
                                pass
                            elif type(powerup) == powerups.Pringle:
                                pass

                            powerup.expired = True
                            # don't use this way 
                            #delete_queue.append(powerup)

                        else:
                            if type(powerup) == powerups.Pickle:
                                powerup.update_pos(active_balls[i].position)

                # Crashes randomly
                """
                for obj in delete_queue:
                    spawned_powerups.remove(obj)
                """

            #### Powerup spawning
            if bounces >= next_powerup_bounces:
                
                spawned_powerups.append(get_new_powerup())

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
            render_queue += active_balls
            for item in render_queue:
                item.render()

            render_queue = []

            WINDOW.blit(font.render("FPS: {} / {}".format(round(clock.get_fps(), 1), time_delta), True, Colours.GREY), (5, 875))
            WINDOW.blit(font.render(f"V: ({round(active_balls[0].velocity.x, 5)}, {round(active_balls[0].velocity.y, 5)})", True, Colours.GREY), (180, 875))
            WINDOW.blit(font.render(str(bounces), True, Colours.GREY), (600, 875))
            WINDOW.blit(font.render(str(active_balls[0].speed), True, Colours.GREY), (550, 875))
            WINDOW.blit(font.render(f"NEXT P: {next_powerup_bounces - bounces}", True, Colours.GREY), (710, 875))
            if ai:
                WINDOW.blit(font.render(f"AIM: {aim_randomiser}", True, Colours.GREY), (850, 875))

            WINDOW.blit(font.render("Blue Lives: " + str(player1.lives), True, Colours.GREY), (1000, 850))
            WINDOW.blit(font.render("Orange Lives: " + str(player2.lives), True, Colours.GREY), (970, 875))
            

        if database.get_resolution() != max_resolution:
            WINDOW_downscaled = pygame.transform.scale(WINDOW, database.get_resolution())
            SCREEN.blit(WINDOW_downscaled, (0, 0))
        else:
            # Shouldn't need to do anything here if the resolution switching method works out 
            #SCREEN.blit(WINDOW, (0, 0))
            pass

        pygame.display.update()
        clock.tick(FPS)

except Exception as e: # worst error handling method 

    print(traceback.print_exc())

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.blit(font.render("FATAL ERROR", True, Colours.PLAYER_RED), (600, 300))
        WINDOW.blit(font.render(str(e), True, Colours.WHITE), (600, 350))
        WINDOW.blit(font.render("Press escape to exit the game", True, Colours.GREY), (600, 500))

        pygame.display.update()
        clock.tick(FPS)
