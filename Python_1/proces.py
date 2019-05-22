import threading

class Point(object)
    def __init__(self):
        self._mutex = threading.RLock()
        self._x = 0
        self._y = 0

    def get(self):
        with self._mutex:
            return (self._x, self._y)

    def set(self, x, y):
        with self._mutex:
            self._x = x
            self._y = y