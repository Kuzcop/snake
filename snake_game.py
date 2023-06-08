import pygame
import math
import random
from snake import snake

pygame.init()
clock = pygame.time.Clock()

x_max = 600
y_max = 600
length_squares = 20
line_width = 2
square_size = math.floor(x_max / length_squares)

apple_coordinate = (random.randint(1, length_squares - 1), random.randint(1, length_squares - 1))

size = (x_max, y_max)
screen = pygame.display.set_mode(size)

snk = snake()

still_running = True

while still_running:

    pygame.time.delay(50)  
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_running = False

    snk.move()

    curr_head_pos = snk.get_head()

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] and not (snk.get_dir() == 'down')) or snk.get_dir() == 'up':
        snk.set_dir('up')
        snk.set_head((curr_head_pos[0], curr_head_pos[1] - 1))
    if (keys[pygame.K_DOWN] and not (snk.get_dir() == 'up')) or snk.get_dir() == 'down':
        snk.set_dir('down')
        snk.set_head((curr_head_pos[0], curr_head_pos[1] + 1))
    if (keys[pygame.K_LEFT] and not (snk.get_dir() == 'right')) or snk.get_dir() == 'left':
        snk.set_dir('left')
        snk.set_head((curr_head_pos[0] - 1, curr_head_pos[1]))
    if (keys[pygame.K_RIGHT] and not (snk.get_dir() == 'left')) or snk.get_dir() == 'right':
        snk.set_dir('right')
        snk.set_head((curr_head_pos[0] + 1, curr_head_pos[1]))

    curr_head_pos = snk.get_head()

    # Check to see if snake head is going to hit a wall, end game if true
    if curr_head_pos[0] < 0 or curr_head_pos[0] == length_squares or curr_head_pos[1] < 0 or curr_head_pos[1] == length_squares:
        snk.reset()
        #break

    if curr_head_pos == apple_coordinate:
        snk.grow_body()
        while True:
            apple_coordinate = (random.randint(0, length_squares - 1), random.randint(0, length_squares - 1))
            if not snk.is_new_apple_in_body(apple_coordinate):
                break

    if snk.eat_body():
        snk.reset()
        #break


    # Render
    screen.fill("black")

    # Drawing apple
    x = square_size*apple_coordinate[0]
    y = square_size*apple_coordinate[1]
    pygame.draw.rect(screen, 'red', [x, y, square_size, square_size])

    # Drawing snake
    for i in range(snk.get_length()):
        x = square_size*(snk.body[i][0][0])
        y = square_size*(snk.body[i][0][1])
        pygame.draw.rect(screen, 'green', [x, y, square_size, square_size])

    # Drawing grid play area
    for i in range(1,length_squares):
        pygame.draw.line(screen, 'white', [square_size*(i), 0], [square_size*(i), y_max], line_width)
        pygame.draw.line(screen, 'white', [0, square_size*(i)], [x_max, square_size*(i)], line_width)

    pygame.display.flip()

pygame.quit()