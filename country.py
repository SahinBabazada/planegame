import pygame

class Country:
    def __init__(self, country_number, image, screen, x, y, trophy_icon_path, font_size=24, font_color=(0, 0, 0)):
        """
        Initialize a single country display with its image and text.

        Parameters:
        - image: The country flag image.
        - screen: The Pygame screen to draw on.
        - x, y: Position coordinates of the country.
        - trophy_icon_path: Path to the trophy icon image.
        - font_size: Font size for the text.
        - font_color: Color of the text (default is black).
        """
        self.country_number = country_number
        self.image = image
        self.screen = screen
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(None, font_size)
        self.font_color = font_color
        self.trophy_count = 0  # Initialize the trophy count to 0
        self.trophy_icon = pygame.image.load(trophy_icon_path).convert_alpha()  # Load trophy icon
        self.trophy_icon = pygame.transform.scale(self.trophy_icon, (15, 15))  # Resize trophy icon if needed

    def draw(self):
        """
        Draw the country and its corresponding texts on the screen.
        """
        # Draw the country image
        self.screen.blit(self.image, (self.x, self.y))
        
        # Draw the country number next to the flag
        country_number_text = f"{self.country_number}"
        country_number_surface = self.font.render(country_number_text, True, self.font_color)
        self.screen.blit(country_number_surface, ((self.x + self.image.get_width()) / 2, self.y + self.image.get_height() // 4 + 10))

        # Draw the trophy icon below the flag
        trophy_icon_x = self.x  + 10
        trophy_icon_y = self.y + self.image.get_height() + 5
        self.screen.blit(self.trophy_icon, (trophy_icon_x, trophy_icon_y))

        # Draw the number of trophies next to the trophy icon
        trophy_text = str(self.trophy_count)
        trophy_surface = self.font.render(trophy_text, True, self.font_color)
        self.screen.blit(trophy_surface, (trophy_icon_x + self.trophy_icon.get_width() + 5, trophy_icon_y))

    def update_trophy_count(self, trophy_count):
        """
        Update the trophy count for this country.

        Parameters:
        - trophy_count: New trophy count to set.
        """
        self.trophy_count = trophy_count

    def add_trophy(self):
        """
        Update the trophy count for this country.

        Parameters:
        - trophy_count: New trophy count to set.
        """
        self.trophy_count += 1
