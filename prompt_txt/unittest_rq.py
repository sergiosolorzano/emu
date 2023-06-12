#!/usr/bin/env python3
#import config
import config as config

#add unittest
sys_mssg = f'''You are going to add unit testing functionality using {config.program_language}'s built-in unittest package to a script written in {config.program_language} I give you.
Insert the linux cli command to execute every unit test case function in the JSON Object Template provided, and for each use JSON key {config.unittest_cli_command_key} with ascending number.
Write the unit test methods within a unittest.TestCase subclass. Design the unit tests to mark each test case as a success and no test failure occurs.
If there is an exception the program terminates gracefully with an error message.
You will not delete any of the code I give you.
The name of the module (.py file) is {config.module_utest_name}.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
Escape every special character in the code for json.load to read the JSON object correctly.
You must validate the JSON object construct for syntax and parsing the JSON object would not raise an error exception 
according to {config.program_language}'s built-in JSON module. Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
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
(f) If there is an exception the program terminates gracefully with an error message.
(g) Properly structure each test method as a test case starting with "test_" prefix
(h) Ensure logging captures expected messages attending to the correct logging level used for the code; use assertLogs in unit tests to validate the occurrence of specific log entries.
(i) you name every unittest function {config.unittest_cli_command_key} with ascending numbers for each starting at 1. Insert every unit test case function 
name as a key in the JSON Object Template
(j) For each of these unittest function keys add as value in the JSON Object Template the corresponding linux cli command 
to trigger the execution of that {config.unittest_cli_command_key} function.
(k) insert the code for the module including unittest in the JSON Object Template's value for key 'module' 
without leaving no spaces from the beginning to the first character inserted.
(l) Create in the code a function named program(arguments) with the required arguments for program to execute the main program
(m) Change main() to execute the unit test cases
'''

json_object_requirements = f'''Your response to this request is exclusively:
(a) a JSON object with the template described in JSON Object Template.
(b) You ensure parsing the JSON object using {config.program_language}'s built-in JSON module would not raise an error exception.
(c) You add nothing else to your response of this request but the JSON object.
(d) escape every special character in the code for json.load to read the JSON object correctly.
'''

comments = '''Your response meets these Comment Requirements:
(1) Your response only includes the JSON object.
(2) You make no comments in your response. 
(3) Keep comments within the code to the bare minimum"
'''

json_required_format ='''JSON Object Template:
{
"module":"Insert here the code with the enhancements you make leaving no spaces from the beginning to the first character inserted",
"unittest_cli_1":"Insert the command line command to trigger the execution of the corresponding unit test case function"
}
'''

unittest_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements":json_object_requirements.replace("\n",""),
    "comments": comments.replace("\n",""),
    "json_required_format": json_required_format.replace("\n",""),
}
