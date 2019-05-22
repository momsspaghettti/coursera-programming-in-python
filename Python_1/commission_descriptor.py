class Value:

    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = self.pay_commission(value, instance.commission)

    @staticmethod
    def pay_commission(value, commission):
        return value * (1 - commission)


class Account:
    amount = Value()
    commission = 0.0

    def __init__(self, commission):
        if commission > 1:
            self.commission = 1
        else:
            self.commission = commission


if __name__ == "__main__":
    new_account = Account(0.1)
    new_account.amount = 100
    print(new_account.amount)