"""Бизнес-логика для лабораторной работы 6."""
import math
class Calculator:
    @staticmethod
    def _number(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError('Expected a number')
        if not math.isfinite(value):
            raise ValueError('Expected a finite number')
    def add(self, a, b):
        self._number(a)
        self._number(b)
        return a + b
    def divide(self, a, b):
        self._number(a)
        self._number(b)
        if b == 0:
            raise ZeroDivisionError('Division by zero')
        return a / b
    @staticmethod
    def is_prime_number(n):
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError('Expected an integer')
        if n < 2:
            return False
        return all(n % divisor for divisor in range(2, math.isqrt(n) + 1))
