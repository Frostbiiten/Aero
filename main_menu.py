from button import button
from enum import Enum
from fade import fader
import pygame

from vector_util import vector2

buttons = []
window = None
pygame.font.init()
title_font = pygame.font.Font("assets/fonts/black_font.ttf", 150)
sub_title_font = pygame.font.Font("assets/fonts/bold_font.ttf", 30)

class colors (Enum):
    IRIS = [69, 74, 222]
    SPACE_CADET = [27, 31, 59]
    ELECTRIC_PURPLE = [177, 74, 237]
    FRENCH_MAUVE = [200, 116, 217]
    CAMEO_PINK = [225, 187, 201]

# Button functions
def play():
    pass

def settings():
    pass

def shop():
    pass

def load(surface):
    global buttons
    global window
    window = surface

    # Reset buttons
    buttons = []

    play_button = button(surface=surface, command=play, image=pygame.image.load("assets/images/right.png"),
        anchor=vector2(0.5, 1), dimensions=vector2(190, 100), position=vector2(0, -50),
        normal_color=colors.SPACE_CADET.value,hover_color=colors.IRIS.value, pressed_color=colors.SPACE_CADET.value, rounding=2)

    settings_button = button(surface=surface, command=settings, image=pygame.image.load("assets/images/gear.png"),
        anchor=vector2(1, 1), dimensions=vector2(190, 100), position=vector2(-100, -50),
        normal_color=colors.SPACE_CADET.value,hover_color=colors.IRIS.value, pressed_color=colors.SPACE_CADET.value, rounding=2)

    store_button = button(surface=surface, command=shop, image=pygame.image.load("assets/images/shoppingCart.png"),
        anchor=vector2(0, 1), dimensions=vector2(190, 100), position=vector2(100, -50),
        normal_color=colors.SPACE_CADET.value,hover_color=colors.IRIS.value, pressed_color=colors.SPACE_CADET.value, rounding=2)

    # Set buttons
    buttons = [play_button, settings_button, store_button]

    fade = fader(window, 1)
    fade.visible = False

def update(mouse_pos, mouse_pressing, dt):
    for button in buttons:
        button.update(mouse_pos, mouse_pressing)
    
def draw():
    global window
    global title_font

    # Clear window
    window.fill([channel / 2 for channel in colors.SPACE_CADET.value])

    # Render title font
    title_surface = title_font.render("AERO", True, colors.CAMEO_PINK.value)
    title_size = title_surface.get_size()
    window_rect = window.get_rect()
    window.blit(
        title_surface, (window_rect.center[0] - title_size[0] / 2, window_rect.center[1] - title_size[1] / 2 - 150))
    
    sub_title_surface = sub_title_font.render("A Game About Flight", True, colors.FRENCH_MAUVE.value)
    sub_title_size = sub_title_surface.get_size()
    window.blit(
        sub_title_surface, (window_rect.center[0] - sub_title_size[0] / 2, window_rect.center[1] - sub_title_size[1] / 2 - 60))

    for button in buttons:
        button.draw()