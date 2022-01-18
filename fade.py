import pygame
from easing_functions import *

# Class used to fade to black and back
class Fader:
    def __init__(self, screen, alpha = 1, fade_function = ExponentialEaseInOut(0, 1, 1)):
        # Mask setup
        rect = screen.get_rect()
        self.mask = pygame.Surface([rect.width, rect.height])
        self.mask.fill((0, 0, 0))

        # Properties setup
        self.alpha = alpha # Alpha of fade interpolation (0-1)
        self.fade_function = fade_function # Fade interpolation function
        self.visible = False # If the black fade screen is visible
        self.queue = False

    # Function for updating fade values
    def update(self, delta_time):
        # Fade alpha based on visibility
        if self.visible:
            self.alpha += delta_time
        else:
            self.alpha -= delta_time

        # Clamp in 0-1 range
        self.alpha = max(0, min(self.alpha, 1))

    # Function used to draw to screen
    def draw(self, screen):
        # Only draw if not fully transparent
        if self.alpha > 0:
            self.mask.set_alpha(self.fade_function.ease(self.alpha) * 255)
            screen.blit(self.mask, (0, 0))