# Pygame
import os
import pygame
import pygame.freetype
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from easing_functions import *

# Own files
from button import button
from fade import fader
from vector_util import lerp, vector2
import main_menu

# Globals
FPS = 60
WINDOW_RESOLUTION = [600, 800]
window = pygame.display.set_mode(WINDOW_RESOLUTION, pygame.NOFRAME)

# Create fader with black screen, fades out
fade = fader(window, 1)
fade.visible = False

def terminate():
    # bring window into scope
    global window

    # Slowly shrink window
    alpha = 0
    easing = ExponentialEaseInOut(start=1, end=0, duration = 1)
    while alpha < 1:
        current_size = vector2(WINDOW_RESOLUTION[0], WINDOW_RESOLUTION[1] * easing.ease(alpha))
        window = pygame.display.set_mode([int(current_size.x), int(current_size.y)], pygame.NOFRAME)
        alpha += 0.005

    # Close application when window is done shrinking
    pygame.quit()

def mainloop():
    # Bring window into scope
    global window
    quit = False

    # Start delta time clock
    delta_time_clock = pygame.time.Clock()

    # Create x buttn
    x_button = button(surface=window, command=terminate, image=pygame.image.load("assets/images/cross.png"), normal_color=[50, 50, 50], hover_color=[225, 30, 30],
    anchor=vector2(1, 0), dimensions=vector2(22, 22), position=vector2(-15, 15), rounding=1)

    # Load main menu
    main_menu.load(surface=window)

    while quit == False:
        # Get time since last frame for deltatime
        delta_time = delta_time_clock.tick(FPS)/1000

        mouse_button_down = False
        mouse_button_up = False

        # Handle events and input
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_button_down = True
                break
            if event.type == MOUSEBUTTONUP:
                mouse_button_up = True
                break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit = True
                    break
            elif event.type == QUIT:
                quit = True
                break

        # Clear screen to black
        window.fill((0, 0, 0))

        mouse_pos = pygame.mouse.get_pos()

        main_menu.update(mouse_pos, mouse_button_up, delta_time)
        main_menu.draw()

        x_button.update(mouse_pos, mouse_button_up)
        x_button.draw()

        # Draw fader last to cover everything
        fade.update(delta_time)
        fade.draw(window)

        # Display screen
        pygame.display.flip()
    
    # When loop is broken, quit must be true, so terminate
    terminate()

def main():
    pygame.init()
    mainloop()

main()