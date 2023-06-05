import pygame
import math
from snake import snake

pygame.init()

x_max = 600
y_max = 600
length_squares = 5
length_lines = 2
square_size = math.floor(x_max / length_squares)

size = (x_max, y_max)
screen = pygame.display.set_mode(size)
running = True

snk = snake()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(snk.get_length()):
        x = square_size*(snk.body[i][0])
        y = square_size*(snk.body[i][1])
        pygame.draw.rect(screen, 'green', [x, y, square_size, square_size])

    for i in range(1,9):
        pygame.draw.line(screen, 'white', [square_size*(i), 0], [square_size*(i), y_max], length_lines)
        pygame.draw.line(screen, 'white', [0, square_size*(i)], [x_max, square_size*(i)], length_lines)

    pygame.display.flip()