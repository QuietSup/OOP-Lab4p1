# 1. Modify the class Rational of Lab No2 to perform the following tasks:
# - adding two Rational numbers. The result should be stored in reduced form;
# - subtracting two Rational numbers. The result should be stored in reduced form;
# - multiplying two Rational numbers. The result should be stored in reduced form;
# - dividing two Rational numbers. The result should be stored in reduced form;
# - comparison two Rational numbers.

import math


class Rational:
    """Contains info about the rational including numerator and denominator
    calculates divisor to simplify a number"""
    def __init__(self, numerator=None, denominator=None):
        if numerator is None:
            numerator = 1
        if denominator is None:
            denominator = 1

        divisor = math.gcd(numerator, denominator)
        self.__num = numerator // divisor
        self.__den = denominator // divisor

    def __call__(self):
        """Return a rational as float

        to be called as num()"""
        return self.__num / self.__den

    def __repr__(self):
        """Return a rational as string in a/b form"""
        return f'{self.num} / {self.den}'

    # OPERATIONS
    def __add__(self, other):
        """Return self+other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can add only numbers (rational, int, float)")
        if isinstance(other, int):
            other = Rational(other, 1)
        if isinstance(other, float):
            other = other.as_integer_ratio()
            other = Rational(other[0], other[1])
        return Rational(self.num * other.den + other.num * self.den, self.den * other.den)

    def __sub__(self, other):
        """Return self-other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You subtract add only numbers (rational, int, float)")
        if isinstance(other, int):
            other = Rational(other, 1)
        if isinstance(other, float):
            other = other.as_integer_ratio()
            other = Rational(other[0], other[1])
        return Rational(self.num * other.den - other.num * self.den, self.den * other.den)

    def __mul__(self, other):
        """Return self*other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can multiply only numbers (rational, int, float)")
        if isinstance(other, int):
            other = Rational(other, 1)
        if isinstance(other, float):
            other = other.as_integer_ratio()
            other = Rational(other[0], other[1])
        return Rational(self.num * other.num, self.den * other.den)

    def __truediv__(self, other):
        """Return self/other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can divide only numbers (rational, int, float)")
        if isinstance(other, int):
            other = Rational(other, 1)
        if isinstance(other, float):
            other = other.as_integer_ratio()
            other = Rational(other[0], other[1])
        return Rational(self.num * other.den, self.den * other.num)

    # COMPARISON
    def __lt__(self, other):
        """Return self<other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can compare only numbers (rational, int, float)")
        return self() < (other() if isinstance(other, Rational) else other)

    def __gt__(self, other):
        """Return self>other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can compare only numbers (rational, int, float)")
        return self() > (other() if isinstance(other, Rational) else other)

    def __le__(self, other):
        """Return self<=other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can compare only numbers (rational, int, float)")
        return self() <= (other() if isinstance(other, Rational) else other)

    def __ge__(self, other):
        """Return self>=other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can compare only numbers (rational, int, float)")
        return self() >= (other() if isinstance(other, Rational) else other)

    def __eq__(self, other):
        """Return self==other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can compare only numbers (rational, int, float)")
        return self() == (other() if isinstance(other, Rational) else other)

    def __ne__(self, other):
        """Return self!=other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can compare only numbers (rational, int, float)")
        return self() != (other() if isinstance(other, Rational) else other)

    # +=, -=, etc
    def __iadd__(self, other):
        """Return self+=other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can add only numbers (rational, int, float)")
        if isinstance(other, int):
            other = Rational(other, 1)
        if isinstance(other, float):
            other = other.as_integer_ratio()
            other = Rational(other[0], other[1])
        self.num, self.den = (self.num * other.den + other.num * self.den), (self.den * other.den)
        return self

    def __isub__(self, other):
        """Return self-=other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You subtract add only numbers (rational, int, float)")
        if isinstance(other, int):
            other = Rational(other, 1)
        if isinstance(other, float):
            other = other.as_integer_ratio()
            other = Rational(other[0], other[1])
        self.num, self.den = (self.num * other.den - other.num * self.den), (self.den * other.den)
        return self

    def __imul__(self, other):
        """Return self*=other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can multiply only numbers (rational, int, float)")
        if isinstance(other, int):
            other = Rational(other, 1)
        if isinstance(other, float):
            other = other.as_integer_ratio()
            other = Rational(other[0], other[1])
        self.num, self.den = (self.num * other.num), (self.den * other.den)
        return self

    def __itruediv__(self, other):
        """Return self/=other"""
        if not isinstance(other, (Rational, int, float)):
            raise TypeError("You can divide only numbers (rational, int, float)")
        if isinstance(other, int):
            other = Rational(other, 1)
        if isinstance(other, float):
            other = other.as_integer_ratio()
            other = Rational(other[0], other[1])
        self.num, self.den = (self.num * other.den), (self.den * other.num)
        return self

    @property
    def num(self):
        return self.__num

    @property
    def den(self):
        return self.__den

    @num.setter
    def num(self, value):
        if not isinstance(value, int):
            raise ValueError("Numerator isn't int")
        self.__num = value

    @den.setter
    def den(self, value):
        if not isinstance(value, int):
            raise ValueError("Denominator isn't int")
        if value == 0:
            raise ValueError("Denominator can't be zero")
        self.__den = value


if __name__ == '__main__':
    a = Rational(1, 2)
    b = Rational()

    print(a)

    print(b)
    n = a + b
    print('+\n', n)
    n = a + 4.5
    print(n)
    a += 4.5
    print(a)
    print(n())
    n = a - b
    print('-\n', n)
    n = a - 4.5
    print(n)
    n = a * b
    print('*\n', n)
    n = a * 4.5
    print(n)
    n = a / b
    print('/\n', n)
    n = a / 4.5
    print(n)

    print(a <= 4)
