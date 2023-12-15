import asyncio
import pygame
from pygame.locals import *

# Game tutorial by Coding With Russ
# https://www.youtube.com/watch?v=mR5pAJdW8fo&ab_channel=CodingWithRuss
# Game re-created by Steven Theron
# 09 October 2023

# Part 1:
# Creating the game board and a game ending event. E.g. Quit game.
# Create fx to draw grid.

# Part 2:
# Create event handler to handle user clicks.
# Create fx to draw Player markers.

# Part 3:
# Add the other Game end conditions.

pygame.init()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
LINE_WIDTH = 6

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define colors
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

font = pygame.font.SysFont(None, 40)

# Create play again rectangle
play_again_rect = Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)


async def main():
    markers = init_grid()

    clicked = False
    player = 1
    winner = 0
    game_over = False

    # Game loop
    run = True
    while run:
        draw_grid()
        draw_markers(markers)

        # Event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Handle Mouse clicks events
            if game_over == 0:
                if event.type == pygame.MOUSEBUTTONDOWN and clicked is False:
                    clicked = True
                if event.type == pygame.MOUSEBUTTONUP and clicked is True:
                    clicked = False
                    coords = pygame.mouse.get_pos()
                    cell_x = coords[0]
                    cell_y = coords[1]

                    if markers[cell_x // 100][cell_y // 100] == 0:
                        markers[cell_x // 100][cell_y // 100] = player
                        player *= -1  # Flip between player 1 and the other player...
                    game_over, winner = check_winner(markers, winner, game_over)

        if game_over:
            draw_winner(winner)
            #  Check if user clicks Play Again Rectangle.
            if event.type == pygame.MOUSEBUTTONDOWN and clicked is False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked is True:
                clicked = False
                coords = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(coords):
                    # Reset game variables.
                    coords = []
                    player = 1
                    winner = 0
                    game_over = False
                    markers = init_grid()

        pygame.display.update()

        await asyncio.sleep(0)
        if not run:
            pygame.quit()
            return


def init_grid():
    # global winner
    # global game_over
    # global player

    markers = []
    # coords = []
    # player = 1
    # winner = 0
    # game_over = False

    for x in range(3):
        row = [0] * 3
        markers.append(row)

    return markers


def draw_grid():
    bg = (255, 255, 200)
    grid = (50, 50, 50)
    screen.fill(bg)
    for x in range(1, 3):
        pygame.draw.line(screen, grid, (0, x * 100), (SCREEN_WIDTH, x * 100), LINE_WIDTH)
        pygame.draw.line(screen, grid, (x * 100, 0), (x * 100, SCREEN_HEIGHT), LINE_WIDTH)


def draw_markers(markers):
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == 1:  # if player 1 is in this cell then draw player 1.
                pygame.draw.line(screen, green,
                                 (x_pos * 100 + 15, y_pos * 100 + 15),
                                 (x_pos * 100 + 85, y_pos * 100 + 85), LINE_WIDTH)
                pygame.draw.line(screen, green,
                                 (x_pos * 100 + 15, y_pos * 100 + 85),
                                 (x_pos * 100 + 85, y_pos * 100 + 15), LINE_WIDTH)
            if y == -1:
                pygame.draw.circle(screen, red,
                                   (x_pos * 100 + 50, y_pos * 100 + 50), 38, LINE_WIDTH)
            y_pos += 1
        x_pos += 1


def check_winner(markers, winner, game_over):
    # global winner
    # global game_over
    y_pos = 0

    for x in markers:
        # check columns
        if sum(x) == 3:
            winner = 1
            game_over = True
        if sum(x) == -3:
            winner = 2
            game_over = True

        # check rows
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == 3:
            winner = 1
            game_over = True
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == -3:
            winner = 2
            game_over = True
        y_pos += 1

    # check cross
    if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[2][0] + markers[1][1] + markers[0][2] == 3:
        winner = 1
        game_over = True
    if markers[0][0] + markers[1][1] + markers[2][2] == -3 or markers[2][0] + markers[1][1] + markers[0][2] == -3:
        winner = 2
        game_over = True

    return game_over, winner


def draw_winner(winner_arg):
    # create text, convert to image then display to screen.
    win_text = "Player " + str(winner_arg) + " wins!"
    win_img = font.render(win_text, True, blue)
    pygame.draw.rect(screen, green, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50))
    screen.blit(win_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

    play_again_text = "Play again?"
    play_again_img = font.render(play_again_text, True, blue)
    pygame.draw.rect(screen, green, play_again_rect)
    screen.blit(play_again_img, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10))


asyncio.run(main())
