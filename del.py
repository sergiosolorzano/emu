#!/usr/bin/env python3
import sys

def sum(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 == 0:
        print("Cannot divide by zero")
        sys.exit()
    return num1 / num2

def program(num1, num2, operation):
    result = None
    if operation == "sum":
        result = sum(num1, num2)
    elif operation == "subtract":
        result = subtract(num1, num2)
    elif operation == "multiply":
        result = multiply(num1, num2)
    elif operation == "divide":
        result = divide(num1, num2)
    else:
        print("Invalid operation")
        sys.exit()
    print(result)

if __name__ == '__main__':
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    operation = input("Enter operation (sum, subtract, multiply, divide): ")
    program(num1, num2, operation)