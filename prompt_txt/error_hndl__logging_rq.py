#!/usr/bin/env python3
#add error handling request

#TODO move to class var
program_language="Python"

sys_mssg = f'''You are going to add error and exception handling and logging functionality to a script written in {program_language} I give you.
You will not delete any of the code I give you.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
You must validate the JSON object construct for syntax and parsing the JSON object would not raise an error exception 
according to {program_language}'s built-in JSON module .
'''

gpt_task = f'''Your Task:
**Exception Handling**:
(1) add error and exception handling functionality, found in {program_language}'s built in packages, to the code found in this JSON object's value for key 'module' 
without leaving no spaces from the beginning to the first character inserted.
(2) Add catch and handle exceptions for every function
(3) Error handling for Input Validation: The program should validate all input and be prepared to handle invalid or unexpected input in a robust way.
(4) add a flag in the module script to enable/disable generating logs. set log level to debug.
**Logging**:
(1) Create a log file with logs of all program and user actions 
(2) name it module.log 
(3) add flag in the module script to enable/disable generating logs. set log level to debug. 
The flag can be set to enable/disabled, set it is enable.
(4) use the built-in logging package
'''

json_object_requirements = f'''Your response to this request is exclusively:
(a) a JSON object with the template described in JSON Required Format Template.
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
"module":"Insert here the code with the enhancements you make leaving no spaces from the beginning to the first character inserted"
}
'''

err_hndl_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements":json_object_requirements.replace("\n",""),
    "comments": comments.replace("\n",""),
    "json_required_format": json_required_format.replace("\n",""),
}