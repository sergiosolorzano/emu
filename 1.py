#!/usr/bin/env python3

import math

def program(number):
    if number < 0:
        return 'Invalid input'
    elif number == 0:
        return 1
    else:
        result = 1
        for i in range(1, number+1):
            result *= i
        return result

if __name__ == '__main__':
    num = int(input('Enter a non-negative integer: '))
    print(program(num))