# Import pygame modules
import sys
import pygame

# Import keys
from pygame.locals import (MOUSEBUTTONUP, MOUSEBUTTONDOWN, K_ESCAPE, KEYDOWN)

# Import enum
from enum import Enum

from easing_functions import ExponentialEaseInOut

# Import project files
from GUI import Button
from fade import Fader
from math_util import Vector2

import main_menu
import main_game

# Globals
WINDOW_RESOLUTION = [600, 800]
window = pygame.display.set_mode(WINDOW_RESOLUTION, pygame.NOFRAME)

# Create fader with black screen, fades out at beginning
fade = Fader(window, 1)

# Game states
class GameState(Enum):
    MAIN_MENU = 0
    MAIN_GAME = 1
current_state = GameState.MAIN_MENU

# Function for closing the application
def terminate():
    # bring window and quit into scope
    global window

    # Slowly shrink window
    alpha = 0 # Start at progress 0, go to 1
    easing = ExponentialEaseInOut(WINDOW_RESOLUTION[1], end=1, duration = 1)
    while alpha < 1:
        current_size = Vector2(WINDOW_RESOLUTION[0], easing.ease(alpha))
        window = pygame.display.set_mode([int(current_size.x), int(current_size.y)], pygame.NOFRAME)
        alpha += 0.005

    # Close application when window is done shrinking
    pygame.display.quit()
    pygame.quit()
    sys.exit()

# Function for main game loop
def main_loop():
    # Bring needed variables into scope
    global window
    global current_state

    quit = False

    # Start delta time clock
    delta_time_clock = pygame.time.Clock()

    # Create x button
    x_button = Button(window,
                        command=terminate,
                        image=pygame.image.load("assets/images/cross.png"),
                        normal_color=[50, 50, 50],
                        hover_color=[225, 30, 30],
                        anchor=Vector2(1, 0),
                        dimensions=Vector2(22, 22),
                        position=Vector2(-15, 15),
                        )

    # Load main menu
    main_menu.load(window)

    while quit == False:
        # Get time since last frame for deltatime
        delta_time = delta_time_clock.tick()/1000

        # Create booleans to check if mouse button down/up
        mouse_button_down = False
        mouse_button_up = False

        # Handle events and input
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_button_down = True
            elif event.type == MOUSEBUTTONUP:
                mouse_button_up = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        # Update mouse position
        mouse_position = pygame.mouse.get_pos()

        if current_state == GameState.MAIN_MENU:
            # Update and draw main menu if needed
            menu_command = main_menu.update(mouse_position, mouse_button_up)

            # If there is no command, continue normally. If there is, act accordingly
            if menu_command == None:
                main_menu.draw()
            elif menu_command == "play":
                main_game.load(window)
                current_state = GameState.MAIN_GAME

        elif current_state == GameState.MAIN_GAME:

            game_command = main_game.update(mouse_position, mouse_button_down, delta_time)

            # If there is no command, continue normally. If there is, act accordingly
            if game_command == None:
                main_game.draw()
            elif game_command == "replay":
                main_game.load(window)
                current_state = GameState.MAIN_GAME
            elif game_command == "exit":
                main_menu.load(window)
                current_state = GameState.MAIN_MENU

        # Update and draw x button
        x_button.update(mouse_position, mouse_button_up)
        x_button.draw()

        # Draw fade last to cover everything
        fade.update(delta_time)
        fade.draw(window)

        # Display screen
        pygame.display.flip()

# Main function to initialize program
def main():
    pygame.init()
    main_loop()

# Call main function
main()