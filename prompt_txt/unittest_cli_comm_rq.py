#!/usr/bin/env python3
#import config_dir
from config_dir import config as config

#add unittest
sys_mssg = f'''You are going to generate the cli commands to execute in linux for existing unittest functions in code I give you.
Every cli command makes a call with the exact name of a unit test or test case function and capitalized where appropiate.
Write the unit test methods within a unittest.TestCase subclass.
You will not make any changes whatsoever to the code I give you.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
Escape every special character in the code for json.load to read the JSON object correctly.
You must validate the JSON object construct for syntax and parsing the JSON object would not raise an error exception 
according to {config.program_language}'s built-in JSON module.
'''

#It is very important you do not nest or define the test case unittest.TestCase function inside any other function.

gpt_task = f'''You should know the code for a program is the value in the JSON Object's key 'module.
Your Task:
(a) Each unittest function you find in the code has a name that is a key in the JSON Object Template with name 'unittest_cli_' with ascending numbers for each starting at 1.
You will replace the value of the unittest_cli_ keys in the JSON object with its corresponding linux cli command to execute the unittest function.
(b) Write the unit test methods within a unittest.TestCase subclass.
(c) re-insert the code you have received in this request which is the value for key 'module' and make no changes to it in the JSON Object Template's value for key 'module' 
without leaving no spaces from the beginning to the first character inserted.
'''

#(b) Every cli command makes a call with the exact name of a unit test or test case function and capitalized where appropiate.
#It is very important you do not nest or define the test case unittest.TestCase function inside inside any other function.

json_object_requirements = f'''Your response to this request is exclusively:
(a) a JSON object with the template described in JSON Object Template.
(b) You ensure parsing the JSON object using {config.program_language}'s built-in JSON module would not raise an error exception.
(c) You add nothing else to your response of this request but the JSON object.
(d) escape every special character in the code for json.load to read the JSON object correctly.
'''

comments = '''Your response meets these Comment Requirements:
(1) Your response only includes the JSON object.
(2) You make no comments in your response. 
'''

json_required_format ='''JSON Object Template:
{
"module":"Insert here the code with the enhancements you make leaving no spaces from the beginning to the first character inserted",
"unittest_cli_1":"Insert the command line command to trigger the execution of the corresponding unittest function"
}
'''

unittest_regen_cli_comm_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements":json_object_requirements.replace("\n",""),
    "comments": comments.replace("\n",""),
    "json_required_format": json_required_format.replace("\n",""),
}

