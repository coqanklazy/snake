import pygame
import sys
import random
from collections import deque

import draw_map
import AI_method

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1200, 800
WIDTH_SCALE = 680
HEIGHT_SCALE = 680
MAP_WIDTH = 30
MAP_HEIGHT = 30
GRID_SIZE = 20
GRID_WIDTH = WIDTH_SCALE  // GRID_SIZE
GRID_HEIGHT = HEIGHT_SCALE  // GRID_SIZE
SNAKE_SPEED = 5
NUM_OF_OBSTACLES = 10

SETTING_WIDTH = 350
SETTING_HEIGHT = 180

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
GOLD = 	(255, 215, 0)
RED = (140, 7, 7)
GREY = (130, 127, 128)
PINK = (240, 101, 149)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Font
font24 = pygame.font.Font('image/impact.ttf', 24)
font28 = pygame.font.Font('image/impact.ttf', 28)
font64 = pygame.font.Font(None, 64)
font36 = pygame.font.Font('image/impact.ttf', 36)
font120 = pygame.font.Font('image/04B_19.TTF', 120)
font100 = pygame.font.Font('image/MarkerFelt.ttf', 100)

# Load sound
eat_sound = pygame.mixer.Sound('audio/eat.mp3')
dead_sound = pygame.mixer.Sound('audio/dead1.mp3')
button_sound = pygame.mixer.Sound('audio/button.mp3')
count_sound = pygame.mixer.Sound('audio/count.mp3')

# Load images
head1 = pygame.image.load('image/head1.png').convert()
head1 = pygame.transform.scale(head1, (20, 20))
body1 = pygame.image.load('image/body1.png').convert()
body1 = pygame.transform.scale(body1, (20, 20))

head2 = pygame.image.load('image/head2.png').convert()
head2 = pygame.transform.scale(head2, (20, 20))
body2 = pygame.image.load('image/body2.png').convert()
body2 = pygame.transform.scale(body2, (20, 20))

food = pygame.image.load('image/food.png').convert_alpha()
food = pygame.transform.scale(food, (20, 20))

