#!/usr/bin/env python3
#import config
import config as config

#user custom request to gpt
sys_mssg = f'''Apply the following changes to a script written in {config.program_language} I give you.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
You must validate the JSON object construct for syntax and parsing the JSON object would not raise an error exception 
according to {config.program_language}'s built-in JSON module.
Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
Multi-line strings within the code must be enclosed in triple quotes.
Escape every special character in the code for json.load to read the JSON object correctly.
'''

json_object_requirements = f'''Your response to this request is exclusively:
(a) a JSON object with the template described in JSON Object Template.
(b) You ensure parsing the JSON object using {config.program_language}'s built-in JSON module would not raise an error exception.
(c) You add nothing else to your response of this request but the JSON object.
(d) escape every special character in the code for json.load to read the JSON object correctly.
'''

comments = '''.Your response meets these Comment Requirements:
(1) Your response only includes the JSON object.
(2) You make no comments in your response. 
(3) Keep comments within the code to the bare minimum"
'''

json_required_format ='''
{
"module":"Insert here the code you produced as described in Program Description leaving no spaces from the beginning to the first character inserted"
}
'''