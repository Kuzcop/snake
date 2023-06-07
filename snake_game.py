import pygame
import math
from snake import snake

pygame.init()
clock = pygame.time.Clock()

x_max = 600
y_max = 600
length_squares = 10
length_lines = 2
square_size = math.floor(x_max / length_squares)

apple_coordinate = (2, 2)

size = (x_max, y_max)
screen = pygame.display.set_mode(size)
running = True

snk = snake()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    old_curr_pos = snk.get_head()

    snk.update_body()

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] and not (snk.get_dir() == 'down')) or snk.get_dir() == 'up':
        snk.set_dir('up')
        snk.set_head((old_curr_pos[0], old_curr_pos[1] - 1))
    if (keys[pygame.K_DOWN] and not (snk.get_dir() == 'up')) or snk.get_dir() == 'down':
        snk.set_dir('down')
        snk.set_head((old_curr_pos[0], old_curr_pos[1] + 1))
    if (keys[pygame.K_LEFT] and not (snk.get_dir() == 'right')) or snk.get_dir() == 'left':
        snk.set_dir('left')
        snk.set_head((old_curr_pos[0] - 1, old_curr_pos[1]))
    if (keys[pygame.K_RIGHT] and not (snk.get_dir() == 'left')) or snk.get_dir() == 'right':
        snk.set_dir('right')
        snk.set_head((old_curr_pos[0] + 1, old_curr_pos[1]))

    new_curr_pos = snk.get_head()

    # Check to see if snake head is going to hit a wall, end game if true
    if new_curr_pos[0] < 0 or new_curr_pos[0] == length_squares or new_curr_pos[1] < 0 or new_curr_pos[1] == length_squares:
        running = False

    # Render
    screen.fill("black")

    # Drawing apple
    #pygame.draw.rect(screen, 'apple', [x, y, square_size, square_size])

    # Drawing snake
    for i in range(snk.get_length()):
        x = square_size*(snk.body[i][0])
        y = square_size*(snk.body[i][1])
        pygame.draw.rect(screen, 'green', [x, y, square_size, square_size])

    # Drawing grid play area
    for i in range(1,length_squares):
        pygame.draw.line(screen, 'white', [square_size*(i), 0], [square_size*(i), y_max], length_lines)
        pygame.draw.line(screen, 'white', [0, square_size*(i)], [x_max, square_size*(i)], length_lines)


    pygame.display.flip()

    clock.tick(10)  # limits FPS to 60

pygame.quit()