background = pygame.image.load('image/background.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

ground = pygame.image.load('image/ground.png').convert()
ground = pygame.transform.scale(ground, (WIDTH, 150))

snake_image = pygame.image.load('image/snake.png').convert_alpha()
snake_image = pygame.transform.scale(snake_image, (650, 400))

obstacles = pygame.image.load('image/BOM.png').convert_alpha()
obstacles = pygame.transform.scale(obstacles, (20, 20))

music_on_image = pygame.image.load('image/music_on.png').convert_alpha()
music_on_image = pygame.transform.scale(music_on_image, (140, 140))

music_off_image = pygame.image.load('image/music_off.png').convert_alpha()
music_off_image = pygame.transform.scale(music_off_image, (140, 140))

# Menu
mode_button_rect = pygame.Rect(500, 300, 200, 60)
quit_button_rect = pygame.Rect(500, 500, 200, 60)
setting_button_menu_rect = pygame.Rect(500, 400, 200, 60)

# Mode
one_player_button_rect = pygame.Rect(350, 300, 200, 60)
pvp_button_rect = pygame.Rect(650, 300, 200, 60)
AI_button_rect = pygame.Rect(350, 400, 200, 60)
pve_button_rect = pygame.Rect(650, 400, 200, 60)
bfs_button_rect = pygame.Rect(350, 300, 200, 60)
dfs_button_rect = pygame.Rect(350, 380, 200, 60)
ID_button_rect = pygame.Rect(350, 460, 200, 60)
ucs_button_rect = pygame.Rect(650, 300, 200, 60)
AStar_button_rect = pygame.Rect(650, 380, 200, 60)
greedy_button_rect = pygame.Rect(650, 460, 200, 60)

# Playing
pause_button_rect = pygame.Rect(850, 200, 200, 60)
pause = False

color_active = RED
color_inactive = BLACK

# Setting speed
speed_rect = pygame.Rect(710, 270, 60, 50)

speed_color = color_inactive
speed_active = False
speed_text = str(SNAKE_SPEED)

# Setting map size
width_rect = pygame.Rect(670, 350, 60, 50)
height_rect = pygame.Rect(770, 350, 60, 50)

width_color = color_inactive
width_active = False
height_color = color_inactive
height_active = False
width_text = str(MAP_WIDTH)
height_text = str(MAP_HEIGHT)

# Setting number of obstacles
obstacles_rect = pygame.Rect(710, 430, 60, 50)

obstacles_color = color_inactive
obstacles_active = False
obstacles_text = str(NUM_OF_OBSTACLES)

return_button_rect = pygame.Rect(500, 600, 200, 60)

# Pasue
resume_button_pause_rect = pygame.Rect(80, 280, 200, 60)
retry_button_pause_rect = pygame.Rect(80, 430, 200, 60)
menu_button_pause_rect = pygame.Rect(480, 280, 200, 60)
quit_button_pause_rect = pygame.Rect(480, 430, 200, 60)
music_playing_rect = pygame.Rect(890, 180, 140, 140)

# Game Over
retry_button_game_over_rect = pygame.Rect(750, 240, 200, 60)
menu_button_game_over_rect = pygame.Rect(970, 240, 200, 60)

def move_snake(snake, snake_direction):
    return (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

# Create obstacles func
def create_obstacles():
    obstacles_list = []
    for i in range(0, NUM_OF_OBSTACLES):
        obstacle_coords = (random.randint(4, GRID_WIDTH - 1), random.randint(4, GRID_HEIGHT - 1))
        obstacles_list.append(obstacle_coords)
    return obstacles_list

# Create food func
def generate_food_location(snake, obstacles_list):
    while True:
        food_x = random.randint(4, GRID_WIDTH - 1)
        food_y = random.randint(4, GRID_HEIGHT - 1)
        for _ in obstacles_list:
            if (food_x, food_y) not in obstacles_list and (food_x, food_y) not in snake:
                return (food_x, food_y)

# Write text
def display_text(text, x, y, color, font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Create button
def create_button (x, y):
    button = pygame.image.load('image/button.png').convert_alpha()
    button = pygame.transform.scale(button, (x, y))
    return button

# Music
music_playing = True

def music_play():
    pygame.mixer.music.load('audio/soundtrack_playing.mp3')
    pygame.mixer.music.play(-1)
def music_stop():
    pygame.mixer.music.stop()

def music_pause():
    pygame.mixer.music.pause()

def music_unpause():
    pygame.mixer.music.unpause()

def set_volume(x):
    pygame.mixer.music.set_volume(x)
    eat_sound.set_volume(x)
    dead_sound.set_volume(x)
    button_sound.set_volume(x)
    count_sound.set_volume(x)

def button_sound_play(x):
    button_sound.play()
    pygame.time.wait(x)

def show_time(time):
    minute = int(time) // 60
    second = int(time) % 60
    if minute == 0:
        display_text(f"Time: {second}s", WIDTH_SCALE-GRID_SIZE*2, HEIGHT_SCALE+40, WHITE, font36)
    else:
        display_text(f"Time: {minute}m{second}s", WIDTH_SCALE-GRID_SIZE*2, HEIGHT_SCALE+40, WHITE, font36)

game_state2 = "menu"
high_score = 0

def init_game():
    global snake1, snake1_direction, snake2, snake2_direction, food_coords, game_state, score1, score2, time, obstacles_list, resume_countdown
    snake1 = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake2 = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake1_direction = RIGHT
    snake2_direction = LEFT
    food_coords = (random.randint(4, GRID_WIDTH - 1), random.randint(4, GRID_HEIGHT - 1))
    game_state = "menu"
    score1 = 0
    score2 = 0
    time = 0
    obstacles_list = create_obstacles()
    resume_countdown = 3

# KEYDOWN
def handle_key_events(key):
    global game_state, snake1_direction, snake2_direction, SNAKE_SPEED, \
        speed_color, speed_active, speed_text, \
        width_color, width_active, width_text, \
        height_color, height_active, height_text, \
        obstacles_color, obstacles_active, obstacles_text, \
        MAP_WIDTH, MAP_HEIGHT, NUM_OF_OBSTACLES, pause, \
        GRID_WIDTH, GRID_HEIGHT, WIDTH_SCALE, HEIGHT_SCALE

    if game_state == "1player" or game_state == "bfs_pve":
        if key == pygame.K_UP or key == pygame.K_w:
            if snake1_direction != DOWN:
                snake1_direction = UP
        elif key == pygame.K_DOWN or key == pygame.K_s:
            if snake1_direction != UP:
                snake1_direction = DOWN
        elif key == pygame.K_LEFT or key == pygame.K_a:
            if snake1_direction != RIGHT:
                snake1_direction = LEFT
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            if snake1_direction != LEFT:
                snake1_direction = RIGHT
        elif key == pygame.K_ESCAPE:
            music_pause()
            game_state = "pause"

    if game_state == "pvp":
        if key == pygame.K_UP:
            if snake1_direction != DOWN:
                snake1_direction = UP
        elif key == pygame.K_DOWN:
            if snake1_direction != UP:
                snake1_direction = DOWN
        elif key == pygame.K_LEFT:
            if snake1_direction != RIGHT:
                snake1_direction = LEFT
        elif key == pygame.K_RIGHT:
            if snake1_direction != LEFT:
                snake1_direction = RIGHT

        if key == pygame.K_w:
            if snake2_direction != DOWN:
                snake2_direction = UP
        elif key == pygame.K_s:
            if snake2_direction != UP:
                snake2_direction = DOWN
        elif key == pygame.K_a:
            if snake2_direction != RIGHT:
                snake2_direction = LEFT
        elif key == pygame.K_d:
            if snake2_direction != LEFT:
                snake2_direction = RIGHT

        elif key == pygame.K_ESCAPE:
            music_pause()
            game_state = "pause"

    if game_state == "setting":
        # Choose Speed
        if speed_active:
            if event.key == pygame.K_RETURN:
                try:
                    speed = int(speed_text)
                    if speed >= 5 and speed <= 30:
                        SNAKE_SPEED = speed
                        speed_color = color_inactive
                except ValueError:
                    pass
                    speed_text = str(SNAKE_SPEED)
            elif event.key == pygame.K_BACKSPACE:
                speed_text = speed_text[:-1]
            else:
                speed_text += event.unicode

        # Choose Map Size - WIDTH
        elif width_active:
            if event.key == pygame.K_RETURN:
                try:
                    width = int(width_text)
                    if width > 10 and width <= 30:
                        MAP_WIDTH = width
                        GRID_WIDTH = width + 4
                        WIDTH_SCALE = GRID_WIDTH*GRID_SIZE
                        width_color = color_inactive
                except ValueError:
                    pass
                    width_text = str(MAP_WIDTH)
            elif event.key == pygame.K_BACKSPACE:
                width_text = width_text[:-1]
            else:
                width_text += event.unicode

        # Choose Map Size - WIDTH
        elif height_active:
            if event.key == pygame.K_RETURN:
                try:
                    height = int(height_text)
                    if height > 10 and height <= 30:
                        MAP_HEIGHT = height
                        GRID_HEIGHT = height + 4
                        HEIGHT_SCALE = GRID_HEIGHT*GRID_SIZE
                        height_color = color_inactive
                except ValueError:
                    pass
                    height_text = str(MAP_HEIGHT)
            elif event.key == pygame.K_BACKSPACE:
                height_text = height_text[:-1]
            else:
                height_text += event.unicode

        # Choose Number Of Obstacles
        elif obstacles_active:
            if event.key == pygame.K_RETURN:
                try:
                    num_of_obstacles = int(obstacles_text)
                    if num_of_obstacles >= 5 and num_of_obstacles <= 30:
                        NUM_OF_OBSTACLES = num_of_obstacles
                        obstacles_color = color_inactive
                except ValueError:
                    pass
                    obstacles_text = str(NUM_OF_OBSTACLES)
            elif event.key == pygame.K_BACKSPACE:
                obstacles_text = obstacles_text[:-1]
            else:
                obstacles_text += event.unicode

# MOUSEBUTTONDOWN
def handle_mouse_click(event):
    global game_state, game_state2, music_playing, music_playing_rect, \
        speed_color, speed_active, speed_text, \
        width_color, width_active, width_text, \
        height_color, height_active, height_text, \
        obstacles_color, obstacles_active, obstacles_text

    if game_state == "menu":
        if mode_button_rect.collidepoint(event.pos):
            button_sound_play(700)
            game_state = "mode"
        elif setting_button_menu_rect.collidepoint(event.pos):
            button_sound_play(500)
            game_state = "setting"
        elif quit_button_rect.collidepoint(event.pos):
            button_sound_play(500)
            pygame.quit()
            sys.exit()

    elif game_state == "mode":
        if one_player_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "1player"
            music_play()
        elif pvp_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "pvp"
            music_play()
        elif AI_button_rect.collidepoint(event.pos):
            button_sound_play(700)
            game_state = "AI"
        elif pve_button_rect.collidepoint(event.pos):
            button_sound_play(700)
            game_state = "pve"
        elif return_button_rect.collidepoint(event.pos):
            button_sound_play(700)
            game_state = "menu"

    elif game_state == "AI":
        if bfs_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "bfs_AI"
            music_play()
        elif ucs_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "ucs_AI"
            music_play()
        elif dfs_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "dfs_AI"
            music_play()
        elif ID_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "ID_AI"
            music_play()

        elif greedy_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "greedy_AI"
            music_play()
        elif return_button_rect.collidepoint(event.pos):
            button_sound_play(700)
            game_state = "mode"

    elif game_state == "pve":
        if bfs_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "bfs_pve"
            music_play()
        elif dfs_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "dfs_pve"
            music_play()
        elif ID_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "ID_pve"
            music_play()
        elif ucs_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "ucs_pve"
            music_play()
        elif greedy_button_rect.collidepoint(event.pos):
            button_sound_play(1000)
            game_state = game_state2 = "greedy_pve"
            music_play()
        elif return_button_rect.collidepoint(event.pos):
            button_sound_play(700)
            game_state = "mode"

    elif game_state == "game_over1":
        if retry_button_game_over_rect.collidepoint(event.pos):
            dead_sound.stop()
            button_sound_play(500)
            music_play()
            init_game()
            game_state = game_state2
        elif menu_button_game_over_rect.collidepoint(event.pos):
            button_sound_play(500)
            init_game()

    elif game_state == "game_over2":
        if retry_button_game_over_rect.collidepoint(event.pos):
            dead_sound.stop()
            button_sound_play(500)
            music_play()
            init_game()
            game_state = game_state2
        elif menu_button_game_over_rect.collidepoint(event.pos):
            button_sound_play(500)
            init_game()

    elif (
        game_state == "1player"
        or game_state == "pvp"
        or game_state == "bfs_AI"
        or game_state == "dfs_AI"
        or game_state == "ID_AI"
        or game_state == "ucs_AI"
        or game_state == "greedy_AI"
    ):
        if pause_button_rect.collidepoint(event.pos):
            music_pause()
            button_sound_play(500)
            game_state = "pause"

    elif game_state == "pause":
        if resume_button_pause_rect.collidepoint(event.pos):
            button_sound_play(700)
            game_state = "resume"
        elif retry_button_pause_rect.collidepoint(event.pos):
            music_stop()
            button_sound_play(500)
            music_play()
            init_game()
            game_state = game_state2
        elif menu_button_pause_rect.collidepoint(event.pos):
            button_sound_play(500)
            init_game()
        elif quit_button_pause_rect.collidepoint(event.pos):
            button_sound_play(500)
            pygame.quit()
            sys.exit()
        elif music_playing_rect.collidepoint(event.pos):
            if music_playing:
                set_volume(0)
            else:
                set_volume(1)
            music_playing = not music_playing

    elif game_state == "setting":
        # Choose Speed
        if speed_rect.collidepoint(event.pos):
            speed_active = not speed_active
        else:
            speed_active = False
        speed_color = color_active if speed_active else color_inactive

        # Choose Map Size -WIDTH
        if width_rect.collidepoint(event.pos):
            width_active = not width_active
        else:
            width_active = False
        width_color = color_active if width_active else color_inactive

        # Choose Map Size -HEIGHT
        if height_rect.collidepoint(event.pos):
            height_active = not height_active
        else:
            height_active = False
        height_color = color_active if height_active else color_inactive

        # Choose Number Of Obstacles
        if obstacles_rect.collidepoint(event.pos):
            obstacles_active = not obstacles_active
        else:
            obstacles_active = False
        obstacles_color = color_active if obstacles_active else color_inactive

        if return_button_rect.collidepoint(event.pos):
            button_sound_play(500)
            game_state = "menu"

def menu_logic():
    global game_state, time, score1, score2, map, snake

    music_stop()
    screen.blit(background, (0, 0))
    display_text("SNAKE GAME", 600, 200, RED, font120)
    draw_map.draw(MAP_WIDTH, MAP_HEIGHT)
    map = pygame.image.load(f'image/map{MAP_WIDTH}x{MAP_HEIGHT}.png')
    map = pygame.transform.scale(map, (WIDTH_SCALE-GRID_SIZE*2, HEIGHT_SCALE-GRID_SIZE*2))
    init_game()

    # Update Time, Score
    time = 0
    score1 = 0
    score2 = 0

    # Mode Button
    mode_button = create_button(200, 60)
    mode_text = font64.render("Mode", True, BLACK)
    mode_button.blit(mode_text, (42, 10))
    screen.blit(mode_button, (500, 300))

    # Quit Button
    quit_button = create_button(200, 60)
    quit_text = font64.render("Quit", True, BLACK)
    quit_button.blit(quit_text, (55, 10))
    screen.blit(quit_button, (500, 500))

    # Setting Button
    setting_button = create_button(200, 60)
    setting_text = font64.render("Setting", True, BLACK)
    setting_button.blit(setting_text, (23, 10))
    screen.blit(setting_button, (500, 400))

def mode_logic():
    screen.blit(background, (0, 0))
    display_text("Mode", 600, 200, GOLD, font100)

    one_player_button = create_button(200, 60)
    one_player_text = font64.render("1P", True, BLACK)
    one_player_button.blit(one_player_text, (75, 10))
    screen.blit(one_player_button, (350, 300))

    pvp_button = create_button(200, 60)
    pvp_text = font64.render("PvP", True, BLACK)
    pvp_button.blit(pvp_text, (65, 10))
    screen.blit(pvp_button, (650, 300))

    one_AI_button = create_button(200, 60)
    one_AI_text = font64.render("AI", True, BLACK)
    one_AI_button.blit(one_AI_text, (75, 10))
    screen.blit(one_AI_button, (350, 400))

    pve_button = create_button(200, 60)
    pve_text = font64.render("PvE", True, BLACK)
    pve_button.blit(pve_text, (65, 10))
    screen.blit(pve_button, (650, 400))

    return_button = create_button(200, 60)
    return_text = font64.render("Return", True, BLACK)
    return_button.blit(return_text, (30, 10))
    screen.blit(return_button, (500, 600))

def one_player_logic():
    global game_state, time, score1, food_coords

    time += 1 / SNAKE_SPEED
    # Move Snake
    new_head = move_snake(snake1, snake1_direction)

    collision = (
        # With Boundary
        new_head[0] < 4
        or new_head[0] >= GRID_WIDTH
        or new_head[1] < 4
        or new_head[1] >= GRID_HEIGHT
        # With Itself
        or new_head in snake1[1:]
        # With Obstacles
        or new_head in obstacles_list
    )

    if collision:
        game_state = "game_over1"
        music_stop()
        dead_sound.play()
    else:
        snake1.insert(0, new_head)
        if snake1[0] == food_coords:
            eat_sound.play()
            score1 += 1
            food_coords = generate_food_location(snake1, obstacles_list)
        else:
            snake1.pop()

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image, (650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))
    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("Snake Game", 950, 120, GOLD, font100)

    # Pause Button
    pause_button = create_button(200, 60)
    pause_text = font64.render("Pause", True, BLACK)
    pause_button.blit(pause_text, (40, 10))
    screen.blit(pause_button, (850, 200))

def PvP_logic():
    global game_state, time, score1, score2, food_coords

    time += 1 / SNAKE_SPEED
    # Move Snake
    new_head1 = move_snake(snake1, snake1_direction)
    new_head2 = move_snake(snake2, snake2_direction)

    # Snake 1
    collision1 = (
        # With Boundary
        new_head1[0] < 4
        or new_head1[0] >= GRID_WIDTH
        or new_head1[1] < 4
        or new_head1[1] >= GRID_HEIGHT
        # With Itself
        or new_head1 in snake1[1:]
        # With Obstacles
        or new_head1 in obstacles_list
    )

    # Snake 2
    collision2 = (
        # With Boundary
        new_head2[0] < 4
        or new_head2[0] >= GRID_WIDTH
        or new_head2[1] < 4
        or new_head2[1] >= GRID_HEIGHT
        # With Itself
        or new_head2 in snake2[1:]
        # With Obstacles
        or new_head2 in obstacles_list
    )

    if collision1 or collision2:
        game_state = "game_over2"
        music_stop()
        dead_sound.play()
    else:
        snake1.insert(0, new_head1)
        snake2.insert(0, new_head2)
        if snake1[0] == food_coords:
            eat_sound.play()
            score1 += 1
            food_coords = generate_food_location(snake1, obstacles_list)
            snake2.pop()
        elif snake2[0] == food_coords:
            eat_sound.play()
            score2 += 1
            food_coords = generate_food_location(snake2, obstacles_list)
            snake1.pop()
        else:
            snake1.pop()
            snake2.pop()

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image, (650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))

    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))

    for i, segment in enumerate(snake2):
        if i == 0:
            screen.blit(head2, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body2, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))

    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score1: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("Score2: "+str(score2), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+80, WHITE, font36)
    display_text("Snake Game", 950, 120, GOLD, font100)

    # Pause Button
    pause_button = create_button(200, 60)
    pause_text = font64.render("Pause", True, BLACK)
    pause_button.blit(pause_text, (40, 10))
    screen.blit(pause_button, (850, 200))

