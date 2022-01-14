import pygame
import pygame.freetype
import particles
import button as pushbutton
from vector_util import vector2

WINDOW_RESOLUTION = [600, 800]
FPS = 60

window = pygame.display.set_mode(WINDOW_RESOLUTION, pygame.NOFRAME)

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

def terminate():
    pygame.quit()

def mainloop():
    global window
    quit = False
    delta_time_clock = pygame.time.Clock()

    # b = button.button(window, terminate, pygame.font.Font("assets/fonts/default_font.ttf", 32))
    # x = button.button(surface=window, command=terminate, font=pygame.font.Font("assets/fonts/default_font.ttf", 32), text="", text_color=(10, 10, 10),
    # position=vector2(-20, 20), anchor=vector2(1, 0), dimensions=vector2(30, 30), rounding=2, normal_color=[220, 220, 200],
    # hover_color=[255, 10, 10])

    buttons = []
    steps = 10

    for x in range(0, steps):
        for y in range(0, steps):
            b = pushbutton.button(surface=window, command=terminate,font=pygame.font.Font("assets/fonts/default_font.ttf", 32), text=str(y * steps + x), image=pygame.image.load("assets/images/cross.png"), rounding=0, hover_scalar=1.1, hover_color=(255, 0, 0),
            position=vector2(WINDOW_RESOLUTION[0] / steps / 2, WINDOW_RESOLUTION[1] / steps / 2), anchor=vector2(x / steps, y / steps), dimensions=vector2(WINDOW_RESOLUTION[0] / steps, WINDOW_RESOLUTION[1] / steps))
            buttons.append(b)

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

        '''
        b.update(mouse_pos, mouse_button_down)
        b.draw()

        x.update(mouse_pos, mouse_button_down)
        x.draw()
        '''
        for button in buttons:
            button.update(mouse_pos, mouse_button_down)
            button.draw()

        # Display screen
        pygame.display.flip()
    
    # When loop is broken, quit must be true, so terminate
    terminate()

def main():
    pygame.init()
    mainloop()

main()