import pygame
import random
import sys
import os

pygame.init()

# A bunch of things
data_folder = "data"

background_image = pygame.image.load(os.path.join(data_folder, "background.jpg"))
background_width, background_height = background_image.get_size()
screen = pygame.display.set_mode((1111, 625))
b_speed = 5
b_speed_limit = 75

car_image = pygame.image.load(os.path.join(data_folder, "car.png"))
car_x, car_y = 100, 50
car_width, car_height = car_image.get_size()

cars_image = pygame.image.load(os.path.join(data_folder, "cars.png")) 
cars_x = 600
cars_y = 600
cars_width, cars_height = cars_image.get_size()

font = pygame.font.Font(None, 100)

pygame.display.set_caption('Endless road')

background_x = 0
car_speed = 3
cars_speed = 5

running = True
game_over = False

timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)  # 1000ms = 1s

timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event:
            timer += 1
    # When to increase the speed
    current_time = pygame.time.get_ticks() / 3000
    if current_time % 1 == 0:  
        b_speed += 1
        cars_speed += 1
        car_speed += 1

    # Cars Movement
    cars_x -= cars_speed
  
    # Car Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car_y -= car_speed
    if keys[pygame.K_DOWN]:
        car_y += car_speed
    if keys[pygame.K_RIGHT]:
        car_x += car_speed
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
    # Borders so the car doesn't escape
    if car_x < 0:
        car_x = 0
    elif car_x + car_width > screen.get_width() + 70:
        car_x = screen.get_width() - car_width + 70
    if car_y < -30:
        car_y = -30
    elif car_y + car_height > screen.get_height() - 10:
        car_y = screen.get_height() - car_height - 10

    # Detect when to spawn new cars
    if cars_x < -cars_width:
        cars_x = screen.get_width()
        cars_y = random.randint(0, 500)

    # Detect Collision
    car_rect = pygame.Rect(car_x + 20, car_y + 20, car_width - 40, car_height - 40)
    cars_rect = pygame.Rect(cars_x + 20, cars_y + 20, cars_width - 40, cars_height - 40)
    if car_rect.colliderect(cars_rect):
        running = False
        game_over = True

    if running:
        screen.fill((0, 0, 0))  

        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + background_width, 0))

        background_x -= b_speed
        if background_x < -background_width: 
            background_x = 0
        elif background_x > background_width:
            background_x = background_width

        screen.blit(car_image, (car_x, car_y)) 
        screen.blit(cars_image, (cars_x, cars_y))

        # Display the timer
        timer_text = font.render("Time: " + str(timer) + "s", True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))

        pygame.display.flip()
    else:
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds
        pygame.quit()
        sys.exit()