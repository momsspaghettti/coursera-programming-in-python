import unittest


def is_simple_number(x: int) -> bool:
    num = 0
    for i in range(2, x + 1):
        if x % i == 0:
            num += 1

    return num == 1


def is_square_num(x: int) -> bool:
    for i in range(int(x ** 0.5) - 1, int(x ** 0.5) + 1):
        if i * i == x:
            return True

    return False


def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    if not isinstance(x, int):
        raise TypeError

    if x < 0:
        raise ValueError

    factors_tuple = tuple()
    if x == 0:
        factors_tuple = (0, )
        return factors_tuple

    if x == 1:
        factors_tuple = (1, )
        return factors_tuple

    if is_square_num(x):
        factors_tuple = (int(x ** 0.5), int(x ** 0.5))
        return factors_tuple

    for i in range(2, x + 1):
        if x % i == 0 and is_simple_number(i):
            factors_tuple += (i, )

    return factors_tuple


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        with self.subTest(x=1):
            self.assertRaises(TypeError, factorize, 'string')
            self.assertRaises(TypeError, factorize, 1.5)

    def test_negative(self):
        for i in (-1, -10, -100):
            with self.subTest(x=2):
                self.assertRaises(ValueError, factorize, i)

    def test_zero_and_one_cases(self):
        with self.subTest(x=3):
            self.assertEqual(factorize(0), (0,))
            self.assertEqual(factorize(1), (1,))

    def test_simple_numbers(self):
        for i in (3, 13, 29):
            with self.subTest(x=4):
                self.assertEqual(factorize(i), (i,))

    def test_two_simple_multipliers(self):
        with self.subTest(x=5):
            self.assertEqual(factorize(6), (2, 3))
            self.assertEqual(factorize(26), (2, 13))
            self.assertEqual(factorize(121), (11, 11))

    def test_many_multipliers(self):
        with self.subTest(x=6):
            self.assertEqual(factorize(1001), (7, 11, 13))
            self.assertEqual(factorize(9699690), (2, 3, 5, 7, 11, 13, 17, 19))


if __name__ == '__main__':
    unittest.main()