def pause_logic():
    global game_state

    pause_display = pygame.image.load('image/pause.png').convert_alpha()
    pause_display = pygame.transform.scale(pause_display, (760, 400))

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))

    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    for i, segment in enumerate(snake2):
        if i == 0:
            screen.blit(head2, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body2, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    display_text("Score: "+str(score1), 125, 720, WHITE, font36)
    show_time(time)

    # Resume Button
    resume_button = create_button(200, 60)
    resume_text = font64.render("Resume", True, BLACK)
    resume_button.blit(resume_text, (15, 10))
    pause_display.blit(resume_button, (80, 100))

    # Retry Button
    retry_button = create_button(200, 60)
    retry_text = font64.render("Retry", True, BLACK)
    retry_button.blit(retry_text, (45, 10))
    pause_display.blit(retry_button, (80, 250))

    # Menu Button
    menu_button = create_button(200, 60)
    menu_text = font64.render("Menu", True, BLACK)
    menu_button.blit(menu_text, (42, 10))
    pause_display.blit(menu_button, (480, 100))

    # Setting Button
    quit_button = create_button(200, 60)
    quit_text = font64.render("Quit", True, BLACK)
    quit_button.blit(quit_text, (55, 10))
    pause_display.blit(quit_button, (480, 250))

    screen.blit(pause_display, (0, 180))
    screen.blit(snake_image, (650, 300))

    if music_playing:
        screen.blit(music_on_image, (890, 180))
    else:
        screen.blit(music_off_image, (890, 180))

    display_text("Paused", 950, 120, GOLD, font100)

def resume_logic():
    global game_state, resume_countdown

    pause_display = pygame.image.load('image/pause.png').convert_alpha()
    pause_display = pygame.transform.scale(pause_display, (760, 400))

    if resume_countdown > 0:
        count_sound.play()
        count_txt = font100.render(str(resume_countdown), True, BLACK)
        pause_display.blit(count_txt, (370, 120))
        screen.blit(pause_display, (0, 180))
        pygame.display.flip()

        pygame.time.wait(1000)
        resume_countdown -= 1
    else:
        resume_countdown = 3
        music_unpause()
        game_state = game_state2

def game_over1_logic():
    global game_state, high_score, score1, time

    # Update High Score
    high_score = max(high_score, score1)

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image, (650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))
    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))

    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("High Score: "+str(high_score), 960, 200, WHITE, font36)
    display_text("Game Over", 960, 120, GOLD, font100)

    # Retry Button
    retry_button = create_button(200, 60)
    retry_text = font64.render("Retry", True, BLACK)
    retry_button.blit(retry_text, (45, 10))
    screen.blit(retry_button, (750, 240))

    # Menu Button
    menu_button = create_button(200, 60)
    menu_text = font64.render("Menu", True, BLACK)
    menu_button.blit(menu_text, (42, 10))
    screen.blit(menu_button, (970, 240))

