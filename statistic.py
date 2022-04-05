# -*- coding: utf-8 -*-
import numpy as np
import secrets
import csv


WIDTH = 30
HEIGHT = 30
FPS = 12000000000000000000000000


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
            if (wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y][x - 1]) < wae[y][x - 1]):
                wae[y][x - 1] = wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y][x - 1])
        if x + 1 <= WIDTH - 1 and proi_wae[y][x + 1] == 0:
            if (wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y][x + 1]) < wae[y][x + 1]):
                wae[y][x + 1] = wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y][x + 1])
        if y - 1 >= 0 and proi_wae[y - 1][x] == 0:
            if (wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y - 1][x]) < wae[y - 1][x]):
                wae[y - 1][x] = wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y - 1][x])
        if y + 1 <= WIDTH - 1 and proi_wae[y + 1][x] == 0:
            if (wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y + 1][x]) < wae[y + 1][x]):
                wae[y + 1][x] = wae[y][x] + (WIDTH ** 2 + 1) ** (1 - arr[y + 1][x])
        proi_wae[y][x] = FPS
        cumzone = np.cumsum(proi_wae[WIDTH - 1])
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


def init():
    arr = np.ndarray((WIDTH, HEIGHT))
    param = 10  # менять вероятность от 5 до 95 с шагом 5
    for i, e in enumerate(arr):
        for j, ee in enumerate(arr[i]):
            arr[i][j] = secrets.randbelow(100)  # random.randint(0, 99) #
            if arr[i][j] > param:
                arr[i][j] = 0
            else:
                arr[i][j] = 1
    return arr


for j in range(500):
    arr = init()
    per = deikstra(arr)
    lenth = len(per)
    red = 0
    for i in range(lenth):
        if arr[per[i][0]][per[i][1]] == 0:
            red += 1
    i = 0
    count = []
    cls = 0
    while i < lenth:
        if arr[per[i][0]][per[i][1]] == 1:
            i += 1
        elif arr[per[i][0]][per[i][1]] == 0:
            while i < lenth and arr[per[i][0]][per[i][1]] == 0:
                cls += 1
                i += 1
            count.append(cls)
            cls = 0
    avg = 0
    i = 0
    while i < len(count):
        avg += count[i]
        i += 1
    avg = avg/len(count)
    with open('30_010_l_m_r.csv', mode='+a', encoding='utf-8') as w_file: # менять название на <размер матрицы>_<вероятность>_l_m_r.csv
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow([lenth, str(int(avg)) + ',' + str(int(round(avg % 1, 5)*100000)), red])