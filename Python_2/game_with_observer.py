from abc import ABC, abstractmethod


class ObservableEngine():

    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        if subscriber in self.__subscribers:
            self.__subscribers.remove(subscriber)

    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, message):
        pass


class ShortNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = set()

    def update(self, message):
        self.achievements.add(message["title"])


class FullNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = list()

    def update(self, message):
        if message not in self.achievements:
            self.achievements.append(message)


if __name__ == '__main__':
    engine = ObservableEngine()

    short = ShortNotificationPrinter()
    full = FullNotificationPrinter()

    engine.subscribe(short)
    engine.subscribe(full)

    engine.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})

    print(short.achievements)
    print(full.achievements)
