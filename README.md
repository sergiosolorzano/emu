Generates the code for a program description requested by the user using OpenAI API gpt-3.5-turbo and code-davinci-002 models.

Code changes/additions are added on a per-menu-API-request basis.

Selected log entries from running the resulting program are sent to GPT for debug.

This template is being updated to also generate the full program code but requesting from the API atomic modules with the objective of optimizing token expense.

Repo file structure:
```
.
├── config_dir          #file configuration
              ├── config.json         #project file and paths
              ├── config.py           #module with project file and paths
├── creds 			#credentials folder for OpenAI API
│   └── self_config.py 		#OpenAI API credentials. Move sample_self_config.py to be this file and fill credentials data
├── emu_cli.py 			#run this module to run the program
├── feature_common.py 		#common methods for feature requests to API
├── feature_manager.py 		#manager for each feature requested by user in the menu
├── ft_operations 		#non-API requests directory
│   ├── op_loadcode.py 		#loads code from local file to apply code change requests to it
│   ├── op_run_program.py 	#run the code
├── ft_requests 		#feature text requests directory
│   ├── feature_request_argparse.py 		#standard add argparse request
│   ├── feature_request_custom_req.py 		#user enters custom system and request prompt
│   ├── feature_request_debuglogs.py 		#send logs from running the program to API to debug error found in logs
│   ├── feature_request_docstrings.py 		#add docstrings
│   ├── feature_request_excpt_and_log.py 	#add exception handling and logs to the code
│   ├── feature_request_rawcode.py 		#generate initial code from a program description
├── log_list_handler.py 										
├── openai_params.py 				#openai required API parameters
├── project 					#project output directory
│   ├── module.log 
│   ├── module.py 				#code requested stored here and versioned
├── prompt_txt 					#prompt specs directory for each request
│   ├── clean_json_rq.py
│   ├── custom_req.py
│   ├── debug_rq.py
│   ├── docstrings_rq.py
│   ├── error_hndl_logging_rq.py
│   ├── input_and_argparse_rq.py
│   ├── raw_code_rq.py
├── README.md
├── requirements.txt
├── sample_self_config.py
├── tools 					#file and request management utilities directory
│   ├── file_management.py
│   └── request_utils.py
├── user_interaction.py 			#user interaction class
```
---------------------------------------------

Python v3.10+ required
Python required packages: See requirements.txt
Add this package to your sys.path

*Path Change Required:*
Change path to your python environment at config.json: e.g. "python_env_path": "/home/sergio/anaconda3/bin/python"
For path of current env set value to "python"

---------------------------------------------

Authentication:
Create a directory at the root of this project and save sample_self_config.py. Rename this py file to self_config.py and enter your endpoints and keys.

---------------------------------------------

Configuring OpenAI model and temperature per request:
For now set for each request in request_code() e.g. ft_requests/feature_request_argparse.py:
```
    def request_code(self, *request_args):
        #override common instance vars
        self.common_instance.u_test_bool = False
        self.common_instance.model = oai.gpt_engine_deployment_name
        self.common_instance.model_temp = 0.7
        return self.common_instance.request_code_enhancement(*request_args)
```
---------------------------------------------

Execution module: emu_cli.py

1.  Generate Raw Code
		Request model for code according to a description you provide.
2.  Load Raw Code Script From File
3.  Add Argparse
4.  Exception Handling and Logging
5.  User Custom Request
		Requirement: code to be already loaded. A JSON format for the response entered at custom_req.py json_required_format variable.
6.  Run Program And Request Repair of Debug Logs
	Run the program and upon errors send the log error captured for the model to amend the code accordingly.
7.  Add Docstrings To Program Code.
8.  Set Menu Sequence
9.  Run All
10. Exit

Choose your request: 

----------------------------------------------