def game_over2_logic():
    global game_state, high_score, score1, score2

    # Update High Score
    high_score = max(high_score, score1, score2)

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image, (650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))
    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))

    for i, segment in enumerate(snake2):
        if i == 0:
            screen.blit(head2, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body2, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))

    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score1: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("Score2: "+str(score2), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+80, WHITE, font36)

    display_text("High Score: "+str(high_score), 960, 200, WHITE, font36)
    display_text("Game Over", 960, 120, GOLD, font100)

    # Retry Button
    retry_button = create_button(200, 60)
    retry_text = font64.render("Retry", True, BLACK)
    retry_button.blit(retry_text, (45, 10))
    screen.blit(retry_button, (750, 240))

    # Menu Button
    menu_button = create_button(200, 60)
    menu_text = font64.render("Menu", True, BLACK)
    menu_button.blit(menu_text, (42, 10))
    screen.blit(menu_button, (970, 240))

def setting_logic():
    global game_state

    screen.blit(background, (0, 0))

    # Return Button
    return_button = create_button(200, 60)
    return_text = font64.render("Return", True, BLACK)
    return_button.blit(return_text, (30, 10))
    screen.blit(return_button, (500, 600))

    # Setting Frame
    setting_frame = pygame.image.load('image/setting2.png').convert()
    setting_frame = pygame.transform.scale(setting_frame, (500, 320))
    txt_setting = font64.render("SETTING", True, BLACK)
    setting_frame.blit(txt_setting, (160, 25))

    # Speed Frame
    txt_speed = font64.render("Speed", True, BLACK)
    setting_frame.blit(txt_speed, (24, 100))

    # Speed Number
    speed_x = 370
    speed_y = 100
    for char in speed_text:
        char = font64.render(char, True, speed_color)
        setting_frame.blit(char, (speed_x, speed_y))
        speed_x += 25

    # Map Size
    txt_map_size = font64.render("Map Size", True, BLACK)
    setting_frame.blit(txt_map_size, (24, 180))

    # Map Size -WIDTH Number
    width_x = 324
    width_y = 180
    for char in width_text:
        char = font64.render(char, True, width_color)
        setting_frame.blit(char, (width_x, width_y))
        width_x += 25

    # Map Size -HEIGHT Number
    height_x = 420
    height_y = 180
    for char in height_text:
        char = font64.render(char, True, height_color)
        setting_frame.blit(char, (height_x, height_y))
        height_x += 25

    # Obstacles Frame
    txt_obstacles = font64.render("Obstacles", True, BLACK)
    setting_frame.blit(txt_obstacles, (24, 260))

    # Number of Obstacles
    obstacles_x = 370
    obstacles_y = 260
    for char in obstacles_text:
        char = font64.render(char, True, obstacles_color)
        setting_frame.blit(char, (obstacles_x, obstacles_y))
        obstacles_x += 25

    screen.blit(setting_frame, (SETTING_WIDTH, SETTING_HEIGHT))

    display_text("Click on the value -> Delete and change -> Enter", 600, 150, RED, font24)
    display_text("Min = 5", 270, 300, BLACK, font36)
    display_text("Min = 11x11", 244, 380, BLACK, font36)
    display_text("Min = 5", 270, 460, BLACK, font36)

    display_text("Max = 30", 940, 300, BLACK, font36)
    display_text("Max = 30x30", 966, 380, BLACK, font36)
    display_text("Max = 30", 940, 460, BLACK, font36)

