#!/usr/bin/env python3

import os
import json

#read config data
with open("config.json") as f:
    config_data = json.load(f)

#dir names
initial_dir = os.getcwd()
root = os.getenv("HOME")
prompt_dirname = config_data["folder_locations"]["prompt_dirname"]
project_dirname = config_data["folder_locations"]["project_dirname"]
json_dirname = config_data["folder_locations"]["json_dirname"]
custom_json_format_dirname = config_data["folder_locations"]["custom_json_format_dirname"]

# full dir paths
full_prompt_dirname = f"{initial_dir}/{prompt_dirname}"
full_project_dirname = f"{initial_dir}/{project_dirname}"
full_json_dir = f"{initial_dir}/{json_dirname}"
full_custom_json_format_dirname = f"{initial_dir}/{custom_json_format_dirname}"

# filenames
module_script_fname = config_data["file_names"]["module_script_fname"]
log_fname = config_data["file_names"]["log_fname"]
module_utest_name = config_data["file_names"]["module_utest_name"]
json_fname = config_data["file_names"]["json_fname"]
custom_json_format_fname = config_data["file_names"]["custom_json_format_fname"]
#key in json file to get the code
code_key_in_json = module_script_fname.split(".")[0]

#full path files
full_custom_json_format_fname = f"{initial_dir}/{custom_json_format_dirname}/{custom_json_format_fname}"
full_path_module = f"{full_project_dirname}/{module_script_fname}"
full_path_logfile = f"{full_project_dirname}/{log_fname}"

# program language
program_language = config_data["program_language"]
language_version = config_data["language_version"]

#unit test cli key
unittest_cli_command_key = config_data["unittest_cli_command_key"]

#openai tokens
max_response_tokens=config_data["openai_tokens"]["max_response_tokens"]
token_limit=config_data["openai_tokens"]["token_limit"]

#python path with required environment
python_env_path = config_data["python_env_path"]
