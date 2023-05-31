#!/usr/bin/env python3
#add unittest

#TODO move to class var
program_language="Python"
unittest_cli_command_key = "unittest_cli_"
module_name = "module.py"

sys_mssg = f'''You are going to add unit testing functionality using pythong built-in unittest package to a script written in {program_language} I give you.
Every cli command makes a call with the exact name of a unit test or test case function and capitalized where appropiate.
Write the unit test methods within a unittest.TestCase subclass. Design the unit tests to mark each test case as a success and avoid the test failure.
You will not delete any of the code I give you.
The name of the module (.py file) is {module_name}.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
You must validate the JSON object construct for syntax and parsing the JSON object would not raise an error exception 
according to {program_language}'s built-in JSON module.
'''
#Unittest test cases must be defined at the top level of the module (not inside a function) so they can be discovered and run.
#It is very important you do not nest or define the test case unittest.TestCase function inside inside any other function.
gpt_task = f'''Your Task:
(a) Each function in the module has one or multiple corresponding unittest function to unit-test.
(b) Each unittest function tests every statement of its corresponding function in the module.
Hence a module function may have multiple corresponding unittest functions.
(c) Create multiple unittest functions to test the program() function, where you specifically design each unittest function to test each single statement of the program function.
(d) Write the unit test methods within a unittest.TestCase subclass.
(e) Design the unit tests to mark each test case as a success and avoid the test failure
(f) Properly structure each test method as a test case starting with "test_" prefix
(g) Ensure logging captures expected messages attending to the correct logging level used for the code; use assertLogs in unit tests to validate the occurrence of specific log entries.
(h) you name each unittest function {unittest_cli_command_key} with ascending numbers for each starting at 1. Insert each unittest function 
name as a key in the JSON Object Template
(i) For each of these unittest function keys add as value in the JSON Object Template the corresonding linux cli command 
to trigger the execution of that {unittest_cli_command_key} function.
(j) insert the code for the module including unittest in the JSON Object Template's value for key 'module' 
without leaving no spaces from the beginning to the first character inserted.
(k) Create in the code a function named program(arguments) with the required arguments for program to execute the main program
'''

#It is very important every cli command makes a call with the exact name of a unit test function and capitalized where appropiate.
#(f) It is very important you **do not nest the test case function inside any other function.
#(2) Hard code input variables to test each backtesting function and hard code an expected_output variable with the expected result
#Compare the expected_output to the backtesting function output in an assert statement.
#(d) User interaction is disabled when a unittest function call any function in the module

json_object_requirements = f'''Your response to this request is exclusively:
(a) a JSON object with the template described in JSON Object Template.
(b) You ensure parsing the JSON object using {program_language}'s built-in JSON module would not raise an error exception.
(c) You add nothing else to your response of this request but the JSON object.
'''

comments = '''.Your response meets these Comment Requirements:
(1) Your response only includes the JSON object.
(2) You make no comments in your response. 
(3) Keep comments within the code to the bare minimum"
'''

json_required_format ='''JSON Object Template:
{
"module":"Insert here the code with the enhancements you make leaving no spaces from the beginning to the first character inserted",
"unittest_cli_1":"Insert the command line command to trigger the execution of the corresponding unittest function"
}
'''

unittest_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements":json_object_requirements.replace("\n",""),
    "comments": comments.replace("\n",""),
    "json_required_format": json_required_format.replace("\n",""),
}