import random
import pygame
import sys
from asteroid import Asteroid
from background import Background
from country import Country
from explosion import Explosion
from finish_line import FinishLine
from plane import Plane
from robotball import RobotBall
from tiktokservice import TikTokService



pygame.init()

WIDTH, HEIGHT = 800, 600
PLANE_HEIGHT = HEIGHT // 4
trophy_icon_path = 'images/trophy.png'

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Scene with Parallax Effect, Planes, and Finish Line")

plane_images = [
    pygame.transform.scale(pygame.image.load('plane_images/plane_1_yellow.png').convert_alpha(), (100, 50)),
    pygame.transform.scale(pygame.image.load('plane_images/plane_1_blue.png').convert_alpha(), (100, 50)),
    pygame.transform.scale(pygame.image.load('plane_images/plane_1_pink.png').convert_alpha(), (100, 50)),
    pygame.transform.scale(pygame.image.load('plane_images/plane_1_red.png').convert_alpha(), (100, 50)),
]

country_images = [
    pygame.transform.scale(pygame.image.load('countries_images/azerbaijan.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('countries_images/armenia.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('countries_images/russia.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('countries_images/ukraine.png').convert_alpha(), (50, 50)),
]

torpedo_image = pygame.image.load('torpedo/torpedo.png').convert_alpha()
flame_images = [
    pygame.image.load('torpedo/torpedo_flame.png').convert_alpha(),
    pygame.image.load('torpedo/torpedo_flame_1.png').convert_alpha(),
    pygame.image.load('torpedo/torpedo_flame_2.png').convert_alpha()
]

background = Background(screen=screen, width=WIDTH, height=HEIGHT)

planes = [
    Plane(plane_images[0], PLANE_HEIGHT // 2, screen, WIDTH, HEIGHT, torpedo_image, flame_images, 1, wave_amplitude=15, wave_frequency=0.05),
    Plane(plane_images[1], PLANE_HEIGHT + PLANE_HEIGHT // 2, screen, WIDTH, HEIGHT, torpedo_image, flame_images, 2, wave_amplitude=10, wave_frequency=0.1),
    Plane(plane_images[2], 2 * PLANE_HEIGHT + PLANE_HEIGHT // 2, screen, WIDTH, HEIGHT, torpedo_image, flame_images, 3, wave_amplitude=12, wave_frequency=0.08),
    Plane(plane_images[3], 3 * PLANE_HEIGHT + PLANE_HEIGHT // 2, screen, WIDTH, HEIGHT, torpedo_image, flame_images, 4, wave_amplitude=20, wave_frequency=0.04),
]

countries = [
    Country(1, country_images[0], screen, 10, PLANE_HEIGHT // 2 - country_images[0].get_height() // 2, trophy_icon_path),
    Country(2, country_images[1], screen, 10, PLANE_HEIGHT + PLANE_HEIGHT // 2 - country_images[1].get_height() // 2, trophy_icon_path),
    Country(3, country_images[2], screen, 10, 2 * PLANE_HEIGHT + PLANE_HEIGHT // 2 - country_images[2].get_height() // 2, trophy_icon_path),
    Country(4, country_images[3], screen, 10, 3 * PLANE_HEIGHT + PLANE_HEIGHT // 2 - country_images[3].get_height() // 2, trophy_icon_path),
]

tiktok_service = TikTokService(planes, username="@pandaaagame")
tiktok_service.start_service()

asteroid_image_path = 'images/asteroid.png'
asteroid_sound_path = 'sounds/asteroid.mp3'

robotballs = []

last_robotball_time = pygame.time.get_ticks()
robotball_creation_delay = random.randint(5000, 10000)

finish_line = FinishLine(screen=screen, width=WIDTH, height=HEIGHT)

asteroids = []
explosions = []

# Timer settings for random asteroid creation
last_asteroid_time = pygame.time.get_ticks()
asteroid_creation_delay = random.randint(5000, 15000)  # Random delay between 5 to 15 seconds

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                planes[0].shoot_torpedo()  # Plane 1 shoots torpedo
            elif event.key == pygame.K_f:
                planes[1].shoot_torpedo(width=60, height=30, speed=15, direction='left')  # Plane 2 shoots torpedo

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        planes[0].move_left()
    if keys[pygame.K_d]:
        planes[0].move_right()
    if keys[pygame.K_j]:
        planes[1].move_left()
    if keys[pygame.K_l]:
        planes[1].move_right()
    if keys[pygame.K_LEFT]:
        planes[2].move_left()
    if keys[pygame.K_RIGHT]:
        planes[2].move_right()
    if keys[pygame.K_KP4]:
        planes[3].move_left()
    if keys[pygame.K_KP6]:
        planes[3].move_right()

    current_time = pygame.time.get_ticks()
    if current_time - last_asteroid_time > asteroid_creation_delay:
        new_asteroid = Asteroid(asteroid_image_path, screen, WIDTH, HEIGHT, asteroid_sound_path)
        asteroids.append(new_asteroid)
        
        last_asteroid_time = current_time
        asteroid_creation_delay = random.randint(5000, 15000)

    if current_time - last_robotball_time > robotball_creation_delay:
        new_robotball = RobotBall(screen, 'robotball', WIDTH, HEIGHT)
        robotballs.append(new_robotball)
        
        last_robotball_time = current_time
        robotball_creation_delay = random.randint(5000, 10000)

    # Check for collisions between torpedoes and asteroids
    for plane in planes:
        for torpedo in plane.torpedos:
            for asteroid in asteroids:
                if torpedo.check_collision(asteroid):
                    explosion = Explosion(asteroid.rect.centerx - 15, asteroid.rect.centery - 15)
                    explosions.append(explosion)
                    asteroid.stop_sound()
                    asteroids.remove(asteroid)
                    plane.torpedos.remove(torpedo)
                    break

    for plane in planes:
        for asteroid in asteroids:
            if plane.rect.colliderect(asteroid.rect):
                plane.move_left(newSpeed=15)
                asteroid.stop_sound()
                asteroids.remove(asteroid)
                break

    for robotball in robotballs:
        for plane in planes:
            if robotball.check_collision_with_plane(plane):
                explosion = Explosion(robotball.rect.centerx - 15, robotball.rect.centery - 15)
                explosions.append(explosion)
                plane.move_left(newSpeed=10)  # Move the plane slightly left upon collision
                robotballs.remove(robotball)
                break
    
        for plane in planes:
            for torpedo in plane.torpedos:
                if robotball.check_collision_with_torpedo(torpedo):
                    explosion = Explosion(robotball.rect.centerx - 15, robotball.rect.centery - 15)
                    explosions.append(explosion)
                    robotballs.remove(robotball)
                    plane.torpedos.remove(torpedo)
                    break

    # Check if any plane crosses the finish line
    for plane, country in zip(planes, countries):
        if plane.rect.right >= finish_line.x:
            country.add_trophy()  # Increment the country's trophy count
            plane.reset_position()  # Reset the plane's position (implement this method if needed)

    # Draw all elements
    background.draw()
    for country in countries:
        country.draw()  # Draw each country individually
    finish_line.draw()
    for plane in planes:
        plane.draw()
    for asteroid in asteroids:
        asteroid.update()  # Update and draw each asteroid
    for robotball in robotballs:
        robotball.update()  # Update and draw each robotball
    for explosion in explosions:
        explosion.update()
        explosion.draw(screen)
        if explosion.is_finished():
            explosions.remove(explosion)  # Remove explosion if it has finished

    pygame.display.flip()
    clock.tick(60)
