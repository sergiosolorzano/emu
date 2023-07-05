Generates the code for a program description requested by the user using Azure OpenAI API gpt-3.5-turbo and code-davinci-002 models.

Code changes/additions are added on a per-menu-API-request basis.

Selected log entries from running the resulting program are sent to GPT for debug.

<video src="https://github.com/sergiosolorzano/emu/assets/24430655/bb6f7a3c-b6de-4abe-870d-866651a1536e" controls="controls" muted="muted" playsinline="playsinline">
      </video>

---------------------------------------------
```
Repo file structure:

.
├── config_dir          #file configuration
      ├── config.json         #project files, paths, token limits metadata 
      ├── config.py           #set by user API, model, temperature for each request
├── creds 			#credentials folder for OpenAI API
│   └── self_config.py 		#Azure OpenAI API credentials & model names metadata
                                        #Move sample_self_config.py to self_config.py and fill data
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
Create "creds" directory at the root of this project and save in it sample_self_config.py. Rename this py file to self_config.py and enter your endpoints, model/deployment names and keys.
Project tested with Azure OpenAI API. Untested OpenAI API.

---------------------------------------------

Configuring OpenAI model and temperature per request:
- Model keys for class class Azure_OpenAI_Model and OpenAI_Model must match model keys used in self_config.py
- Set API that corresponds to model, e.g.
    request_argparse_api=Model_API.AZURE_OPENAI_API
- Set model for each request type, e.g.:
    model_request_argparse = (Azure_OpenAI_Model.gpt35_deployment_name,Azure_OpenAI_Model.gpt35_model_name)
- Set model temperature for each request type, e.g.:
    model_request_argparse_temperature = 0.7

---------------------------------------------

Execution of this program: 
At command line ./emu_cli.py shows menu:
```
1.  Generate Raw Code
        Request model for code according to a description you provide.
2.  Load Raw Code Script From File
3.  Add Argparse
4.  Exception Handling and Logging
5.  User Custom Request
        Requirement: code to be already loaded. Expected JSON response as specified in custom_req.py json_required_format variable.
6.  Run Program And Request Repair of Debug Logs
        Run the program and upon errors send the log error captured for the model to amend the code accordingly.
7.  Add Docstrings To Program Code.
8.  Set Menu Sequence
9.  Run All
10. Exit

Choose your request: 
```

----------------------------------------------

Toggle to show the prompt for each requests: At config_dir/config.py toggle bool show_request
