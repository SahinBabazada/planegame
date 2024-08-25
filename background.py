import pygame


class Background:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.sky_color = pygame.image.load('background_images/sky_color.png').convert()
        self.sun = pygame.image.load('background_images/sun.png').convert_alpha()
        self.farground_cloud_1 = pygame.image.load('background_images/farground_cloud_1.png').convert_alpha()
        self.farground_cloud_2 = pygame.image.load('background_images/farground_cloud_2.png').convert_alpha()
        self.mid_ground_cloud_1 = pygame.image.load('background_images/mid_ground_cloud_1.png').convert_alpha()
        self.mid_ground_cloud_2 = pygame.image.load('background_images/mid_ground_cloud_2.png').convert_alpha()
        self.midground_mountains = pygame.image.load('background_images/midground_mountains.png').convert_alpha()
        self.foreground_mountains = pygame.image.load('background_images/foreground_mountains.png').convert_alpha()
        self.speed_fg_clouds = 0.5
        self.speed_mid_clouds = 0.3
        self.speed_mountains = 0.1
        self.fg_clouds_scroll = 0
        self.mid_clouds_scroll = 0
        self.mountain_scroll = 0
        self.width = width
        self.height = height

    def draw_repeating_background(self, image):
        image_width = image.get_width()
        image_height = image.get_height()
        for y in range(0, self.height, image_height):
            for x in range(0, self.width, image_width):
                self.screen.blit(image, (x, y))

    def draw_scrolling_layer(self, image, y, scroll, speed):
        image_width = image.get_width()
        scroll -= speed
        self.screen.blit(image, (scroll, y))
        self.screen.blit(image, (scroll + image_width, y))
        if scroll <= -image_width:
            scroll = 0
        return scroll

    def draw(self):
        self.draw_repeating_background(self.sky_color)
        self.screen.blit(self.sun, (self.width // 2 - self.sun.get_width() // 2, 50))
        self.fg_clouds_scroll = self.draw_scrolling_layer(self.farground_cloud_1, 50, self.fg_clouds_scroll, self.speed_fg_clouds)
        self.fg_clouds_scroll = self.draw_scrolling_layer(self.farground_cloud_2, 80, self.fg_clouds_scroll, self.speed_fg_clouds)
        self.mid_clouds_scroll = self.draw_scrolling_layer(self.mid_ground_cloud_1, 150, self.mid_clouds_scroll, self.speed_mid_clouds)
        self.mid_clouds_scroll = self.draw_scrolling_layer(self.mid_ground_cloud_2, 200, self.mid_clouds_scroll, self.speed_mid_clouds)
        self.mountain_scroll = self.draw_scrolling_layer(self.midground_mountains, self.height - self.midground_mountains.get_height(), self.mountain_scroll, self.speed_mountains)
        self.mountain_scroll = self.draw_scrolling_layer(self.foreground_mountains, self.height - self.foreground_mountains.get_height(), self.mountain_scroll, self.speed_mountains)