import pygame
from GUI import Text, Button
from math_util import Vector2

return_value = None

def play():
    global return_value
    return_value = "play"

def settings():
    pass

def shop():
    pass

# Function called to load the main menu
def load(surface):
    global window
    global title_text
    global subtitle_text
    global buttons
    global return_value

    window = surface

    title_text = Text(window, text="Aero", size=150, color=(255, 255, 255), position=Vector2(0,-90))
    subtitle_text = Text(window, text="A Flying Game", color=(255, 255, 255))

    # Create play button
    play_button = Button(
        surface=surface,
        command=play,
        anchor=Vector2(0.5, 1),
        position=Vector2(0, -110),
        normal_color=(46, 45, 77),
        hover_color=(68, 85, 208),
        image=pygame.image.load("assets/images/right.png")
        )

    # Create setttings button
    settings_button = Button(
        surface=surface,
        command=settings,
        anchor=Vector2(0.5, 1),
        position=Vector2(197, -110),
        normal_color=(46, 45, 77),
        hover_color=(68, 85, 208),
        image=pygame.image.load("assets/images/gear.png")
        )

    # Create setttings button
    shop_button = Button(
        surface=surface,
        command=shop,
        anchor=Vector2(0.5, 1),
        position=Vector2(-197, -110),
        normal_color=(46, 45, 77),
        hover_color=(68, 85, 208),
        image=pygame.image.load("assets/images/shop.png")
        )

    # Create button list with only play buttoon
    buttons = [play_button, settings_button, shop_button]

    # Reset return value
    return_value = None

# Function called every frame
def update(mouse_position, mouse_pressing):
    global return_value

    for button in buttons:
        button.update(mouse_position, mouse_pressing)

    # Return the return value every frame
    return return_value

# Function for displaying the main menu
def draw():
    global title_text
    global subtitle_text
    global window

    # Clear window - draw background
    window.fill((23, 22, 38))

    title_text.draw()
    subtitle_text.draw()

    for button in buttons:
        button.draw()