def AI_logic():
    screen.blit(background, (0, 0))
    display_text("AI Mode", 600, 200, GOLD, font100)

    bfs_button = create_button(200, 60)
    bfs_text = font36.render("BFS Method", True, BLACK)
    bfs_button.blit(bfs_text, (15, 10))
    screen.blit(bfs_button, (350, 300))

    dfs_button = create_button(200, 60)
    dfs_text = font36.render("DFS Method", True, BLACK)
    dfs_button.blit(dfs_text, (15, 10))
    screen.blit(dfs_button, (350, 380))

    id_button = create_button(200, 60)
    id_text = font36.render("ID Method", True, BLACK)
    id_button.blit(id_text, (15, 10))
    screen.blit(id_button, (350, 460))

    ucs_button = create_button(200, 60)
    ucs_text = font36.render("UCS Method", True, BLACK)
    ucs_button.blit(ucs_text, (15, 10))
    screen.blit(ucs_button, (650, 300))

    astar_button = create_button(200, 60)
    astar_text = font28.render("A STAR Method", True, BLACK)
    astar_button.blit(astar_text, (15, 13))
    screen.blit(astar_button, (650, 380))

    greedy_button = create_button(200, 60)
    greedy_text = font28.render("GREEDY Method", True, BLACK)
    greedy_button.blit(greedy_text, (15, 13))
    screen.blit(greedy_button, (650, 460))

    return_button = create_button(200, 60)
    return_text = font64.render("Return", True, BLACK)
    return_button.blit(return_text, (30, 10))
    screen.blit(return_button, (500, 600))

