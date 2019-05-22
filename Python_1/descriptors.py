class Descriptor:
    def __init__(self):
        self.value = None

    @staticmethod
    def save_value(value):
        with open("1.txt", "a") as f:
            f.write(str(value))

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.save_value(value)
        self.value = value


class Class:
    attr = Descriptor()


if __name__ == "__main__":
    cl1 = Class()
    cl1.attr = 10
    cl1.attr = 11