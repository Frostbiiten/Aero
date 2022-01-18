import pygame
from GUI import Text, FontPaths, Anchors, Button
from math_util import Vector2
from math import ceil
from easing_functions import *

text = []
buttons = []

background_rect_ease = ExponentialEaseInOut(0, 1, 1.2)
text_opacity_ease = ExponentialEaseInOut(0, 255, 0.7)
score_counter_ease = ExponentialEaseOut(0, 1, 3)
button_scalar_ease = ExponentialEaseOut(0, 1, 0.7)

global score

return_value = None

def replay():
    global return_value
    return_value = "replay"

def exit():
    global return_value
    return_value = "exit"

def load(_surface, _score, high_score):
    global surface
    global transition_alpha
    global darken_overlay 
    global replay_button
    global buttons
    global score
    global text
    global return_value

    score = _score
    surface = _surface
    transition_alpha = 0

    darken_overlay = pygame.Surface([surface.get_width(), surface.get_height()])
    darken_overlay.fill((0, 0, 0))

    # Create score string. If there are not enough digits, insert some
    score_string = str(score)
    if len(score_string) < 4:
        score_string = '0' * (4 - len(score_string)) + score_string

    score_number_text = Text(
        surface,
        text=score_string,
        size=120,
        color=(255, 255, 255),
        position=Vector2(0, -150),
        text_anchor=Anchors.TOP_CENTER,
        font=FontPaths.EXTRA_BOLD
    )
    score_title_text =Text(
        surface,
        text="New High Score!" if high_score else "Score",
        size=50,
        color=(255, 255, 255),
        position=Vector2(0, -120),
        text_anchor=Anchors.BOTTOM_CENTER,
        font=FontPaths.SEMI_BOLD
    )
    text = [score_number_text, score_title_text]

    # Create play button
    replay_button = Button(
        surface=surface,
        command=replay,
        anchor=Vector2(0.5, 1),
        position=Vector2(105, -250),
        normal_color=(46, 45, 77),
        hover_color=(68, 85, 208),
        image=pygame.image.load("assets/images/replay.png")
        )

    replay_button.scalar = 0

    # Create play button
    exit_button = Button(
        surface=surface,
        command=exit,
        anchor=Vector2(0.5, 1),
        position=Vector2(-105, -250),
        normal_color=(46, 45, 77),
        hover_color=(255, 33, 96),
        image=pygame.image.load("assets/images/exit.png")
        )


    exit_button.scalar = 0

    # Set buttons
    buttons = [replay_button, exit_button]

    # Reset return value
    return_value = None

def update(delta_time, mouse_position, mouse_pressing):
    global transition_alpha   
    global score_counter_ease
    global button_scalar_ease
    global return_value
    global surface
    global buttons
    global score
    global text

    if return_value != None:
        return return_value

    transition_alpha += delta_time

    # Update score counter and text
    score_counter_progress = score_counter_ease.ease(min(transition_alpha, score_counter_ease.duration))
    score_string = str(ceil(score * score_counter_progress))
    if len(score_string) < 4:
        score_string = '0' * (4 - len(score_string)) + score_string

    if score_string != text[0].text:
        text[0].text = score_string
        text[0].update()

    # Update buttons
    for button in buttons:
        button.update(mouse_position, mouse_pressing)
        if transition_alpha - 1 < 0:
            button.scalar = 0
        elif transition_alpha - 1 < button_scalar_ease.duration:
            button.scalar = button_scalar_ease.ease(transition_alpha - 1)
    
def draw():
    global background_rect_ease
    global transition_alpha
    global text_opacity_ease
    global darken_overlay
    global surface
    global buttons
    global text

    alpha = background_rect_ease.ease(transition_alpha)

    darken_overlay.set_alpha(alpha * 255)
    surface.blit(darken_overlay, (0, 0))

    rect_size = Vector2(550, 450) * alpha
    background_rect = pygame.Rect(0, 0, rect_size.x, rect_size.y)
    background_rect.center = surface.get_rect().center
    pygame.draw.rect(surface,
        color=(29, 29, 43),
        rect=background_rect,
        border_radius=5
    )

    text_alpha = text_opacity_ease.ease(transition_alpha - 0.6)

    # Draw text and buttons
    for text_widget in text:
        text_widget.draw(text_alpha)

    if transition_alpha > 0:
        for button in buttons:
            button.draw()