def bfs_AI_logic():
    global game_state, time, score1, food_coords, snake1_direction

    time += 1 / SNAKE_SPEED

    bfs_path = AI_method.bfs(snake1[0], food_coords, obstacles_list, snake1, GRID_WIDTH, GRID_HEIGHT)

    new_head = None

    if bfs_path:
        snake1_direction = bfs_path[0]
        new_head = (snake1[0][0] + snake1_direction[0], snake1[0][1] + snake1_direction[1])

    if new_head is not None:
        collision = (
            # With Boundary
            (new_head[0] < 4)
            or (new_head[0] >= GRID_WIDTH)
            or (new_head[1] < 4)
            or (new_head[1] >= GRID_HEIGHT)
            # With Itself
            or (new_head in snake1[1:])
            # With Obstacles
            or (new_head in obstacles_list)
        )
    else:
        collision = True

    if collision:
        game_state = "game_over1"
        music_stop()
        dead_sound.play()
    else:
        snake1.insert(0, new_head)
        if snake1[0] == food_coords:
            eat_sound.play()
            score1 += 1
            food_coords = generate_food_location(snake1, obstacles_list)
        else:
            snake1.pop()

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image,(650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))
    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("Snake Game", 950, 120, GOLD, font100)

    # Pause Button
    pause_button = create_button(200, 60)
    pause_text = font64.render("Pause", True, BLACK)
    pause_button.blit(pause_text, (40, 10))
    screen.blit(pause_button, (850, 200))


def dfs_AI_logic():
    global game_state, time, score1, food_coords, snake1_direction

    time += 1 / SNAKE_SPEED

    dfs_path = AI_method.dfs(snake1[0], food_coords, obstacles_list, snake1, GRID_WIDTH, GRID_HEIGHT)

    new_head = None

    if dfs_path:
        snake1_direction = dfs_path[0]
        new_head = (snake1[0][0] + snake1_direction[0], snake1[0][1] + snake1_direction[1])

    if new_head is not None:
        collision = (
            # With Boundary
            (new_head[0] < 4)
            or (new_head[0] >= GRID_WIDTH)
            or (new_head[1] < 4)
            or (new_head[1] >= GRID_HEIGHT)
            # With Itself
            or (new_head in snake1[1:])
            # With Obstacles
            or (new_head in obstacles_list)
        )
    else:
        collision = True

    if collision:
        game_state = "game_over1"
        music_stop()
        dead_sound.play()
    else:
        snake1.insert(0, new_head)
        if snake1[0] == food_coords:
            eat_sound.play()
            score1 += 1
            food_coords = generate_food_location(snake1, obstacles_list)
        else:
            snake1.pop()

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image,(650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))
    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("Snake Game", 950, 120, GOLD, font100)

    # Pause Button
    pause_button = create_button(200, 60)
    pause_text = font64.render("Pause", True, BLACK)
    pause_button.blit(pause_text, (40, 10))
    screen.blit(pause_button, (850, 200))


