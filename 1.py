#!/usr/bin/env python3

import argparse
import logging

logging.basicConfig(filename='/home/sergio/Simple_Selfgen/project/module.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')

def program(num1, num2, operation):
    try:
        if operation == 'sum':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A calculator that performs addition, subtraction, multiplication, and division operations on two numbers.')
    parser.add_argument('num1', type=float, help='The first number')
    parser.add_argument('num2', type=float, help='The second number')
    parser.add_argument('operation', type=str, help='The arithmetic operation to perform', choices=['sum', 'subtract', 'multiply', 'divide'])
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    try:
        program(args.num1, args.num2, args.operation)
        logging.info('User input: num1=%s, num2=%s, operation=%s', args.num1, args.num2, args.operation)
    except Exception as e:
        print(e)
        logging.error(e, exc_info=True)
