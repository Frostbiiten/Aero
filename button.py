import pygame
import pygame.freetype
import math_util as mathu
import vector_util as vecu

class button():
    def __init__(self, surface, command, font, text = "Button", text_color = (10, 10, 10),
                position=vecu.vector2(0, 0), anchor=vecu.vector2(0.5, 0.5), dimensions=vecu.vector2(200, 200), 
                rounding = 10, normal_color=[220, 220, 220], hover_color=[250, 250, 250], pressed_color=[200, 200, 200],
                hover_scalar = 1.1):

        # Set button text
        self.text = text
        self.text_color = text_color
        self.font = font

        # Set up anchor, position and dimensions
        self.anchor = anchor
        self.position = position
        self.dimensions = dimensions
        self.rounding = rounding

        # Set up misc.
        self.surface = surface
        self.command = command
        self.pressed = False

        # Set up colors
        self.current_color = normal_color.copy()
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.hover_scalar = hover_scalar
        self.scalar = 1

        # Set up rect
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update_rect()

    def update_rect(self):
        # Get surface size
        surface_size = vecu.vector2(self.surface.get_size()[0], self.surface.get_size()[1])
        # Get top-left position of button
        position = (surface_size * self.anchor) - (self.dimensions * self.scalar / 2) + self.position
        # Get size of button
        size = self.dimensions * self.scalar
        # Set rect
        self.rect = pygame.Rect(position.x, position.y, size.x, size.y)

    def lerp_color(self, color, speed = 0.2):
        self.current_color[0] = mathu.lerp(self.current_color[0], color[0], speed)
        self.current_color[1] = mathu.lerp(self.current_color[1], color[1], speed)
        self.current_color[2] = mathu.lerp(self.current_color[2], color[2], speed)

    def update(self, mouse_position, pressing):
        # Update the rect bounds
        self.update_rect()

        # Check if mouse is over button and act accordingly
        if pygame.Rect.collidepoint(self.rect, mouse_position):
            if pressing == True:
                self.lerp_color(self.pressed_color)
                self.scalar = mathu.lerp(self.scalar, 1, 0.2)
                self.command()
            else:
                self.lerp_color(self.hover_color)
                self.scalar = mathu.lerp(self.scalar, self.hover_scalar, 0.2)
        else:
            self.lerp_color(self.normal_color)
            self.scalar = mathu.lerp(self.scalar, 1, 0.2)

    def draw(self):
        pygame.draw.rect(self.surface, self.current_color, self.rect, border_radius=self.rounding)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_size = text_surface.get_size()
        self.surface.blit(text_surface, (self.rect.center[0] - text_size[0] / 2, self.rect.center[1] - text_size[1] / 2))