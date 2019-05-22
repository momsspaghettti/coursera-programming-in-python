from abc import ABC, abstractmethod


class Creature(ABC):

    @abstractmethod
    def feed(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def make_noise(self):
        pass


class Animal(Creature):

    def feed(self):
        print("I eat grass")

    def move(self):
        print("I walk forward")

    def make_noise(self):
        print("WOOO!")


class AbstractDecorator(Creature):

    def __init__(self, base):
        self.base = base

    def move(self):
        self.base.move()

    def feed(self):
        self.base.feed()

    def make_noise(self):
        self.base.make_noise()


class Swimming(AbstractDecorator):

    def move(self):
        print("I swim forward")

    def make_noise(self):
        print("...")


class Predator(AbstractDecorator):

    def feed(self):
        print("I eat other animals")


class Fast(AbstractDecorator):

    def move(self):
        self.base.move()
        print("Fast!")


if __name__ == '__main__':
    animal = Animal()

    swimming = Swimming(animal)

    predator = Predator(swimming)

    fast_predator = Fast(predator)

    fast_predator.move()
    fast_predator.feed()
    fast_predator.make_noise()  