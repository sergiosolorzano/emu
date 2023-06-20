#!/usr/bin/env python3
#import config
import config as config

#add docstrings
sys_mssg = f'''You are going to add docstrings to a script written in {config.program_language} I give you.
You will not delete any of the code I give you.
Your response to this request is exclusively a JSON object using the JSON Object Template provided.
Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
Do not use multi-line in the code you create. Escape every special character in the code for json.load to read the JSON object correctly.
You must validate the JSON object construct in your response for syntax. Do not enclose anything either at the beginning or the end in the JSON Object with three double (""") or single quotes.
You ensure parsing the JSON object in your response using {config.program_language}'s built-in JSON module would not raise an error exception.
'''
#Multi-line strings within the code must be enclosed in triple quotes.
gpt_task = f'''Specifications for your Task to add docstrings to the script:
Purpose: Every function, class, and module should start with a concise summary of its purpose or behavior. This should be a brief, one-line explanation.
Parameters: For functions or methods, describe each input parameter (name and expected type), explaining what it represents and any assumptions or constraints about its value.
Return Value: Describe the type and meaning of the value returned by the function or method. If the function doesn't return anything (returns None), this should also be mentioned.
Exceptions: Document any errors that the function or method can raise. Explain the conditions under which they are raised.
Usage Examples: Include a simple example showing a common usage of the function or method. This can be particularly useful for complex functions.
Remember, the goal of the docstring is to help other developers understand the purpose and usage of the code without having to read the actual implementation.
Do not use multi-line anywhere in the code.
'''

json_object_requirements = f'''Your response to this request is exclusively:
(a) a JSON object with the template described in JSON Object Template.
(b) You ensure parsing the JSON object using {config.program_language}'s built-in JSON module would not raise an error exception.
(c) escape every special character in the code for json.load to read the JSON object correctly.
(d) You add nothing else to your response of this request but the JSON object.
'''

json_required_format ='''JSON Object Template:
{
"module":"Insert here the code with the enhancements you make leaving no spaces from the beginning to the first character inserted",
"unittest_cli_1":"Insert the command line command to trigger the execution of the corresponding unittest function"
}
'''

docstrings_instructions_dict = {
    "gpt_task":gpt_task.replace("\n",""),
    "json_object_requirements": json_object_requirements.replace("\n",""),
    "json_required_format": json_required_format.replace("\n",""),
}
