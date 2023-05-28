#!/usr/bin/env python3

program_language="Python"

module_name = "module.py"

gpt_task = f'''Your Task:
(1) To create the code for a single module (.py file) named {module_name} in {program_language}. Program Description described the code you need to create.
(2) Your response to this request is exclusively a JSON object with the template described in Required Format Template. You add nothing else to your response of this request but the JSON object.
(3) The code you produce for the module must meet the requirements in Code Requirements.
'''
backtest_cli_command_key = "backtest_cli_"

sys_mssg = f"You program in {program_language}. You create the code that follows these specific requirements: Backtesting Requirements, Required Format Template, Comment Requirements. You insert the code in the JSON object. Your response to this request is exclusively a JSON object. You must validate the JSON object construct for syntax. You make no comments in your response.  Each backtesting function tests every statement of its corresponding module function and the program function. Every input of the program function is an optional argument."

user_input = '''Add inputs to the code for the user to be prompted when the program is run.'''


comments = '''Comment Requirements:
(1) Your response only includes the JSON object.
(2) You make no comments in your response. 
(2) Keep comments within the code to the bare minimum"
'''

module_requirements = '''Code Requirements:
(1) each method in the module is atomic, for example a calculator has different methods to sum, divide, multiply or subtract
(2) create in the code a function named program that executes the main program.
(2) the code meets the requirements described in:
(a) 'Backtesting Requirements'
(b) 'Comment Requirements'
(c) If your code contains multipline use 3 of '
'''
backtesting_requirements = '''Backtesting Requirements:
(1) Create backtesting functions in the module to unit test.
(a) Each backtesting function tests every statement within the corresponding module function, including the program function.
(b) Each function in the module has a corresponding backtesting function to unit-test. No function in the module has no corresponding backtesting function
(c) Every input of the program function is an optional argument. This enables the backtesting function to unit-test all statements in the program function.
(d) Create multiple backtesting functions, with each function specifically designed to test a single statement of the program function.
(e) User input input() is disabled when a backtest_cli calls any module function or program function
(f) name each backtesting function backtest_cli_ with ascending numbers for each starting at 1
(g) add each backtesting function as a key in the Required Format Template. For each of these backtesting function keys add as value
in the Required Format Template the corresonding cli command to trigger the execution of that backtest cli function.
(2) Hard code input variables to test each backtesting function and hard code an expected_output variable with the expected result
Compare the expected_output to the backtesting function output in an assert statement.
'''

required_format ='''Required Format Template:
{
"module":"Insert here the code you produced as described in Program Description leaving no spaces from the beginning to the first character inserted",
"backtest_cli_1":"Insert the command line command to trigger the execution of a backtesting function"
}
'''

create_logs = f'''Log Requirements: 
(1) Insert the code to write logs to a file named module.log of every (a) function and user action errors (b) the context in which the error occurred
(2) add flag in the module script to enable/disable generating logs. set log level to debug. 
The flag can be set to enable/disabled
(3) use the built-in logging package'''

error_handling = f'''Error Handling Requirements: 
(a) Catch and handle exceptions for every function
(b) Input Validation: The program should validate all input and be prepared to handle invalid or unexpected input in a robust way.
(c) add flag in the module script to enable/disable generating logs. set log level to debug. 
The flag can be set to enable/disabled
(d) use the built-in logging package'''

example_code_1 = '''Example Code for a summing calculator:
def sum(a, b):
    return a + b

#Every input of the program function is an optional argument.
#So that user input input() is disabled when a backtest_cli calls any module function
def program(a=None, b=None, op=None):
    if a is None:
        a = float(input('Enter first number: '))
    if b is None:
        b = float(input('Enter second number: '))
    if op is None:
        op = input('Enter operation (+): ')
    else:
        return 'Error: invalid operation'
    return result

#Test every statement in program function by hard-coding input values and the expected output  in the backtest function
def backtest_cli_1():
    a, b, op = 2, 3, '+'
    expected_output = 5
    assert program(a, b, op) == expected_output, 'Fail'
'''

example_code_2 = '''Example Code for a word counter:

def count_words(input_str):
    words = input_str.split()
    return len(words)

#Every input of the program function is an optional argument.
#So that user input input() is disabled when a backtest_cli calls any module function
def program(input_str=None):
    if input_str is None:
        input_str = input('Enter a sentence or paragraph: ')
    return count_words(input_str)

#Test every statement in the program function by hard-coding input values and the expected output in the backtest function
def backtest_cli_1():
    input_str = 'Hello, my name is John. I am from New York.'
    expected_output = 11
    assert program(input_str) == expected_output, 'Fail'
'''

example_code_3 = '''Example Code where the program generates a random number, and the user is prompted to guess the number. The program provides feedback on whether the guess is too high, too low, or correct.:
import random

import random

def get_random_number():
    return random.randint(1, 100)

#Every input of every function is an optional argument.
#So that user input input() is disabled when a backtest_cli calls any module function

def guess_number(user_guess=None, random_number=None):
    while True:
        if user_guess is None:
            user_guess = int(input('Guess the number between 1 and 100: '))
        if random_number is None:
            random_number = get_random_number()
        if user_guess == random_number:
            return 'Congratulations! You guessed the correct number!'
        elif user_guess > random_number:
            return 'Too high, try again.'
        else:
            return 'Too low, try again.'

#Every input of the program function is an optional argument.
#So that user input input() is disabled when a backtest_cli calls any module function

def program(user_guess=None, random_number=None):
    if user_guess is None and random_number is None:
        guess_number()
    else:
        guess_number(user_guess,random_number)

#Test every statement in the program function by hard-coding input values and the expected output  in the backtest function
def backtest_cli_1():
    user_guess = 3
    random_number = 4
    expected_output = 'Too low, try again.'
    assert guess_number(user_guess,random_number) == expected_output, 'Fail'
'''

review = '''Once you have created the code, check that 
(1) the JSON object you create meets the Required Format Template
(2) each and every  of the following requirements are met in your code:
(a) Program Description
(b) Backtesting Requirements
(c) Comment Requirements
'''

#Enhancements
json_format ='''JSON Object Template:
{
"module":"Insert here the code with the enhancements you make leaving no spaces from the beginning to the first character inserted"
}
'''

module_instructions_dict = {
    "module_requirements":module_requirements.replace("\n",""),
    "backtesting_requirements":backtesting_requirements.replace("\n",""),
    "required_format": required_format.replace("\n",""),
    "comments": comments.replace("\n",""),
    "example_code_1": example_code_1.replace("\n",""),
    "example_code_2": example_code_2.replace("\n",""),
    "example_code_3": example_code_3.replace("\n",""),
    "review": review.replace("\n","")
}


#Wrap key and value in "".
#Add your code to the module.py property.
#(3) Add a flag to the module code named backtest that when enabled executes all functions using backtesting function inputs and when disabled uses user input.

# (1) Create backtesting functions in the module to unit test. Each backtesting function makes a call to execute a function in the module
# (b) Each function in the module has a corresponding backtesting function. No function in the module has no corresponding backtesting function
# (c) name each backtesting function backtest_cli_ with ascending numbers for each starting at 1
# (d) add each backtesting function as a key in the Required Format Template. For each of these backtesting function keys add as value
# in the Required Format Template the corresonding cli command to trigger the execution of that backtest cli function.
# (2) Each backtesting function tests all statements within the corresponding module function, including the program function.
# (3) Make the arguments of program function optional so the backtesting function can unit-test all statements in the program function.
# (3) Hard code input variables to test each backtesting function and hard code an expected_output variable with the expected result
# Compare the expected_output to the backtesting function output and print Success or Fail.