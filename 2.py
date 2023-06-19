#!/usr/bin/env python3

import argparse
import math
import logging

logging.basicConfig(filename='/home/sergio/PythonWorkspace/emu/project/module.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')


def add(a,b):
    try:
        return a+b
    except Exception as e:
        logging.error('Error occurred: {}'.format(e), exc_info=True)
        return 'Error: {}'.format(e)

def subtract(a,b):
    try:
        return a-b
    except Exception as e:
        logging.error('Error occurred: {}'.format(e), exc_info=True)
        return 'Error: {}'.format(e)

def multiply(a,b):
    try:
        return a*b
    except Exception as e:
        logging.error('Error occurred: {}'.format(e), exc_info=True)
        return 'Error: {}'.format(e)

def divide(a,b):
    try:
        if b==0:
            return a/b

def square_root(a):
    try:
        if a<0:
            raise ValueError('negative number')
        else:
            return math.sqrt(a)
    except Exception as e:
        logging.error('Error occurred: {}'.format(e), exc_info=True)
        return 'Error: {}'.format(e)

def program():
    try:
        parser = argparse.ArgumentParser(description='Performs basic calculator operations and calculates square roots.')
        parser.add_argument('num1', type=float, help='First number')
        parser.add_argument('num2', type=float, help='Second number')
        parser.add_argument('-a', '--add', action='store_true', help='Add the two numbers')
        parser.add_argument('-s', '--subtract', action='store_true', help='Subtract the two numbers')
        parser.add_argument('-m', '--multiply', action='store_true', help='Multiply the two numbers')
        parser.add_argument('-d', '--divide', action='store_true', help='Divide the two numbers')
        parser.add_argument('-r1', '--root1', action='store_true', help='Calculate the square root of the first number')
        parser.add_argument('-r2', '--root2', action='store_true', help='Calculate the square root of the second number')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
        args = parser.parse_args()
        a = args.num1
        b = args.num2
        if args.add:
            print('Sum:', add(a,b))
        if args.subtract:
            print('Difference:', subtract(a,b))
        if args.multiply:
            print('Product:', multiply(a,b))
        if args.divide:
            print('Quotient:', divide(a,b))
        if args.root1:
            print('Square Root of', a, ':', square_root(a))
        if args.root2:
            print('Square Root of', b, ':', square_root(b))
    except Exception as e:
        logging.error('Error occurred: {}'.format(e), exc_info=True)
        print('Error: {}'.format(e))

if __name__ == '__main__':
    program()
