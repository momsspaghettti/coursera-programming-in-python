#import pygame
import random
import math

SCREEN_DIM = (800, 600)


# Класс двумерных векторов

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

    def get_points(self, base_points, count):
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


# Отрисовка справки
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# Основная функция

def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    polyline = Polyline()
    knot = Knot()
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline.points = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline.points.append(Vec2d(event.pos.x, event.pos.y))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points(gameDisplay=gameDisplay)
        knot.points = polyline.points
        knot.get_knot(steps)
        polyline.draw_points(gameDisplay=gameDisplay)
        if not pause:
            polyline.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)


if __name__ == "__main__":
    main()