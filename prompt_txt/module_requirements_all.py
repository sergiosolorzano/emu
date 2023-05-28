program_language="Python"
must_have_mods=["main.py","user_input_module.py"]
    
#Program Description is the input provided by the user
gpt_task = f'''Your Task: To create a program in {program_language} as shown in Program Description  
by creating program modules as described in "Modules Description". 
Don't give me any code for now.'''

modules_description = f'''Modules Description:
(a) Propose how many independent modules you can create that each performs an independent task for the program. 
(b) Provide a description for each module.
(c) In addition to the above mentioned modules you will also create modules as described in Required Modules.
(d) do not call from {must_have_mods[0]} or {must_have_mods[1]} a sub-function of (1) any module here or (2) Required Modules
(e) Each module will generate logs as described in "Log Requirements".
(f) Add the requirements in Backtesting Requirements to each module.'''

required_modules = f'''Required Modules: Create 
(a) a main module, name it {must_have_mods[0]}, that calls other modules but does not perform any operation by itself 
(b) a {must_have_mods[1]} script that collects all the user input required for the program to complete. 
Ensure user_input_module validates that a user input does not create an exception 
and if it does let the user know the input is not valid and ask again for that input. '''

backtesting_requirements = f'''Backtesting Requirements: This functionality enables testing each module independently with user input.
(1) request inputs from the user 
(a) the inputs required to run each module independently and 
(b) the output the user expects from the module for those inputs. 
(2) At the end of each module when the script completes print on screen "testing output" which includes the expected output 
provided by the user and the script output when the script completes 
(3) a flag in each module script to enable/disable testing a module. This flag is enable/disabled from the script itself and from {must_have_mods[0]}'''

create_logs = f'''Log Requirements: Add to the description of all modules that (a) all program or user actions are recorded 
into a log file named <module_name>.log (b) a flag in each module script to enable/disable generating logs. set log level to debug. 
The flag can be set enable/disabled from {must_have_mods[0]}'''

final_orders = '''Don't forget: (1) At the beginning of your answer give me a list for all module scripts title "List of Modules:"
with each filename separated by ","'''

required_format = '''
Do not return any non-Json in your response. Create a JSON object for your response. Very Important: Use this template format for your json, so expand it with the modules and features you propose.:
{
    "List of Modules":"main.py, user_input_module.py",
    "modules":[
    {"main.py":"calls other modules to perform the operations but does not perform any operation by itself."},
    {"user_input_module.py":"collects all the user input required for the program to complete and validates the input to avoid exceptions."}
    ],
    "Backtesting Requirements":[
    "Request user input: For each module, the user must input the required inputs to run the module independently and the expected output of the module for those inputs."
    ],
    "Log Requirements":[
    "All module and user actions are recorded into a log file named <module_name>_log."
    ],
    "End":"*****End of Response*****"
}
'''


module_requirements_dict = {
    "modules_description" : modules_description.replace("\n",""),
    "required_modules" : required_modules.replace("\n",""),
    "backtesting_requirements" : backtesting_requirements.replace("\n",""),
    "create_logs" : create_logs.replace("\n",""),
    "final_orders" : final_orders.replace("\n",""),
    "required_format" : required_format.replace("\n","")
}
