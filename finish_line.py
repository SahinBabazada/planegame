import pygame


class FinishLine:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.image = pygame.image.load('background_images/finish.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, height))
        self.x = self.width - self.image.get_width()

    def draw(self):
        self.screen.blit(self.image, (self.x, 0))