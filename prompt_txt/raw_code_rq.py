#!/usr/bin/env python3
#import config
import config as config

sys_mssg = f'''You program in {config.program_language}.
You create the code that implements the description in Program Description and that follows these specific requirements as outlined in Requirements.
Add statement __name__ == '__main__' to the code module .
You insert the code in a JSON object. Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
(d) escape every special character in the code for json.load to read the JSON object correctly.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
You must validate the JSON object construct for syntax.
You ensure parsing the JSON object using {config.program_language}'s built-in JSON module would not raise an error exception.
'''
#You make no comments in your response.

gpt_task = f'''Your Task:
(1) To create the code for a single module (.py file) named {config.module_script_fname} in {config.program_language}.
(2) The code you create implements the Program Description.
(3) Your response to this request meets the Requirements.
'''

json_object_requirements = f'''Your response to this request is exclusively:
(a) a JSON object with the template described in JSON Required Format Template.
(b) You ensure parsing the JSON object using {config.program_language}'s built-in JSON module would not raise an error exception.
(c) You add nothing else to your response of this request but the JSON object.
(d) escape every special character in the code for json.load to read the JSON object correctly.
'''

task_requirements = '''Your response to this request meets every requirement. Requirements:
(1) the JSON object you create meets each and every requirement in:
(a) JSON Required Format Template
(b) the Comment Requirements
(2) your code meets each and every requirement in the:
(a) Program Description
(b) Code Requirements
(b) Comment Requirements
'''

comments = '''Comment Requirements:
(1) Your response only includes the JSON object.
(2) You make no comments in your response. 
(3) Keep comments within the code to the bare minimum"
'''

module_requirements = '''Code Requirements:
(1) each method in the module is atomic, for example a calculator has different methods to sum, divide, multiply or subtract
(2) create in the code a function named program(arguments) with the required arguments for program to execute the main program
(3) create the code to print on screen program results
(4) Add statement __name__ == '__main__' to the code module.
(5) the code meets the requirements described in:'Comment Requirements'
(6) place every module you import are at the top of the code and not inside any function you create
(7) Do not enclose anything either at the beginning or the end in the JSON Object with three double or single quotes
'''
json_required_format ='''JSON Required Format Template:
{
"module":"Insert here the code you produced as described in Program Description leaving no spaces from the beginning to the first character inserted"
}
'''

example_code_1 = '''Example Code for a summing calculator:
def sum(a, b):
    return a + b

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
'''

example_code_2 = '''Example Code for a word counter:

def count_words(input_str):
    words = input_str.split()
    return len(words)

def program(input_str=None):
    if input_str is None:
        input_str = input('Enter a sentence or paragraph: ')
    return count_words(input_str)
'''

example_code_3 = '''Example Code where the program generates a random number, and the user is prompted to guess the number. The program provides feedback on whether the guess is too high, too low, or correct.:
import random

import random

def get_random_number():
    return random.randint(1, 100)

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

raw_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements":json_object_requirements.replace("\n",""),
    "task_requirements":task_requirements.replace("\n",""),
    "module_requirements":module_requirements.replace("\n",""),
    "comments": comments.replace("\n",""),
    "json_required_format": json_required_format.replace("\n","")
}