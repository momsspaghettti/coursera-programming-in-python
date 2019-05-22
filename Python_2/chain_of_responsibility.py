class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:

    def __init__(self, type_):
        self.type_ = type_


class EventSet:

    def __init__(self, value):
        self.value = value


class NullHandler:

    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):

    def handle(self, obj, event):
        if (type(event) == EventGet) and issubclass(event.type_, int):
            print(f"вернуть значение {obj.integer_field}")
            return obj.integer_field
        elif (type(event) == EventSet) and (type(event.value) == int):
            print(f"установить значение {obj.integer_field} = {event.value}")
            obj.integer_field = event.value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):

    def handle(self, obj, event):
        if (type(event) == EventGet) and issubclass(event.type_, float):
            print(f"вернуть значение {obj.float_field}")
            return obj.float_field
        elif (type(event) == EventSet) and (type(event.value) == float):
            print(f"установить значение {obj.float_field} = {event.value}")
            obj.float_field = event.value
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):

    def handle(self, obj, event):
        if (type(event) == EventGet) and issubclass(event.type_, str):
            print(f"вернуть значение {obj.string_field}")
            return obj.string_field
        elif (type(event) == EventSet) and (type(event.value) == str):
            print(f"установить значение {obj.string_field} = {event.value}")
            obj.string_field = event.value
        else:
            return super().handle(obj, event)


if __name__ == '__main__':
    chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
    obj = SomeObject()

    chain.handle(obj, EventGet(int))
    chain.handle(obj, EventGet(str))
    chain.handle(obj, EventGet(float))
    chain.handle(obj, EventSet(1))
    chain.handle(obj, EventSet(1.1))
    chain.handle(obj, EventSet("str"))