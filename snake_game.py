import pygame
import math

pygame.init()

x_max = 600
y_max = 600
length_squares = 5
square_size = math.floor(x_max / length_squares)

size = (x_max, y_max)
screen = pygame.display.set_mode(size)
running = False

while not running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True

    for i in range(9):
        pygame.draw.line(screen, 'white', [square_size*(1+i), 0], [square_size*(1+i), y_max], 2)
        pygame.draw.line(screen, 'white', [0, square_size*(1+i)], [x_max, square_size*(1+i)], 2)

    pygame.display.flip()