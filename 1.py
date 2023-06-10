#!/usr/bin/env python3

import math
import unittest

def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    return a/b

def power(a,b):
    return math.pow(a,b)

def square_root(a):
    return math.sqrt(a)

def program(operation, a, b):
    if operation == 'add':
        result = add(a,b)
    elif operation == 'subtract':
        result = subtract(a,b)
    elif operation == 'multiply':
        result = multiply(a,b)
    elif operation == 'divide':
        result = divide(a,b)
    elif operation == 'power':
        result = power(a,b)
    elif operation == 'square_root':
        result = square_root(a)
    return result

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2,3), 5)
    def test_subtract(self):
        self.assertEqual(subtract(5,3), 2)
    def test_multiply(self):
        self.assertEqual(multiply(2,3), 6)
    def test_divide(self):
        self.assertEqual(divide(6,3), 2)
    def test_power(self):
        self.assertEqual(power(2,3), 8)
    def test_square_root(self):
        self.assertEqual(square_root(25), 5)
    def test_program_add(self):
        self.assertEqual(program('add', 2, 3), 5)
    def test_program_subtract(self):
        self.assertEqual(program('subtract', 5, 3), 2)
    def test_program_multiply(self):
        self.assertEqual(program('multiply', 2, 3), 6)
    def test_program_divide(self):
        self.assertEqual(program('divide', 6, 3), 2)
    def test_program_power(self):
        self.assertEqual(program('power', 2, 3), 8)
    def test_program_square_root(self):
        self.assertEqual(program('square_root', 25), 5)

if __name__ == '__main__':
    unittest.main()