#!/usr/bin/env python3

import argparse
import math

def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    try:
        return a/b
    except ZeroDivisionError:
        print('Error: division by zero')
        exit(1)

def program():
    parser = argparse.ArgumentParser(description='Perform basic arithmetic operations')
    parser.add_argument('a', type=float, help='First number')
    parser.add_argument('b', type=float, help='Second number')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--sum', dest='sum', action='store_const', const=add, help='sum of two numbers')
    parser.add_argument('--difference', dest='difference', action='store_const', const=subtract, help='difference of two numbers')
    parser.add_argument('--product', dest='product', action='store_const', const=multiply, help='product of two numbers')
    parser.add_argument('--quotient', dest='quotient', action='store_const', const=divide, help='quotient of two numbers')
    args = parser.parse_args()
    a = args.a
    b = args.b
    result = {}
    if args.sum:
        result['sum'] = add(a,b)
    if args.difference:
        result['difference'] = subtract(a,b)
    if args.product:
        result['product'] = multiply(a,b)
    if args.quotient:
        result['quotient'] = divide(a,b)
    return result

if __name__ == '__main__':
    results = program()
    print(results)