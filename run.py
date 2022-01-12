import pygame
import sys
import random
pygame.init()
# Screen Dimensions
screen_width = 400
screen_height = 400
# Game Window
game_board = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Python in Python')
clock = pygame.time.Clock()
# Colours
white = (255, 255, 255)
black = (0, 0, 0)
lighter_square = (38, 52, 69)
darker_square = (32, 41, 55)
# Grid dimensions
grid_size = 20
# Produces a 20 x 20 grid
grid_width = 20
grid_height = 20
# Snake
snake_position = (0, 0)
snake_colour = (0, 159, 0)
snake_x = screen_width / 2
snake_y = screen_height / 2
snake_size = 20
current_score = 0
snake_speed = 5
# Apple
apple_position = (0, 0)
apple_colour = (200, 0, 0)
apple_x = round(random.randrange(0, screen_width - snake_size) / grid_size) * grid_size
apple_y = round(random.randrange(0, screen_height - snake_size) / grid_size) * grid_size
# Fonts
game_quit_font = pygame.font.SysFont("helvetica", 12)
score_font = pygame.font.SysFont("Courier", 16)
# Other
game_quit = False
game_over = False


def background(game_board):
    """
  Creates the chequered grid for the game based on if the grid number is disable by two or not. If it is apply the darker colour if not, apply the lighter colour.
  """
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x + y) % 2 == 0:
                square_one = pygame.Rect((x * grid_size, y * grid_size),
                                         (grid_size, grid_size))
                pygame.draw.rect(game_board, (lighter_square), square_one)
            else:
                square_two = pygame.Rect((x * grid_size, y * grid_size),
                                         (grid_size, grid_size))
                pygame.draw.rect(game_board, (darker_square), square_two)


def show_score():
    """
  Creates and displays the live updating score as the game is played.
  """
    font_score = pygame.font.SysFont("Courier", 16)
    scoreboard = font_score.render("Score: "+str(current_score), True, (white))
    game_board.blit(scoreboard, (5, 10))


# def high_score():
#     high_score = current_score
#     font_score = pygame.font.SysFont("Courier", 16)
#     scoreboard = font_score.render("High Score: "+str(current_score), True, (white))
#     game_board.blit(scoreboard, (245, 10))

def snake(game_board):
    """
  Creates and draws the snake using the variables and coordinates
  """
    for x, y in snake_list:
        pygame.draw.rect(game_board, snake_colour, [x, y, 20, 20])
        pygame.draw.rect(game_board, white, [x, y, 20, 20], 1)


snake_list = []
snake_length = 1


def apple(game_board):
    """
  Creates and draws the apple using the variables and coordinates
  """
    pygame.draw.rect(game_board, apple_colour, [apple_x, apple_y, 20, 20])
    pygame.draw.rect(game_board, white, [apple_x, apple_y, 20, 20], 1)


def apple_eaten(snake_x, apple_x, snake_y, apple_y, current_score, snake_speed, snake_length):
    """
  Detects whether the apple has been eaten and updates the scores, speed and apple postition accordingly.
  """
    if snake_x == apple_x and snake_y == apple_y:
        current_score += 10
        snake_speed += 0.5
        snake_length += 1
        print("Snake ate the apple")
        apple_x = round(random.randrange(0, screen_width - grid_size) / grid_size) * grid_size
        apple_y = round(random.randrange(0, screen_height - grid_size) / grid_size) * grid_size
    return snake_x, apple_x, snake_y, apple_y, current_score, snake_speed, snake_length


def message(msg, color):
    """
  Creates the message after the snake has crashed into the wall or into it's self.
  """
    mesg = game_quit_font.render(msg, True, white)
    game_board.blit(mesg, [screen_width/5, screen_height/2])


def keyboard_commands(move_horizontal, move_vertical):
    """
  Uses the keyboard commands from the direction arrows to move the snake around the grid.
  """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_horizontal = -20
                move_vertical = 0
            elif event.key == pygame.K_RIGHT:
                move_horizontal = 20
                move_vertical = 0
            elif event.key == pygame.K_UP:
                move_vertical = -20
                move_horizontal = 0
            elif event.key == pygame.K_DOWN:
                move_vertical = 20
                move_horizontal = 0
    return move_horizontal, move_vertical


def game_loop():
    """
  Game loop based on the game_quit and game_over variables inside while and if loops.
  """
    global game_over
    global game_quit
    global current_score
    global snake_length
    global apple_x
    global apple_y

    snake_x = screen_width / 2
    snake_y = screen_height / 2
    current_score = 0
    snake_length = 1
    snake_speed = 5
    move_horizontal = 0
    move_vertical = 0

    while game_over == False:
        move_horizontal, move_vertical = keyboard_commands(move_horizontal, move_vertical)
        snake_x += move_horizontal
        snake_y += move_vertical
        background(game_board)
        scoreboard = show_score()
        apple(game_board)
        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True
        snake(game_board)
        pygame.display.update()
        snake_x, apple_x, snake_y, apple_y, current_score, snake_speed, snake_length = apple_eaten(snake_x, apple_x, snake_y, apple_y, current_score, snake_speed, snake_length)
        clock.tick(snake_speed)

        if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
            game_over = True

        while game_over == True:
            game_board.fill(black)
            message("Game Over!\n Play Again?\n Yes (Y)/ No (N)", white)
            show_score()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        game_quit = True
                        game_over = True
                    if event.key == pygame.K_y:
                        game_quit = False
                        game_over = False
                        game_loop()

            pygame.display.update()
    pygame.quit()
    quit()
game_loop()
