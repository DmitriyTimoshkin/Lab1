# -*- coding: utf-8 -*-

# import random
from pprint import pprint

import numpy as np
import secrets
import pygame
import sys
import time

run = True

FPS = 120000000000000000000000000000
fps = 60

side = 20
WIDTH = 20
HEIGHT = 20

WHITE = (255, 255, 255)
GRAY = (175, 175, 175)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 225)

pygame.init()
pygame.display.set_caption('Перколяция')
screen = pygame.display.set_mode((WIDTH * side, HEIGHT * side))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


def workWithArr(arr):
    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    if pygame.mouse.get_focused():
        pygame.draw.rect(screen, RED, ((pos[0] - side / 2) - (pos[0] - side / 2) %
                                       side, (pos[1] - side / 2) - (pos[1] - side / 2) % side, side, side))

    if pressed[0]:
        arr[int((pos[1] - side / 2) - (pos[1] - side / 2) % side) // side,
            int((pos[0] - side / 2) - (pos[0] - side / 2) % side) // side] = 1
    elif pressed[2]:
        arr[int((pos[1] - side / 2) - (pos[1] - side / 2) % side) // side,
            int((pos[0] - side / 2) - (pos[0] - side / 2) % side) // side] = 0

    return arr


def klust_count(arr):
    klust_arr = []
    total = []
    kurwa = np.zeros((WIDTH, WIDTH))
    for i in range(WIDTH):
        for j in range(WIDTH):
            if arr[i][j] == 0 and kurwa[i][j] == 0:
                kurwa[i][j] = 1
            elif arr[i][j] == 1 and kurwa[i][j] == 0:
                pass


def deikstra(arr):
    wae = np.full((WIDTH, WIDTH), FPS)  # do you know de wae
    proi_wae = np.zeros((WIDTH, WIDTH))  # you know de wae
    for i in range(WIDTH):
        wae[0][i] = 0
    cumzone = np.cumsum(proi_wae[WIDTH - 1])
    while cumzone[-1] < (WIDTH * FPS) * 0.95:
        prom_arr = wae + proi_wae
        a = np.argmin(prom_arr)
        y = a // WIDTH
        x = a % WIDTH

        if x - 1 >= 0 and proi_wae[y][x - 1] == 0:
            if wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y][x - 1]) < wae[y][x - 1]:
                wae[y][x - 1] = wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y][x - 1])

        if x + 1 <= WIDTH - 1 and proi_wae[y][x + 1] == 0:
            if wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y][x + 1]) < wae[y][x + 1]:
                wae[y][x + 1] = wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y][x + 1])

        if y - 1 >= 0 and proi_wae[y - 1][x] == 0:
            if wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y - 1][x]) < wae[y - 1][x]:
                wae[y - 1][x] = wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y - 1][x])

        if y + 1 <= WIDTH - 1 and proi_wae[y + 1][x] == 0:
            if wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y + 1][x]) < wae[y + 1][x]:
                wae[y + 1][x] = wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y + 1][x])

        proi_wae[y][x] = FPS
        cumzone = np.cumsum(proi_wae[WIDTH - 1])
    # print(wae)
    x = np.argmin(wae[WIDTH - 1])
    y = WIDTH - 1
    omega_wae = []
    omega_wae.append([y, x])
    while y != 0:
        if x - 1 >= 0:
            if wae[y][x - 1] == wae[y][x] - (WIDTH ** 2 + 1) ** (1 - arr[y][x]):
                x = x - 1
                omega_wae.append([y, x])
        if x + 1 <= WIDTH - 1:
            if wae[y][x + 1] == wae[y][x] - (WIDTH ** 2 + 1) ** (1 - arr[y][x]):
                x = x + 1
                omega_wae.append([y, x])
        if y - 1 >= 0:
            if wae[y - 1][x] == wae[y][x] - (WIDTH ** 2 + 1) ** (1 - arr[y][x]):
                y = y - 1
                omega_wae.append([y, x])
        if y + 1 <= WIDTH - 1:
            if wae[y + 1][x] == wae[y][x] - (WIDTH ** 2 + 1) ** (1 - arr[y][x]):
                y = y + 1
                omega_wae.append([y, x])

    mass = 0
    for a in omega_wae[:-2]:
        mass = mass + (WIDTH ** 2 + 1) ** (1 - arr[a[0]][a[1]])
    return omega_wae


