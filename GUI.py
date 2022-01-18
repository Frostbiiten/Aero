'''
Edem Hoggar
GUI module
This is a GUI file that provides a layer of abstraction between pygame
and the rest of the game to make and operate several gui widgets
'''

import pygame
import pygame.freetype
from math_util import Vector2, lerp
from enum import Enum

# Initalize pygame fonts when imported to draw fonts
pygame.font.init()

# Enum of font paths to be used for GUI (from thickest to thinnest)
class FontPaths (Enum):
    # Boldest
    BOLDEST = "assets/fonts/boldest.ttf"
    BOLDEST_ITALIC = "assets/fonts/boldest_i.ttf"

    # Extra-Bold
    EXTRA_BOLD = "assets/fonts/extra_bold.ttf"
    EXTRA_BOLD_ITALIC = "assets/fonts/extra_bold_i.ttf"

    # Bold
    BOLD = "assets/fonts/bold.ttf"
    BOLD_ITALIC = "assets/fonts/bold_i.ttf"

    # Semi-Bold
    SEMI_BOLD = "assets/fonts/semi_bold.ttf"
    SEMI_BOLD_ITALIC = "assets/fonts/semi_bold_i.ttf"

    # Medium
    MEDIUM = "assets/fonts/medium.ttf"
    MEDIUM_ITALIC = "assets/fonts/medium_i.ttf"

    # Normal
    NORMAL = "assets/fonts/normal.ttf"
    NORMAL_ITALIC = "assets/fonts/normal_i.ttf"

    # Light
    LIGHT = "assets/fonts/light.ttf"
    LIGHT_ITALIC = "assets/fonts/light_i.ttf"

    # Extra-Light
    EXTRA_LIGHT = "assets/fonts/extra_light.ttf"
    EXTRA_LIGHT_ITALIC = "assets/fonts/extra_light_i.ttf"

    # Thin
    THIN = "assets/fonts/thin.ttf"
    THIN_ITALIC = "assets/fonts/thin_i.ttf"

# anchors
class Anchors (Enum):
    TOP_LEFT = Vector2(0, 0)
    TOP_CENTER = Vector2(0.5, 0)
    TOP_RIGHT = Vector2(1, 0)
    MIDDLE_RIGHT = Vector2(1, 0.5)
    BOTTOM_RIGHT = Vector2(1, 1)
    BOTTOM_CENTER = Vector2(0.5, 1)
    BOTTOM_LEFT = Vector2(0, 1)
    MIDDLE_LEFT = Vector2(0, 0.5)
    MIDDLE_CENTER = Vector2(0.5, 0.5)

# Dictionary for caching fonts, they are loaded when first used
font_dictionary = {}

# Text widget class
class Text():
    def __init__( self,
                surface, # Surface to draw the text on
                text, # Text to be displayed
                size = 20,
                color = (10, 10, 10), # The color of the text
                position=Vector2(0, 0), # The position offset of the text (pixels)
                screen_anchor=Vector2(0.5, 0.5), # The anchor of the image (0 to 1 screen range)
                font=FontPaths.NORMAL, # The font in which to display the text
                text_anchor=Anchors.MIDDLE_CENTER
                ):
        
        # Set the target surface and text
        self.surface = surface
        self.text = text
        self.color = color
        self.position = position
        self.screen_anchor = screen_anchor
        self.text_anchor = text_anchor.value

        # Get the font_key identifier, which contains the font and size
        font_key = (font.value, size)

        # Check if the specific font type exists in the dictionary. If not, insert it
        if font_key not in font_dictionary:
            font_dictionary[font_key] = pygame.font.Font(font.value, size)

        # The dictionary is guaranteed to have the font now, so set the font
        self.font = font_dictionary[font_key]

        # Update the font to prepare for drawing
        self.update()

    # Function to update the text. Only needs to be called when the text changes
    def update(self):
        # Render text to surface
        self.text_surface = self.font.render(self.text, True, self.color) # Draw text to text surface
        self.text_surface_size = Vector2(self.text_surface.get_size()[0], self.text_surface.get_size()[1]) # Update size of text surface
        self.surface_size = Vector2(self.surface.get_size()[0], self.surface.get_size()[1]) # Update size of screen

    # Function to draw the text
    def draw(self, alpha = 255):
        # Get text position based on anchors
        position = (self.surface_size * self.screen_anchor) - (self.text_surface_size * self.text_anchor) + self.position
        self.text_surface.set_alpha(alpha)
        self.surface.blit(self.text_surface, [position.x, position.y]) # Draw text to screen

