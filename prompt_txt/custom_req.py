#!/usr/bin/env python3
#user custom request to gpt

#TODO move to class var
program_language="Python"

sys_mssg = f'''Apply the following changes to a script written in {program_language} I give you.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
You must validate the JSON object construct for syntax and parsing the JSON object would not raise an error exception 
according to {program_language}'s built-in JSON module .
'''

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