#!/usr/bin/env python3
#send logs to debug program

import raw_code_rq
import file_management as fm
#TODO move to class var
program_language="Python"

sys_mssg = f'''You will change the code to correct the error shown in Error for the script written in {program_language} I give you.
You will keep the changes to the minimum maintaining the structure of the code I give you.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
You must validate the JSON object construct for syntax and parsing the JSON object would not raise an error exception 
according to {program_language}'s built-in JSON module .
'''

command = '''The error shown in Error shows when running the script from terminal on linux with command:'''

error = '''Error:'''

gpt_task = f'''Your Task:
You will change the code to correct the error shown in Error for the script written in {program_language} I give you.
You will keep the changes to the minimum maintaining the structure of the code I give you.
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
"module":"Insert here the code with the changes you make leaving no spaces from the beginning to the first character inserted"
}
'''

debug_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements":json_object_requirements.replace("\n",""),
    "comments": comments.replace("\n",""),
    "json_required_format": json_required_format.replace("\n",""),
}