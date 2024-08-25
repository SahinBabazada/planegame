import pygame
import math
from torpedo import Torpedo


class Plane:
    def __init__(self, image, y_position, screen, width, height, torpedo_image, flame_images, country_number, wave_amplitude=10, wave_frequency=0.1):
        """
        Initialize the plane with its properties.

        Parameters:
        - image: The plane image.
        - y_position: Initial vertical position.
        - screen: The Pygame screen.
        - width, height: Dimensions of the screen.
        - torpedo_image: Image of the torpedo.
        - flame_images: List of flame images for the torpedo.
        - wave_amplitude: The amplitude of the wavy movement.
        - wave_frequency: The frequency of the wavy movement.
        """
        self.image = image
        self.screen = screen
        self.width = width
        self.height = height
        self.x_position = 120
        self.rect = self.image.get_rect(center=(self.x_position, y_position))
        self.speed = 5
        self.torpedo_image = torpedo_image
        self.flame_images = flame_images
        self.torpedos = []
        self.wave_amplitude = wave_amplitude
        self.wave_frequency = wave_frequency
        self.original_y = y_position 
        self.time = 0
        self.country_number = country_number

    def reset_position(self):
        self.rect.right = 120
        
    def move_left(self, newSpeed = None):
        if newSpeed is None:
            newSpeed = self.speed

        if self.rect.left > 60:
            self.rect.x -= newSpeed

    def move_right(self, newSpeed = None):
        if newSpeed is None:
            newSpeed = self.speed

        if self.rect.right < self.width:
            self.rect.x += newSpeed

    def _apply_wave_movement(self):
        """
        Apply a wavy movement to the plane.
        """
        self.time += 1
        wave_offset = self.wave_amplitude * math.sin(self.wave_frequency * self.time)
        self.rect.y = self.original_y + wave_offset
        
    def shoot_torpedo(self, width=50, height=20, speed=10, direction='right'):
        """
        Shoot a torpedo with customizable parameters.
        
        Parameters:
        - width, height: Size of the torpedo.
        - speed: Movement speed of the torpedo.
        - direction: Direction of the torpedo ('right' or 'left').
        """
        # Determine the starting point of the torpedo
        start_x = self.rect.right if direction == 'right' else self.rect.left
        start_y = self.rect.centery

        # Ensure flame_images is a list of images, not an integer
        if not isinstance(self.flame_images, list):
            print("Error: flame_images is not a list.")
            return

        # Create a new torpedo object and add it to the list
        torpedo = Torpedo(self.torpedo_image, self.flame_images, start_x, start_y, width, height, speed, direction)
        self.torpedos.append(torpedo)


    def update_torpedos(self, screen_width):
        for torpedo in self.torpedos:
            torpedo.move()
            torpedo.draw(self.screen)
            # Remove torpedo if it goes off screen
            if torpedo.is_off_screen(screen_width):
                self.torpedos.remove(torpedo)

    def draw(self):
        """
        Draw the plane and its torpedoes on the screen.
        """
        # Apply wave movement even when idle
        self._apply_wave_movement()

        # Draw the plane
        self.screen.blit(self.image, self.rect)
        
        # Update and draw torpedoes
        self.update_torpedos(self.screen.get_width())
