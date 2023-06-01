#!/usr/bin/env python3

import argparse
import sys
import logging

def calculator(num1, num2, op):
    try:
        if op == '+':
            return num1 + num2
        elif op == '-':
            return num1 - num2
        elif op == '*':
            return num1 * num2
        elif op == '/':
            if num2 == 0:
                logging.error('Error: cannot divide by 0', exc_info=True)
                raise ZeroDivisionError('Error: cannot divide by 0')
            else:
                return num1 / num2
    except Exception as e:
        logging.error(str(e), exc_info=True)
        raise

def program():
    try:
        parser = argparse.ArgumentParser(description='A calculator program that collects two numbers from a user and the arithmetic operation to perform being a choice of sum, subtract, multiply or divide. Then print the result on the terminal.')
        parser.add_argument('num1', help='first number', type=float)
        parser.add_argument('num2', help='second number', type=float)
        parser.add_argument('op', help='operation: +, -, *, /', type=str)
        parser.add_argument('--version', action='version', version='%(prog)s 1.0')
        args = parser.parse_args()
        num1 = args.num1
        num2 = args.num2
        op = args.op
        result = calculator(num1, num2, op)
        print(result)
        logging.debug('Result: ' + str(result))
    except Exception as e:
        logging.error(str(e), exc_info=True)
        raise

if __name__ == '__main__':
    logging.basicConfig(filename='/home/sergio/Simple_Selfgen/project/module.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s - %(lineno)d')
    program()