#!/usr/bin/env python3

def sum(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    return a/b

def program(a,b):
    print("Sum: ",sum(a,b))
    print("Difference: ",subtract(a,b))
    print("Product: ",multiply(a,b))
    print("Quotient: ",divide(a,b))
if __name__=='__main__':
    program(10,5)