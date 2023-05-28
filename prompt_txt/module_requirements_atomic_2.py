#!/usr/bin/env python3

program_language="Python"

module_name = "module.py"

gpt_task = f'''Your Task: To amend {module_name} in {program_language} as shown in Amendments.
Your respond with a JSON object with the template described in Required Format Template'''

backtest_number_key = "number_backtest_cli"

backtest_cli_command_key = "backtest_cli_"

no_comments = "Comment Requirements: Don't provide comments in your code"

module_additions = '''Amendments:
(a) logs as described in 'Log Requirements'.
(b) the requirements described in 'Backtesting Requirements'
(c) the requirements described in 'Required Format Template'
(d) include in your code error handling for all user input
'''
backtesting_requirements = '''Backtesting Requirements:
(1) add to the main code if __name__ == "__main__": statement to execute any backtesting function from the command line
(2) Add to all 
(2) when the backtesting function is run and at the end of its execution show on screen:
(a) the function name
(b) "backtest output:" with the output from running the function 
(c) "expected_output:"with the expected output from the user
(3) compare the backtest output and the expected output and print Success if these match else Fail.
'''

create_logs = f'''Log Requirements: 
(a) Create a log file with logs of all program and user actions 
(b) name it module.log 
(c) add flag in the module script to enable/disable generating logs. set log level to debug. 
The flag can be set to enable/disabled
(d) use the built-in logging package'''

required_format = '''
Required Format Template: Your response includes only a JSON object. Add your code to the module.py property. This is your JSON Template, wrap key and value in "":
{
"module":"Insert the code you generate in here leaving no spaces from the beginning to the first character inserted",
"backtest_cli_1":"Insert the command line command to trigger the execution of a backtesting function",
"number_backtest_cli":"Insert the number of backtest command lines as an integer, e.g. if you create up to backtest_cli_3, insert 3 as an integer"
}
'''

review = '''Once you have created the code, check that each and every requirement is met in your code:
(1) Your Task description
(2) the code meets the Program Description
(3) your code meets the following requirements:
(a) Backtesting Requirements
(b) Log Requirements
(c) Comment Requirements
(3) your JSON object response meets the format as shown in the example of Required Format Template.

'''

module_instructions_dict = {
    #"module_additions":module_additions.replace("\n",""),
    "backtesting_requirements":backtesting_requirements.replace("\n",""),
    "create_logs":create_logs.replace("\n",""),
    "required_format": required_format.replace("\n",""),
    "no_comments": no_comments.replace("\n",""),
    "review": review.replace("\n","")
}


# (2) Each backtesting function prompts the user with method input() for:
# (a) (a.1) the inputs to run each function and (a.2) a short explanation of each input and choices available
# (b) for the output the user expects for those inputs