def ID_AI_logic():
    global game_state, time, score1, food_coords, snake1_direction

    time += 1 / SNAKE_SPEED

    ID_path = AI_method.ID(snake1[0], food_coords, obstacles_list, snake1, GRID_WIDTH, GRID_HEIGHT)

    new_head = None

    if ID_path:
        snake1_direction = ID_path[0]
        new_head = (snake1[0][0] + snake1_direction[0], snake1[0][1] + snake1_direction[1])

    if new_head is not None:
        collision = (
            # With Boundary
            (new_head[0] < 4)
            or (new_head[0] >= GRID_WIDTH)
            or (new_head[1] < 4)
            or (new_head[1] >= GRID_HEIGHT)
            # With Itself
            or (new_head in snake1[1:])
            # With Obstacles
            or (new_head in obstacles_list)
        )
    else:
        collision = True

    if collision:
        game_state = "game_over1"
        music_stop()
        dead_sound.play()
    else:
        snake1.insert(0, new_head)
        if snake1[0] == food_coords:
            eat_sound.play()
            score1 += 1
            food_coords = generate_food_location(snake1, obstacles_list)
        else:
            snake1.pop()

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image,(650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))
    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("Snake Game", 950, 120, GOLD, font100)

    # Pause Button
    pause_button = create_button(200, 60)
    pause_text = font64.render("Pause", True, BLACK)
    pause_button.blit(pause_text, (40, 10))
    screen.blit(pause_button, (850, 200))


def ucs_AI_logic():
    global game_state, time, score1, food_coords, snake1_direction

    time += 1 / SNAKE_SPEED

    ucs_path = AI_method.ucs(snake1[0], food_coords, obstacles_list, snake1, GRID_WIDTH, GRID_HEIGHT)

    new_head = None

    if ucs_path:
        snake1_direction = ucs_path[0]
        new_head = (snake1[0][0] + snake1_direction[0], snake1[0][1] + snake1_direction[1])

    if new_head is not None:
        collision = (
            # With Boundary
            (new_head[0] < 4)
            or (new_head[0] >= GRID_WIDTH)
            or (new_head[1] < 4)
            or (new_head[1] >= GRID_HEIGHT)
            # With Itself
            or (new_head in snake1[1:])
            # With Obstacles
            or (new_head in obstacles_list)
        )
    else:
        collision = True

    if collision:
        game_state = "game_over1"
        music_stop()
        dead_sound.play()
    else:
        snake1.insert(0, new_head)
        if snake1[0] == food_coords:
            eat_sound.play()
            score1 += 1
            food_coords = generate_food_location(snake1, obstacles_list)
        else:
            snake1.pop()

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image,(650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))
    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("Snake Game", 950, 120, GOLD, font100)

    # Pause Button
    pause_button = create_button(200, 60)
    pause_text = font64.render("Pause", True, BLACK)
    pause_button.blit(pause_text, (40, 10))
    screen.blit(pause_button, (850, 200))

def greedy_AI_logic():
    global game_state, time, score1, food_coords, snake1_direction

    time += 1 / SNAKE_SPEED

    ucs_path = AI_method.greedy(snake1[0], food_coords, obstacles_list, snake1, GRID_WIDTH, GRID_HEIGHT)

    new_head = None

    if ucs_path:
        snake1_direction = ucs_path[0]
        new_head = (snake1[0][0] + snake1_direction[0], snake1[0][1] + snake1_direction[1])

    if new_head is not None:
        collision = (
            # With Boundary
            (new_head[0] < 4)
            or (new_head[0] >= GRID_WIDTH)
            or (new_head[1] < 4)
            or (new_head[1] >= GRID_HEIGHT)
            # With Itself
            or (new_head in snake1[1:])
            # With Obstacles
            or (new_head in obstacles_list)
        )
    else:
        collision = True

    if collision:
        game_state = "game_over1"
        music_stop()
        dead_sound.play()
    else:
        snake1.insert(0, new_head)
        if snake1[0] == food_coords:
            eat_sound.play()
            score1 += 1
            food_coords = generate_food_location(snake1, obstacles_list)
        else:
            snake1.pop()

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image,(650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))
    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("Snake Game", 950, 120, GOLD, font100)

    # Pause Button
    pause_button = create_button(200, 60)
    pause_text = font64.render("Pause", True, BLACK)
    pause_button.blit(pause_text, (40, 10))
    screen.blit(pause_button, (850, 200))



