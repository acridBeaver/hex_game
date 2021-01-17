import pygame as pg
from math import sqrt, hypot
from collections import deque
from hexogon.consts import *


class Point:
    def __init__(self, *pos):
        if len(pos) == 1:
            self.x, self.y = pos[0]
            self.X, self.Y = list(map(int, pos[0]))
        else:
            self.x, self.y = pos
            self.X, self.Y = list(map(int, pos))

    def dist(self, other):
        return hypot(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return '[x:{x}, y:{y}]'.format(x=self.x, y=self.y)

    def __iter__(self):
        return (x for x in (self.x, self.y))


def triangle_s(A, B, C):
    a = C.dist(B)
    b = A.dist(C)
    c = A.dist(B)
    p = (a + b + c) / 2
    return sqrt(p * (p - a) * (p - b) * (p - c))


def in_hex(pos, x, y, a):
    P = Point(pos)
    points = [(x + a, y), (x + a / 2, y + a * sqrt(3) / 2),
              (x - a / 2, y + a * sqrt(3) / 2), (x - a, y),
              (x - a / 2, y - a * sqrt(3) / 2), (x + a / 2, y - a * sqrt(3) / 2)]
    points = list(map(Point, points))
    sum = 0
    for i in range(-1, 5):
        sum += triangle_s(points[i], points[i + 1], P)
    S = a * a * 3 * sqrt(3) / 2
    return abs(S - sum) < EPS


def in_rect(pos, x, y, w, h):
    return x < pos.x < x + w and y < pos.y < y + h


def draw_hex(surface, count_in, count_out, pos, a):
    x, y = pos
    points = [(x - a / 2, y - a * sqrt(3) / 2),
              (x + a / 2, y - a * sqrt(3) / 2),
              (x + a, y),
              (x + a / 2, y + a * sqrt(3) / 2),
              (x - a / 2, y + a * sqrt(3) / 2),
              (x - a, y)]
    pg.draw.polygon(surface, count_in, points)
    pg.draw.polygon(surface, count_out, points, 4)


def in_bounds(v, w, h):
    return 0 <= v.X < h and 0 <= v.Y < w


def check_move(start, grid, exit, player):
    w = len(grid[0])
    h = len(grid)
    Q = deque()
    Q.append(start)
    used = [[False for _ in range(w)] for __ in range(h)]
    moves = [Point(1, 0), Point(1, -1), Point(0, 1),
             Point(0, -1), Point(-1, 1), Point(-1, 0)]
    while len(Q):
        cur = Q[-1]
        if exit(cur):
            return True
        used[cur.X][cur.Y] = True
        flag = False
        for m in moves:
            other = cur + m
            if (in_bounds(other, w, h) and not used[other.X][other.Y]) \
                    and grid[other.X][other.Y] == player:
                Q.append(other)
                flag = True
                break
        if not flag:
            Q.pop()
    return False


def text_rect(txt, size):
    font = pg.font.SysFont('Verdana', size)
    text = font.render(txt, False, BLACK)
    return text.get_rect()


def text_out(surface, data, size, col, pos):
    txt = str(data)
    font = pg.font.SysFont('Verdana', size)
    text = font.render(txt, False, col)
    rect = text.get_rect(center=pos)
    surface.blit(text, rect)
