from abc import ABC, abstractmethod


class A(ABC):

    def __init__(self, data, result):
        self.data = data
        self.result =result

    @abstractmethod
    def do_something(self):
        print(self.data)


class B(A):

    def do_something_else(self):
        print("Hello!")

    def do_something(self):
        super().do_something()

if __name__ == '__main__':
    b = B(123, 321)
    b.do_something()
    b.do_something_else()
    print(b.data, b.result)
