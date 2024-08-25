import pygame

class Explosion:
    def __init__(self, x, y, width=100, height=100, fps=60, animation_speed=5, sound_file='sounds/boom.mp3'):
        """
        Initialize the explosion effect.

        Parameters:
        - x, y: Position of the explosion.
        - width, height: Size of the explosion images.
        - fps: Frames per second for the animation.
        - animation_speed: Speed of the animation (higher value means slower animation).
        - sound_file: Path to the sound file to play with the explosion.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fps = fps
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.clock = pygame.time.Clock()
        self.explosion_images = self.load_images()
        self.total_frames = len(self.explosion_images) * self.animation_speed
        self.sound_file = sound_file
        self.sound_played = False
        self.load_sound()

    def load_images(self):
        """
        Load and scale the explosion images.
        
        Returns:
        - List of loaded and scaled images.
        """
        images = [
            pygame.image.load('explosion_images/explosion_01.png'),
            pygame.image.load('explosion_images/explosion_02.png'),
            pygame.image.load('explosion_images/explosion_03.png'),
            pygame.image.load('explosion_images/explosion_04.png'),
            pygame.image.load('explosion_images/explosion_05.png'),
            pygame.image.load('explosion_images/explosion_06.png'),
            pygame.image.load('explosion_images/explosion_07.png'),
            pygame.image.load('explosion_images/explosion_08.png'),
            pygame.image.load('explosion_images/explosion_09.png')
        ]
        # Scale images to the desired width and height
        scaled_images = [pygame.transform.scale(img, (self.width, self.height)) for img in images]
        return scaled_images

    def load_sound(self):
        """
        Load the sound file for the explosion.
        """
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(self.sound_file)

    def play_sound(self):
        """
        Play the explosion sound if not already played.
        """
        if not self.sound_played:
            self.sound.play()
            self.sound_played = True

    def update(self):
        """
        Update the explosion animation frame.
        """
        self.clock.tick(self.fps)
        self.current_frame += 1
        if self.current_frame >= self.total_frames:
            self.current_frame = 0  # Reset animation after it completes
            self.sound_played = False  # Allow sound to play again

    def draw(self, screen):
        """
        Draw the current frame of the explosion on the screen.

        Parameters:
        - screen: The Pygame screen to draw on.
        """
        frame_index = self.current_frame // self.animation_speed
        screen.blit(self.explosion_images[frame_index], (self.x, self.y))
        pygame.display.update()
        self.play_sound()

    def is_finished(self):
        """
        Check if the explosion animation has finished.

        Returns:
        - Boolean indicating whether the animation is complete.
        """
        return self.current_frame == self.total_frames - 1
