import pygame
import random
import math

class RobotBall:
    def __init__(self, screen, images_folder, width, height, robotball_width=24, robotball_height=24, speed=3, wave_amplitude=5, wave_frequency=0.05):
        """
        Initialize the robot ball with animation and movement properties.

        Parameters:
        - screen: The Pygame screen to draw on.
        - images_folder: Folder path where robot ball images are stored.
        - width, height: Screen dimensions.
        - robotball_width, robotball_height: Size of the robot ball.
        - speed: Movement speed towards planes.
        - wave_amplitude: Amplitude for the wavy movement.
        - wave_frequency: Frequency for the wavy movement.
        """
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.robotball_width = robotball_width
        self.robotball_height = robotball_height
        self.speed = speed
        self.wave_amplitude = wave_amplitude
        self.wave_frequency = wave_frequency
        self.images = self.load_images(images_folder)
        self.image_index = 0
        self.rect = self.images[0].get_rect()
        self.rect.x = self.screen_width  # Start from the right edge of the screen
        self.rect.y = random.randint(0, self.screen_height - robotball_height)  # Random y position
        self.direction_x = -1  # Move towards the left initially
        self.direction_y = random.choice([-1, 1])  # Randomly choose to move up or down
        self.idle_counter = 0

    def load_images(self, folder):
        """
        Load the animation images from the specified folder.

        Returns:
        - List of loaded images.
        """
        images = []
        for i in range(16):
            img_path = f"{folder}/skeleton-animation_{i:02d}.png"
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (self.robotball_width, self.robotball_height))
            images.append(img)
        return images

    def move(self):
        """
        Move the robot ball in a wavy pattern towards the planes.
        """
        # Update x position
        self.rect.x += self.direction_x * self.speed
        
        # Update y position with wavy movement
        self.rect.y += self.direction_y * int(self.wave_amplitude * math.sin(self.rect.x * self.wave_frequency))
        
        # Reverse direction if robot ball goes off screen vertically
        if self.rect.top < 0 or self.rect.bottom > self.screen_height:
            self.direction_y *= -1

    def animate(self):
        """
        Update the animation frame of the robot ball.
        """
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0

    def draw(self):
        """
        Draw the current frame of the robot ball on the screen.
        """
        self.screen.blit(self.images[self.image_index], self.rect)

    def update(self):
        """
        Update the robot ball's movement and animation.
        """
        self.move()
        self.animate()
        self.draw()

    def check_collision_with_plane(self, plane):
        """
        Check if the robot ball collides with a plane.

        Parameters:
        - plane: The plane to check collision against.

        Returns:
        - Boolean: True if collision occurs, False otherwise.
        """
        return self.rect.colliderect(plane.rect)

    def check_collision_with_torpedo(self, torpedo):
        """
        Check if the robot ball collides with a torpedo.

        Parameters:
        - torpedo: The torpedo to check collision against.

        Returns:
        - Boolean: True if collision occurs, False otherwise.
        """
        return self.rect.colliderect(torpedo.rect)

    def is_off_screen(self):
        """
        Check if the robot ball is off the screen.

        Returns:
        - Boolean: True if off screen, False otherwise.
        """
        return self.rect.right < 0  # If the robot ball moves off the left side of the screen
