#!/usr/bin/env python3
#add error handling request

import raw_code_rq
import file_management as fm
#TODO move to class var
program_language="Python"

sys_mssg = f'''You are going to add error and exception handling and logging functionality to a script written in {program_language} I give you.
If there is an exception the program terminates gracefully with an error message.
You will not delete any of the code I give you.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
Escape every special character in the code for json.load to read the JSON object correctly.
You must validate the JSON object construct for syntax and parsing the JSON object would not raise an error exception 
according to {program_language}'s built-in JSON module. Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
'''

gpt_task = f'''Your Task:
**Exception Handling**:
(1) add error and exception handling functionality, found in {program_language}'s built in packages, to the code found in this JSON object's value for key 'module' 
without leaving no spaces from the beginning to the first character inserted.
(2) Add code to catch and handle exceptions for every function and no system exit occurs during the program.
(3) If there is an exception the program terminates gracefully with an error message.
(4) Error handling for Input Validation: The program should validate all input and be prepared to handle invalid or unexpected input in a robust way.
**Logging**:
(1) Without removing any print statements from the code, add the necessary handlers to write log records to a file named {fm.modules_dir}/{raw_code_rq.module_log_fname}
(2) Without removing any print statements from the code, record to the log file all program errors info and exceptions and user actions. Add argument exc_info=True to every logging call.
(3) Set log level to debug.
(4) use the built-in logging package
(5) Add Log message format to include the line number in the code where the log statement occurs.
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

err_hndl_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements":json_object_requirements.replace("\n",""),
    "comments": comments.replace("\n",""),
    "json_required_format": json_required_format.replace("\n",""),
}
