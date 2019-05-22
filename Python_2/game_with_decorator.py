from abc import ABC, abstractmethod


class Hero:

    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):

    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_stats(self):
        self.base.get_stats()

    @abstractmethod
    def get_positive_effects(self):
        self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        self.base.get_negative_effects()


class AbstractPositive(AbstractEffect):

    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_stats(self):
        self.base.get_stats()

    @abstractmethod
    def get_positive_effects(self):
        self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):

    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_stats(self):
        self.base.get_stats()

    @abstractmethod
    def get_positive_effects(self):
        self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        self.base.get_negative_effects()


class Berserk(AbstractPositive):

    def get_positive_effects(self):
        self.positive_effects = self.base.get_positive_effects()
        self.positive_effects.append("Berserk")
        return self.positive_effects

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Strength"] += 7
        self.stats["Endurance"] += 7
        self.stats["Agility"] += 7
        self.stats["Luck"] += 7

        self.stats["Perception"] -= 3
        self.stats["Charisma"] -= 3
        self.stats["Intelligence"] -= 3

        self.stats["HP"] += 50

        return self.stats

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class Blessing(AbstractPositive):

    def get_positive_effects(self):
        self.positive_effects = self.base.get_positive_effects()
        self.positive_effects.append("Blessing")
        return self.positive_effects

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.base.stats["Strength"] += 2
        self.base.stats["Endurance"] += 2
        self.base.stats["Agility"] += 2
        self.base.stats["Luck"] += 2
        self.base.stats["Perception"] += 2
        self.base.stats["Charisma"] += 2
        self.base.stats["Intelligence"] += 2

        return self.stats

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class Weakness(AbstractNegative):

    def get_negative_effects(self):
        self.negative_effects = self.base.get_negative_effects()
        self.negative_effects.append("Weakness")
        return self.negative_effects

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Strength"] -= 4
        self.stats["Endurance"] -= 4
        self.stats["Agility"] -= 4

        return self.stats

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class EvilEye(AbstractNegative):

    def get_negative_effects(self):
        self.negative_effects = self.base.get_negative_effects()
        self.negative_effects.append("EvilEye")
        return self.negative_effects

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Luck"] -= 10

        return self.stats

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Curse(AbstractNegative):

    def get_negative_effects(self):
        self.negative_effects = self.base.get_negative_effects()
        self.negative_effects.append("Curse")
        return self.negative_effects

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Strength"] -= 2
        self.stats["Endurance"] -= 2
        self.stats["Agility"] -= 2
        self.stats["Luck"] -= 2
        self.stats["Perception"] -= 2
        self.stats["Charisma"] -= 2
        self.stats["Intelligence"] -= 2

        return self.stats

    def get_positive_effects(self):
        return self.base.get_positive_effects()


if __name__ == '__main__':
    hero = Hero()

    hero.get_positive_effects()
    hero.get_negative_effects()
    print(hero.get_stats())

    new_hero = Berserk(hero)
    print(hero.get_stats())
    print(new_hero.get_stats())
    new_hero = Blessing(new_hero)
    print(new_hero.get_stats(), new_hero.get_positive_effects())
    new_hero = Curse(new_hero)
    print(new_hero.get_positive_effects(), new_hero.get_negative_effects())
