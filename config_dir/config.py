#!/usr/bin/env python3

import os
import json
import openai
from creds.self_config import self_config_azure_openai
from creds.self_config import self_config_openai_api

#read config_dir data
path_to_file = os.getcwd()+"/config_dir/config.json"
with open(path_to_file) as f:
    config_data = json.load(f)

#set default (fall back unless specified) api for this session
class Model_API:
    #avaialble APIs
    AZURE_OPENAI_API=0
    OPENAI_API=1

    @staticmethod
    def runtime_set_openai_credentials(model_api):
        if model_api == Model_API.AZURE_OPENAI_API:
            # set azure openai credentials
            openai.api_type = self_config_azure_openai['OPENAI_API_TYPE']
            openai.api_version = self_config_azure_openai['OPENAI_API_VERSION']
            openai.api_base = self_config_azure_openai['OPENAI_API_BASE']
            openai.api_key = self_config_azure_openai['OPENAI_API_KEY']
        elif model_api == Model_API.OPENAI_API:
            openai.organization = self_config_openai_api['OPENAI_ORGANIZATION']
            openai.api_key = self_config_openai_api['OPENAI_API_KEY']

#default starting session API, re-assigned by request
used_api = Model_API.AZURE_OPENAI_API

# model keys must match those entered in self_config.py
class Azure_OpenAI_Model:
    gpt35_deployment_name = self_config_azure_openai["gpt_engine_350301_deployment_name"]
    codex_deployment_name = self_config_azure_openai["codex_engine_002_deployment_name"]
    davincitext_deployment_name = self_config_azure_openai["davincitext_003_deployment_name"]

    gpt35_model_name = self_config_azure_openai["gpt_engine_350301_name"]
    codex_model_name = self_config_azure_openai["codex_engine_002_name"]
    davincitext_model_name = self_config_azure_openai["davincitext_engine_003_name"]

# model keys must match those entered in self_config.py
class OpenAI_Model:
    gpt35_deployment_name = self_config_openai_api["gpt_engine_350613_deployment_name"]
    codex_deployment_name = self_config_openai_api["codex_engine_002_deployment_name"]
    davincitext_deployment_name = self_config_openai_api["davincitext_003_deployment_name"]

    gpt35_model_name = self_config_openai_api["gpt_engine_350613_name"]
    codex_model_name = self_config_openai_api["codex_engine_002_name"]
    davincitext_model_name = self_config_openai_api["davincitext_engine_003_name"]

##---Required to be set by user---
#set API that corresponds to model
request_argparse_api=Model_API.AZURE_OPENAI_API
request_custom_req_api=Model_API.AZURE_OPENAI_API
request_debuglogs_api=Model_API.AZURE_OPENAI_API
request_docstrings_api=Model_API.AZURE_OPENAI_API
request_excpt_and_logs_api=Model_API.AZURE_OPENAI_API
request_rawcode_api=Model_API.AZURE_OPENAI_API

#set model for each request feature
model_request_argparse = (Azure_OpenAI_Model.gpt35_deployment_name,Azure_OpenAI_Model.gpt35_model_name)
model_request_custom_req = (Azure_OpenAI_Model.gpt35_deployment_name,Azure_OpenAI_Model.gpt35_model_name)
model_request_debuglogs = (Azure_OpenAI_Model.codex_deployment_name,Azure_OpenAI_Model.codex_model_name)
model_request_docstrings = (Azure_OpenAI_Model.gpt35_deployment_name,Azure_OpenAI_Model.gpt35_model_name)
model_request_excpt_and_logs = (Azure_OpenAI_Model.gpt35_deployment_name,Azure_OpenAI_Model.gpt35_model_name)
model_request_rawcode = (Azure_OpenAI_Model.gpt35_deployment_name,Azure_OpenAI_Model.gpt35_model_name)

#set model temperature
model_request_argparse_temperature = 0.7
model_request_custom_req_temperature = 0.7
model_request_debuglogs_temperature = 0.4
model_request_docstrings_temperature = 0.7
model_request_excpt_and_logs_temperature = 0.2
model_request_rawcode_temperature = 0.7
##---End Required to be set by user---

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

#full path files
full_custom_json_format_fname = f"{initial_dir}/{custom_json_format_dirname}/{custom_json_format_fname}"
full_path_module = f"{full_project_dirname}/{module_script_fname}"
full_path_logfile = f"{full_project_dirname}/{log_fname}"

#key in json file to get the code
code_key_in_json = module_script_fname.split(".")[0]

# program language
program_language = config_data["program_language"]
language_version = config_data["language_version"]

#unit test cli key TODO
unittest_cli_command_key = config_data["unittest_cli_command_key"]

#openai tokens
max_response_tokens=config_data["openai_tokens"]["max_response_tokens"]
token_limit=config_data["openai_tokens"]["token_limit"]

#python path with required environment
python_env_path = config_data["python_env_path"]

#show requests on terminal
show_request = True




