import math

import pygame
import random
from typing import List, Union


class Game:
    HELP_MENU = [['F1', 'Show Help'], ['R', 'Restart'],
                 ['P', 'Pause/Play'], ['Num+', 'More points'],
                 ['Num-', 'Less points'], ['', '']]

    def __init__(self, show_help=False):
        self.steps = 35
        self.working = True

        self.show_help = show_help
        self.pause = True
        self.hue = 0
        self.color = pygame.Color(0)

        #
        self.polyline: Knot = Knot()

        self.points: List[Vec2d] = []
        self.speeds = []

    def _start(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")

    def _finish(self):
        pygame.display.quit()
        pygame.quit()
        exit(0)

    def _handler_QUIT(self, event):
        self.working = False

    def _handler_KEYDOWN(self, event):
        if event.key == pygame.K_ESCAPE:
            self.working = False
        if event.key == pygame.K_r:
            self.polyline = Polyline()
            self.points = []
            self.speeds = []
        if event.key == pygame.K_p:
            self.pause = not self.pause
        if event.key == pygame.K_KP_PLUS:
            self.steps += 1
        if event.key == pygame.K_F1:
            self.show_help = not self.show_help
        if event.key == pygame.K_KP_MINUS:
            self.steps -= 1 if self.steps > 1 else 0

    def _handler_MOUSEBUTTONDOWN(self, event):
        cur_pos = Vec2d(*event.pos)
        self.polyline.add_points(cur_pos, Vec2d(random.random() * 2, random.random() * 2))

    def render_screen(self):
        self.gameDisplay.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)
        self.polyline.draw_points(color=(255, 255, 255), gameDisplay=self.gameDisplay)
        self.polyline.draw_points(count=3, style='line', color=self.color, gameDisplay=self.gameDisplay)

    def draw_help(self):
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        help_menu = self.HELP_MENU.copy()
        help_menu.append([str(self.steps), "Current points"])
        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(help_menu):
            self.gameDisplay.blit(font1.render(text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def run(self):
        self._start()
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._handler_QUIT(event)
                if event.type == pygame.KEYDOWN:
                    self._handler_KEYDOWN(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handler_MOUSEBUTTONDOWN(event)
            self.render_screen()
            if not self.pause:
                self.polyline.set_points()
            if self.show_help:
                self.draw_help()
            pygame.display.flip()
        self._finish()


SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __getitem__(self, item):
        if item == 0:
            return self._x
        elif item == 1:
            return self._y
        raise IndexError

    def __len__(self):
        return math.sqrt(self._x**2 + self._y**2)

    def __sub__(self, other):
        return Vec2d(self._x - other[0], self._y - other[1])

    def __add__(self, other):
        return Vec2d(self._x + other[0], self._y + other[1])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2d(self._x * other, self._y * other)
        elif isinstance(other, Vec2d):
            pass

    def int_pair(self):
        return int(self._x), int(self._y)


class Polyline:

    def __init__(self):
        self.points = []
        self.speeds = []

    def get_point(self, points, alpha, deg=None) -> Vec2d:
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def pop_point(self):
        self.points.pop()
        self.speeds.pop()

    def add_points(self, points: Vec2d, speed: Vec2d):
        self.points.append(points)
        self.speeds.append(speed)

    def get_points(self, base_points: List[Vec2d], count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def draw_points(self, width=3, *, gameDisplay, **kwargs):
        color = kwargs.get('color', (255, 255, 255))
        for p in self.points:
            pygame.draw.circle(gameDisplay, color, (int(p[0]), int(p[1])), width)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = Vec2d(- self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = Vec2d(self.speeds[p][0], - self.speeds[p][1])


class Knot(Polyline):

    def draw_points(self, width=3, *, gameDisplay, **kwargs):
        if kwargs.get('style') == 'line':
            color = kwargs.get('color', (255, 255, 255))
            count = kwargs['count']
            points = self.get_knot(count)
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (int(points[p_n][0]), int(points[p_n][1])),
                                 (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

        else:
            super().draw_points(width=3, gameDisplay=gameDisplay, **kwargs)

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [(self.points[i] + self.points[i + 1]) * 0.5,
                   self.points[i + 1],
                   (self.points[i + 1] + self.points[i + 2]) * 0.5
                   ]
            res.extend(self.get_points(ptn, count))
        return res


if __name__ == "__main__":
    Game().run()