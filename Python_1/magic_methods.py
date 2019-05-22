import time

class timer:

    def __init__(self):
        self.start = time.time()

    def __enter__(self):
        return

    def __exit__(self, *args):
        print(time.time() - self.start)
        return True




