#!/usr/bin/env python3
#clean json request

#TODO move to class var
program_language="Python"

sys_mssg = f'''You understand the keys and values of a JSON object used by {program_language} json package.
You must validate the syntax of a JSON object construct and correct it if incorrect, taking care not to change the spacing of keys and values.
Your response to this request exclusively with the corrected JSON object and without any other comments.
'''

gpt_task = f'''Your Task:
Validate the syntax of a JSON object I give you and correct it if is incorrect, taking care not to change the spacing of keys and values.
You use the JSON Object Template as as the required format for the JSON object you will validate and correct.
'''

clean_json_instructions_dict = {
    "gpt_task":gpt_task.replace("\n","")
}