# Button widget class
class Button():
    def __init__(self,
                surface, # The target surface to draw the button
                command, # The function to run when the button is pressed
                text = "", # The text to display in the button (optional)
                font=FontPaths.NORMAL, # The font in which to display the text (if any)
                font_size=20,
                text_color = (10, 10, 10), # The color of the text (if any)
                image = None, # The image to display in the button (optional)
                position=Vector2(0, 0), # The position offset of the image (pixels)
                anchor=Vector2(0.5, 0.5), # The anchor of the image (0 to 1 screen range)
                dimensions=Vector2(190, 190), # The dimensions of the button (pixels)
                rounding = 1, # The corner rounding of the button
                normal_color=(220, 220, 220), # The normal color of the button
                hover_color=(250, 250, 250), # The color of the button when the hovering over it
                pressed_color=(200, 200, 200), # The color of the button when presed
                hover_scalar = 1.1 # The size growth of the button when hovered over
                ):

        # Create text variables if there is any text
        if len(text) > 0:
            surface_size = Vector2(surface.get_size()[0], surface.get_size()[1])
            self.text = Text(
                surface,
                text=text,
                size=font_size,
                position=surface_size * anchor + position,
                color=text_color,
                screen_anchor=Vector2(0, 0),
                font=font
            )
            self.has_text = True
        else:
            self.has_text = False
        
        # Create image variables if there is an image
        if image is None:
            self.has_image = False
        else:
            self.image = image
            self.has_image = True

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
        self.current_color = [normal_color[0], normal_color[1], normal_color[2]]
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color

        # Set up scalar
        self.hover_scalar = hover_scalar
        self.scalar = 1

        # Set up rect
        self.update_rect()

    # Function for updating the rect (dimensions and position) of the button
    def update_rect(self):
        # Get surface size
        surface_size = Vector2(self.surface.get_size()[0], self.surface.get_size()[1])
        # Get top-left position of button
        position = (surface_size * self.anchor) - (self.dimensions * self.scalar / 2) + self.position
        # Get size of button
        size = self.dimensions * self.scalar
        # Set rect
        self.rect = pygame.Rect(position.x, position.y, size.x, size.y)

    # Function for smoothly fading colors
    def lerp_color(self, color, speed = 0.2):
        self.current_color[0] = lerp(self.current_color[0], color[0], speed)
        self.current_color[1] = lerp(self.current_color[1], color[1], speed)
        self.current_color[2] = lerp(self.current_color[2], color[2], speed)

    # Function called to update the button's state
    def update(self, mouse_position, pressing):
        # Update the rect bounds
        self.update_rect()

        # Check if mouse is over button and act accordingly
        if pygame.Rect.collidepoint(self.rect, mouse_position):

            # If mouse is over button and it is being held down, click
            if pressing == True:
                self.lerp_color(self.pressed_color)
                self.scalar = lerp(self.scalar, 1, 0.2)
                self.command()
            else:
                # Else, the mouse is just hovering over the button
                self.lerp_color(self.hover_color)
                self.scalar = lerp(self.scalar, self.hover_scalar, 0.2)
        else:
            self.lerp_color(self.normal_color)
            self.scalar = lerp(self.scalar, 1, 0.2)

    # Function called to show the button on-screen
    def draw(self):
        # Draw the base rectangle of the button
        pygame.draw.rect(self.surface, self.current_color, self.rect, border_radius=self.rounding)

        # If the button has an image, draw it
        if self.has_image:
            # Find the smaller dimension (width or height) of the button. Make sure the image fits inside
            smaller_dimension = self.rect.height if self.rect.height < self.rect. width else self.rect.width
            scaled_image = pygame.transform.scale(self.image, (smaller_dimension, smaller_dimension))
            image_rect = scaled_image.get_rect()
            image_rect.center = self.rect.center
            self.surface.blit(scaled_image, image_rect)

        # If the button has text, draw it
        if self.has_text:
            self.text.draw()

# Toggle widget class
class Toggle():
    def __init__(self,
                surface, # The target surface to draw the button
                position=Vector2(0, 0), # The position offset of the image (pixels)
                anchor=Vector2(0.5, 0.5), # The anchor of the image (0 to 1 screen range)
                color=(240, 240, 240),
                size=20, # The dimensions of the button (pixels)
                rounding = 1, # The corner rounding of the toggle
                value = False # Value of the toggle (True = Checked, False = Unchecked)
                ):

        self.surface = surface

        # Set up anchor, position, color and dimensions
        self.anchor = anchor
        self.position = position
        self.dimensions = Vector2(size, size)
        self.rounding = rounding
        self.color = color
        
        # Load image
        self.check = pygame.image.load("assets/images/check.png")

        # Set value
        self.value = value

        # Set up rect
        self.update_rect()

    # Function for updating the rect (dimensions and position) of the button
    def update_rect(self):

        # Get surface size
        surface_size = Vector2(self.surface.get_size()[0], self.surface.get_size()[1])
        # Get top-left position of button
        position = (surface_size * self.anchor) - (self.dimensions / 2) + self.position

        # Set rect
        self.rect = pygame.Rect(position.x, position.y, self.dimensions.x, self.dimensions.y)

        # Update image properties
        self.scaled_image = pygame.transform.scale(self.check, [self.dimensions.x, self.dimensions.y])
        self.image_rect = self.scaled_image.get_rect()
        self.image_rect.center = self.rect.center

    # Function called to update the button's state
    def update(self, mouse_position, pressing):

        # Check if mouse is over toggle and pressing
        if pygame.Rect.collidepoint(self.rect, mouse_position) and pressing == True:
                self.value = not self.value

    # Function called to show the button on-screen
    def draw(self):

        # Draw the base rectangle of the button
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=self.rounding)

        # If the toggle is enabled, draw the check
        if self.value:
            self.surface.blit(self.scaled_image, self.image_rect)