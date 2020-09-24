#! python3
# sound_toy.py

import os
import pygame
import random
import sys
from pygame.locals import *

# Set up pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
window_width = 800
window_height = 600
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Sound Toy')
fps = 60

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
background_color = black
text_color = white

# Set up fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds
sounds = []
sound_directory = '.\sounds'
for file in os.listdir(sound_directory):
    sounds.append(file)

def terminate():
    pygame.quit()
    sys.exit()


def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


def render_multi_line(text):
    lines = text.splitlines()
    y = 0
    for line in lines:
        render_text = font.render(line, True, white)
        render_text_rect = render_text.get_rect(center=(window_width / 2, (window_height / 4) + y))
        window_surface.blit(render_text, render_text_rect)
        y += 100


def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, 1, text_color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (int(x), int(y))
    surface.blit(text_obj, text_rect)


def collide_with_ss(ball, ss_list, sound_list):
    for ss in ss_list:
        if ball['rect'].colliderect(ss['rect']):
            ss_list.remove(ss)
            sound = pygame.mixer.Sound('sounds' + '\\' + random.choice(sound_list))
            sound.play()


# Ball
ball = {'rect': pygame.Rect(375, 275, 80, 80), 'dir': 'none'}

# Ball movement
DOWNLEFT = 'downleft'
DOWNRIGHT = 'downright'
UPLEFT = 'upleft'
UPRIGHT = 'upright'
move_choice = [DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT]

# Show the "Start" screen.
start_screen_text = 'Alter y speed with UP / DOWN \n Alter x speed with LEFT / RIGHT \n Press any key to start'
render_multi_line(start_screen_text)
pygame.display.update()
wait_for_player_to_press_key()


while True:
    x_speed = 3
    y_speed = 3

    sound_square_list = []
    max_sound_squares = 30
    sound_square_rate = 50
    sound_square_add = 0


    while True:
        # Check for the QUIT event
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

            if event.type == KEYDOWN:
                if event.key == K_UP and y_speed < 10:
                    y_speed += 1
                if event.key == K_DOWN and y_speed > 1:
                    y_speed -= 1
                if event.key == K_RIGHT and x_speed < 10:
                    x_speed += 1
                if event.key == K_LEFT and x_speed > 1:
                    x_speed -= 1

        # ball_rect movement
        if ball['dir'] == 'none':
            ball['dir'] = random.choice(move_choice)

        if ball['dir'] == UPRIGHT:
            ball['rect'].right += x_speed
            ball['rect'].top -= y_speed
        if ball['dir'] == DOWNRIGHT:
            ball['rect'].right += x_speed
            ball['rect'].top += y_speed
        if ball['dir'] == DOWNLEFT:
            ball['rect'].right -= x_speed
            ball['rect'].top += y_speed
        if ball['dir'] == UPLEFT:
            ball['rect'].left -= x_speed
            ball['rect'].top -= y_speed

        # ball_rect collisions with walls
        # top
        if ball['rect'].top < 0:
            if ball['dir'] == UPLEFT:
                ball['dir'] = DOWNLEFT
            if ball['dir'] == UPRIGHT:
                ball['dir'] = DOWNRIGHT

        # bottom
        if ball['rect'].bottom > window_height:
            if ball['dir'] == DOWNLEFT:
                ball['dir'] = UPLEFT
            if ball['dir'] == DOWNRIGHT:
                ball['dir'] = UPRIGHT

        # left
        if ball['rect'].left < 0:
            if ball['dir'] == DOWNLEFT:
                ball['dir'] = DOWNRIGHT
            if ball['dir'] == UPLEFT:
                ball['dir'] = UPRIGHT

        # right
        if ball['rect'].right > window_width:
            if ball['dir'] == DOWNRIGHT:
                ball['dir'] = DOWNLEFT
            if ball['dir'] == UPRIGHT:
                ball['dir'] = UPLEFT

        sound_square_add += 1
        if sound_square_add == sound_square_rate and len(sound_square_list) < max_sound_squares:
            sound_square_add = 0
            ss_size = 30
            sound_square = {'rect': pygame.Rect(random.randint(0, window_width - ss_size),
                                                random.randint(0, window_height - ss_size),
                                                ss_size, ss_size), 'color': red}
            sound_square_list.append(sound_square)

        # Check for collision
        collide_with_ss(ball, sound_square_list, sounds)
        
        # Draw black background onto the window surface
        window_surface.fill(black)

        # Draw player onto the surface
        pygame.draw.rect(window_surface, white, ball['rect'])

        # Draw Sound Squares
        for ss in sound_square_list:
            pygame.draw.rect(window_surface, red, ss['rect'])

        pygame.display.update()
        main_clock.tick(fps)




