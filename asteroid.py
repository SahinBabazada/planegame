import pygame
import random
import math

class Asteroid:
    def __init__(self, image_path, screen, width, height, sound_path, asteroid_width=24, asteroid_height=24, rotation_speed=1, move_speed=2):
        """
        Initialize the asteroid with its properties.

        Parameters:
        - image_path: Path to the asteroid image.
        - screen: The Pygame screen to draw on.
        - width, height: Dimensions of the screen.
        - sound_path: Path to the sound file to play on asteroid creation.
        - asteroid_width, asteroid_height: Dimensions of the asteroid image.
        - rotation_speed: The speed at which the asteroid rotates.
        - move_speed: The speed at which the asteroid moves across the screen.
        """
        self.image_original = pygame.image.load(image_path).convert_alpha()  # Load asteroid image
        self.image_original = pygame.transform.scale(self.image_original, (asteroid_width, asteroid_height))  # Resize asteroid image
        self.image = self.image_original
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.rotation_speed = rotation_speed
        self.move_speed = move_speed
        self.angle = 0  # Isnitial rotation angle
        self.rect = self.image.get_rect(center=(random.randint(0, width), 0))  # Initialize at y = 0, random x

        # Randomly choose a direction for diagonal movement
        self.direction_x = random.choice([-1, 1]) * self.move_speed
        self.direction_y = self.move_speed  # Always moving downwards

        # Load and play sound
        self.sound = pygame.mixer.Sound(sound_path)
        self.sound.play()
        
    def stop_sound(self):
        """
        Stop the asteroid sound.
        """
        self.sound.stop()

    def rotate(self):
        """
        Rotate the asteroid around its center.
        """
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        """
        Move the asteroid diagonally across the screen.
        """
        self.rect.x += self.direction_x
        self.rect.y += self.direction_y
        
        # Bounce off the left and right edges of the screen
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.direction_x = -self.direction_x
        
        # Reset asteroid if it goes off the bottom of the screen
        if self.rect.top > self.screen_height:
            self.reset_position()

    def reset_position(self):
        """
        Reset the asteroid to a new random starting position at the top of the screen.
        """
        self.rect.x = random.randint(0, self.screen_width)
        self.rect.y = 0  # Reset to the top of the screen

        # Play sound again when resetting
        self.sound.play()

    def draw(self):
        """
        Draw the asteroid on the screen.
        """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """
        Update the asteroid's rotation and movement.
        """
        self.rotate()
        self.move()
        self.draw()
