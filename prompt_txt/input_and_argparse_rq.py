#!/usr/bin/env python3
#add input and argparse

#TODO move to class var
program_language="Python"
language_version = "3.10"

sys_mssg = f'''You are going to add argparse arguments functionality to a script written in {program_language} version above {language_version} I give you.
Important: Do not include required=True in argparse's add_argument(), e.g. parser.add_argument('num1', type=float, help='First number').
You will not delete any of the code I give you.
Do not add arguments of the form parser.add_argument -foo and --foo.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
You must validate the JSON object construct for syntax.
You ensure parsing the JSON object using {program_language}'s built-in JSON module would not raise an error exception.
Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
Escape every special character in the code for json.load to read the JSON object correctly.
'''

gpt_task = f'''Your Task:
(1) add argparse arguments functionality for the program to run to the code found in this JSON object's value for key 'module' 
without leaving no spaces from the beginning to the first character inserted.
(2) Important: Do not include required=True in argparse's add_argument(), e.g. parser.add_argument('num1', type=float, help='First number').
(3) Do not add arguments of the form parser.add_argument -foo and --foo.
(4) Add the code for the function program() to have user input and be executed in a statement __name__ == '__main__'.
(5) Add Argparse arguments for version (version = 1.0) and help only for program() arguments.
Create the argparse input help for each individual argument in program().
(6) Code argparse to display help with the arguments to execute program() and a description for these arguements.
'''

json_object_requirements = f'''Your response to this request is exclusively:
(a) a JSON object with the template described in JSON Object Template.
(b) You ensure parsing the JSON object using {program_language}'s built-in JSON module would not raise an error exception.
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
"module":"Insert here the code with the enhancements you make leaving no spaces from the beginning to the first character inserted"
}
'''

input_and_argparse_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements":json_object_requirements.replace("\n",""),
    "comments": comments.replace("\n",""),
    "json_required_format": json_required_format.replace("\n",""),
}
