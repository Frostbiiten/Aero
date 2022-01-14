import pygame
from easing_functions import *

class fader:
    def __init__(self, screen, alpha = 1, fade_function = ExponentialEaseInOut(0, 1, 1)):
        # Mask setup
        rect = screen.get_rect()
        self.mask = pygame.Surface([rect.width, rect.height])
        self.mask.fill((0, 0, 0))

        # Properties setup
        self.alpha = alpha # Alpha of fade interpolation (0-1)
        self.fade_function = fade_function # Fade interpolation function
        self.visible = False # If the black fade screen is visible

    def update(self, dt):
        # Fade alpha based on visibility
        if self.visible:
            self.alpha += dt
        else:
            self.alpha -= dt

        # Clamp in 0-1 range
        self.alpha = max(0, min(self.alpha, 1))

    def draw(self, screen):
        if self.alpha > 0:
            self.mask.set_alpha(self.fade_function.ease(self.alpha) * 255)
            screen.blit(self.mask, (0, 0))