def PvE_logic():
    screen.blit(background, (0, 0))
    display_text("AI Mode", 600, 200, GOLD, font100)

    bfs_button = create_button(200, 60)
    bfs_text = font36.render("BFS Method", True, BLACK)
    bfs_button.blit(bfs_text, (15, 10))
    screen.blit(bfs_button, (350, 300))

    dfs_button = create_button(200, 60)
    dfs_text = font36.render("DFS Method", True, BLACK)
    dfs_button.blit(dfs_text, (15, 10))
    screen.blit(dfs_button, (350, 380))

    id_button = create_button(200, 60)
    id_text = font36.render("ID Method", True, BLACK)
    id_button.blit(id_text, (15, 10))
    screen.blit(id_button, (350, 460))

    ucs_button = create_button(200, 60)
    ucs_text = font36.render("UCS Method", True, BLACK)
    ucs_button.blit(ucs_text, (15, 10))
    screen.blit(ucs_button, (650, 300))

    astar_button = create_button(200, 60)
    astar_text = font28.render("A STAR Method", True, BLACK)
    astar_button.blit(astar_text, (15, 13))
    screen.blit(astar_button, (650, 380))

    greedy_button = create_button(200, 60)
    greedy_text = font28.render("GREEDY Method", True, BLACK)
    greedy_button.blit(greedy_text, (15, 13))
    screen.blit(greedy_button, (650, 460))

    return_button = create_button(200, 60)
    return_text = font64.render("Return", True, BLACK)
    return_button.blit(return_text, (30, 10))
    screen.blit(return_button, (500, 600))

def bfs_PvE_logic():
    global game_state, time, score1, score2, food_coords, snake1_direction, snake2_direction

    time += 1 / SNAKE_SPEED

    new_head1 = move_snake(snake1, snake1_direction)

    collision1 = (
        # With Boundary
        new_head1[0] < 4
        or new_head1[0] >= GRID_WIDTH
        or new_head1[1] < 4
        or new_head1[1] >= GRID_HEIGHT
        # With Itself
        or new_head1 in snake1[1:]
        # With Obstacles
        or new_head1 in obstacles_list
    )

    bfs_path = AI_method.bfs(snake2[0], food_coords, obstacles_list, snake2, GRID_WIDTH, GRID_HEIGHT)

    new_head2 = None

    if bfs_path:
        snake2_direction = bfs_path[0]
        new_head2 = (snake2[0][0] + snake2_direction[0], snake2[0][1] + snake2_direction[1])

    if new_head2 is not None:
        collision2 = (
            # With Boundary
            (new_head2[0] < 4)
            or (new_head2[0] >= GRID_WIDTH)
            or (new_head2[1] < 4)
            or (new_head2[1] >= GRID_HEIGHT)
            # With Itself
            or (new_head2 in snake2[1:])
            # With Obstacles
            or (new_head2 in obstacles_list)
        )
    else:
        collision2 = True

    if collision1 or collision2:
        game_state = "game_over2"
        music_stop()
        dead_sound.play()
    else:
        snake1.insert(0, new_head1)
        snake2.insert(0, new_head2)
        if snake1[0] == food_coords:
            eat_sound.play()
            score1 += 1
            food_coords = generate_food_location(snake1, obstacles_list)
            snake2.pop()
        elif snake2[0] == food_coords:
            eat_sound.play()
            score2 += 1
            food_coords = generate_food_location(snake2, obstacles_list)
            snake1.pop()
        else:
            snake1.pop()
            snake2.pop()

    screen.blit(background, (0, 0))
    screen.blit(map, (60, 60))
    screen.blit(snake_image,(650, 300))

    for obstacle_coords in obstacles_list:
        screen.blit(obstacles, (obstacle_coords[0] * GRID_SIZE, obstacle_coords[1] * GRID_SIZE))
    for i, segment in enumerate(snake1):
        if i == 0:
            screen.blit(head1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body1, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))

    for i, segment in enumerate(snake2):
        if i == 0:
            screen.blit(head2, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
        else:
            screen.blit(body2, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
    screen.blit(food, (food_coords[0] * GRID_SIZE, food_coords[1] * GRID_SIZE))

    show_time(time)

    display_text("Score1: "+str(score1), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+40, WHITE, font36)
    display_text("Score2: "+str(score2), WIDTH_SCALE-GRID_SIZE*(MAP_WIDTH-2), HEIGHT_SCALE+80, WHITE, font36)
    display_text("Snake Game", 950, 120, GOLD, font100)

    # Pause Button
    pause_button = create_button(200, 60)
    pause_text = font64.render("Pause", True, BLACK)
    pause_button.blit(pause_text, (40, 10))
    screen.blit(pause_button, (850, 200))

init_game()

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_key_events(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event)

    if game_state == "menu":
        menu_logic()
    elif game_state == "mode":
        mode_logic()
    elif game_state == "1player":
        one_player_logic()
    elif game_state == "game_over1":
        game_over1_logic()
    elif game_state == "pvp":
        PvP_logic()
    elif game_state == "game_over2":
        game_over2_logic()
    elif game_state == "pause":
        pause_logic()
    elif game_state == "resume":
        resume_logic()
    elif game_state == "setting":
        setting_logic()

    elif game_state == "AI":
        AI_logic()
    elif game_state == "bfs_AI":
        bfs_AI_logic()
    elif game_state == "dfs_AI":
        dfs_AI_logic()
    elif game_state == "ID_AI":
        ID_AI_logic()
    elif game_state == "ucs_AI":
        ucs_AI_logic()
    elif game_state == "greedy_AI":
        greedy_AI_logic()

    elif game_state == "pve":
        PvE_logic()
    elif game_state == "bfs_pve":
        bfs_PvE_logic()

    pygame.display.flip()
    pygame.time.Clock().tick(SNAKE_SPEED)
