import pygame

class Torpedo:
    def __init__(self, image, flame_images, x, y, width=50, height=20, speed=10, direction='right'):
        """
        Initialize the torpedo with its properties.
        
        Parameters:
        - image: The torpedo image.
        - flame_images: List of flame images for animation.
        - x, y: Starting position of the torpedo.
        - width, height: Size of the torpedo.
        - speed: Movement speed of the torpedo.
        - direction: Direction of the torpedo ('right' or 'left').
        """
        # Set torpedo properties
        self.image = pygame.transform.scale(image, (width, height))
        self.flame_images = [pygame.transform.scale(flame, (width // 2, height)) for flame in flame_images]
        self.flame_index = 0
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed if direction == 'right' else -speed
        self.direction = direction

        # Flip image and flames if direction is left
        if direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
            self.flame_images = [pygame.transform.flip(flame, True, False) for flame in self.flame_images]

    def move(self):
        """
        Move the torpedo in the set direction.
        """
        self.rect.x += self.speed

    def draw(self, screen):
        """
        Draw the torpedo and its flame on the screen.
        
        Parameters:
        - screen: The Pygame screen to draw on.
        """
        # Draw the torpedo
        screen.blit(self.image, self.rect)
        
        # Draw the flame behind the torpedo
        flame = self.flame_images[self.flame_index]
        flame_rect = flame.get_rect(center=(self.rect.x - 20 if self.direction == 'right' else self.rect.x + 20, self.rect.centery))
        screen.blit(flame, flame_rect)
        self.flame_index = (self.flame_index + 1) % len(self.flame_images)

    def is_off_screen(self, screen_width):
        """
        Check if the torpedo is off the screen.
        
        Parameters:
        - screen_width: Width of the game screen.
        
        Returns:
        - Boolean indicating whether the torpedo is off-screen.
        """
        return self.rect.left > screen_width or self.rect.right < 0
    
    def check_collision(self, asteroid):
        """
        Check if this torpedo collides with the given asteroid.

        Parameters:
        - asteroid: The asteroid to check collision against.

        Returns:
        - Boolean: True if collision occurs, False otherwise.
        """
        return self.rect.colliderect(asteroid.rect)