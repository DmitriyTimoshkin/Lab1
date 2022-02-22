import numpy as np
import pygame
import sys

run = True

FPS = 12000000000000000000000000000

side = 1
WIDTH = 1000
HEIGHT = 1000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 225)

pygame.init()
pygame.display.set_caption('Перколяция')
screen = pygame.display.set_mode((WIDTH * side, HEIGHT * side))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

par = 1
flag = True


def temp(param):
    return np.random.standard_gamma(param, size=(WIDTH, HEIGHT)) #np.random.randint(param, size=(WIDTH, HEIGHT))


def workWithArr(arr):
    global flag
    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    if pygame.mouse.get_focused():
        pygame.draw.rect(screen, RED, ((pos[0] - side/2) - (pos[0] - side/2) %
                         side, (pos[1] - side/2) - (pos[1] - side/2) % side, side, side))

    if pressed[0]:
        flag = True
        arr[int((pos[1] - side/2) - (pos[1] - side/2) % side) // side,
            int((pos[0] - side/2) - (pos[0] - side/2) % side) // side] = 1
    elif pressed[1]:
        flag = True
        arr = temp(par)
    elif pressed[2]:
        flag = True
        arr[int((pos[1] - side/2) - (pos[1] - side/2) % side) // side,
            int((pos[0] - side/2) - (pos[0] - side/2) % side) // side] = 0

    return arr


def main():
    arr = temp(par)
    global flag
    while run:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit(0)

        if (flag):
            flag = False
            screen.fill(WHITE)
            for i, y in enumerate(arr):
                for j, x in enumerate(y):
                    if x < 0.59:
                        pygame.draw.rect(
                            screen, (0, 0, 0), (j*side, i*side, side, side))

        arr = workWithArr(arr)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
