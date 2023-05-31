#!/usr/bin/env python3
#add input and argparse

#TODO move to class var
program_language="Python"

sys_mssg = f'''You are going to add user input and argparse functionality to a script written in {program_language} I give you.
You will not delete any of the code I give you.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
You must validate the JSON object construct for syntax.
You ensure parsing the JSON object using {program_language}'s built-in JSON module would not raise an error exception.
'''

gpt_task = f'''Your Task:
(1) add user input and argparse functionality to the code found in this JSON object's value for key 'module' 
without leaving no spaces from the beginning to the first character inserted.
(2) Add the code for the function program() to have user input and be executed in a statement __name__ == '__main__'.
(3) Add Argparse with version, set version = 1.0, and help only for program() intput arguments.
Create the argparse input help for each individual argument in program().
(4) Code argparse to display help with any arguments required to execute program() and a description for these arguements.
'''

json_object_requirements = f'''Your response to this request is exclusively:
(a) a JSON object with the template described in JSON Required Format Template.
(b) You ensure parsing the JSON object using {program_language}'s built-in JSON module would not raise an error exception.
(c) You add nothing else to your response of this request but the JSON object.
'''

comments = '''Your response meets these Comment Requirements:
(1) Your response only includes the JSON object.
(2) You make no comments in your response. 
(3) Keep comments within the code to the bare minimum"
'''

json_required_format ='''JSON Object Template:
{
"module":"Insert here the code with the enhancements you make leaving no spaces from the beginning to the first character inserted"
}
'''

input_and_argparse_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements":json_object_requirements.replace("\n",""),
    "comments": comments.replace("\n",""),
    "json_required_format": json_required_format.replace("\n",""),
}