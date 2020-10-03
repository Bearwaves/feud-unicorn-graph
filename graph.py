#! /usr/bin/env python3

import time
import requests
import unicornhat as unicorn

RED = [203, 42, 40]
GREEN = [0, 102, 51]
BLUE = [76, 142, 204]
YELLOW = [246, 176, 78]


def get_player_count():
    try:
        r = requests.get(
                "https://crossbow.feud.bearwaves.com:1323/status/playersOnline"
        )
        if r.status_code is not 200:
            r.raise_for_error()
        return r.json()['playersOnline'], True
    except requests.HTTPError:
        return 0, False


def set_colour(x, y, colour):
    unicorn.set_pixel(x, y, colour[0], colour[1], colour[2])


def draw_graph(graph):
    for j in range(len(graph)):
        for i in range(len(graph[j])):
            set_colour(j, i, graph[j][i])


def draw_column(count, column):
    for i in range(count):
        column[6-(i % 7)] = [BLUE, YELLOW][i//7]


try:
    unicorn.brightness(0.5)
    unicorn.rotation(180)
    graph = [[[0 for k in range(3)] for j in range(8)] for i in range(8)]
    while True:
        graph = graph[1:8] + [[[0 for k in range(3)] for j in range(8)]]
        count, success = get_player_count()
        if not success:
            graph[7][7] = RED
        else:
            graph[7][7] = GREEN
            draw_column(count, graph[7])
        draw_graph(graph)
        unicorn.show()
        time.sleep(5)
except KeyboardInterrupt:
    unicorn.off()