class Cluster:
    """docstring"""

    def __init__(self, number, cells):
        """Constructor"""
        self.number = number
        self.cells = cells

    # Добавление всех точек из кластера other
    def __add__(self, other):
        self.cells = self.cells + other.cells
        return self.cells

    def __repr__(self):
        return "{" + str(self.number) + ", " + str(self.cells) + "}"


def kopelman(arr):
    mat = arr  # Создает матрицу копию

    clusters = []

    number = 1
    for i, string in enumerate(mat):
        for j, val in enumerate(string):

            if mat[i][j] == 1:  # Проверяем, что клетка иммеет значение 1 (чёрная)

                # Общий случай есть клетка сверху и с лева чёрные
                if i != 0 and mat[i-1][j] > 0:                  # Проверяем есть ли верхняя клетка и черная ли она

                    if j != 0 and mat[i][j-1] > 0:              # Проверяем есть ли левая клетка и черная ли она

                        up_number = int(mat[i-1][j])                 # Номер кластера верхний клетки
                        clusters.append(Cluster(up_number, [(i, j)]))
                        mat[i][j] = up_number

                        if mat[i][j-1] != up_number:
                            for element in clusters:
                                if element.number == mat[i][j-1]:
                                    element.number = up_number

                            for n, string2 in enumerate(mat):
                                for m, val2 in enumerate(string):
                                    if mat[n][m] == mat[i][j-1]:
                                        mat[n][m] = up_number

                    # Проверяем белая левая, чёрная верхняя ? (да)
                    if mat[i][j - 1] == 0:
                        up_number = int(mat[i - 1][j])  # Номер кластера верхний клетки
                        clusters.append(Cluster(up_number, [(i, j)]))
                        mat[i][j] = up_number

                # Проверяем белая верхняя, чёрная левая ? (да)
                if i != 0 and mat[i - 1][j] == 0:
                    if j != 0 and mat[i][j - 1] > 0:
                        left_number = int(mat[i][j-1])  # Номер кластера левой клетки
                        clusters.append(Cluster(left_number, [(i, j)]))
                        mat[i][j] = left_number

                # Нет чёрных клеток сверху и слева
                if i != 0 and mat[i-1][j] == 0:
                    if j != 0 and mat[i][j - 1] == 0:
                        clusters.append(Cluster(number, [(i, j)]))
                        mat[i][j] = number

                if i == 0:
                    # Частный случай первая ячейка таблицы
                    if j == 0:
                        clusters.append(Cluster(number, [(i, j)]))
                        mat[i][j] = number
                    # Частный случай первая строка таблицы
                    elif j > 0:
                        left_number = int(mat[i][j - 1])  # Номер кластера левой клетки
                        clusters.append(Cluster(left_number, [(i, j)]))
                        mat[i][j] = left_number

                # Частный случай первый столбец таблицы
                elif i > 0 and j == 0:
                    up_number = int(mat[i - 1][j])  # Номер кластера верхний клетки
                    clusters.append(Cluster(up_number, [(i, j)]))
                    mat[i][j] = up_number

                number += 1

    pprint(clusters)


def init():
    arr = np.ndarray((WIDTH, HEIGHT))
    param = 59  # 59
    for i, e in enumerate(arr):
        for j, ee in enumerate(arr[i]):
            arr[i][j] = secrets.randbelow(100)  # random.randint(0, 99) #  
            if arr[i][j] > param:
                arr[i][j] = 0
            else:
                arr[i][j] = 1
    return arr


def main():
    arr = init()
    arr2d2 = np.zeros(shape=(WIDTH, HEIGHT))

    sttime = time.time()

    f = False
    per = deikstra(arr)
    print(arr)
    kopelman(arr)

    while run:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit(0)

        screen.fill(WHITE)

        for i, y in enumerate(arr):
            for j, x in enumerate(y):
                if x:

                    pygame.draw.rect(
                        screen, BLACK, (j * side, i * side, side, side))
                else:
                    arr2d2[i][j] = 1

        arr = workWithArr(arr)
        crtime = time.time()
        if crtime - sttime > 1:
            per = deikstra(arr)
            # f = True

        for i, el in enumerate(per):
            if not arr[el[0], el[1]]:
                pygame.draw.rect(screen, (255, 100, 0), (el[1] * side, el[0] * side, side, side))
            else:
                pygame.draw.rect(screen, (255, 255, 0), (el[1] * side, el[0] * side, side, side))

        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()
