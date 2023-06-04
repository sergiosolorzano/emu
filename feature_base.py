#!/usr/bin/env python3

#import libraries
import sys
import os
import subprocess
import shlex
import time
import threading
from pathlib import Path
import json

#import module
import file_management as fm

#TODO: create dirs module
sys.path.append(fm.m_root)
sys.path.append(f'{fm.initial_dir}/{fm.m_prompt_dirname}')

#import openai libs/modules
import tiktoken
import openai
import openai_params as oai

#import data to request module code
#import request requirements
import raw_code_rq as raw_code
import clean_json_rq as clean_json
import input_and_argparse_rq as input_and_argparse
import error_hndl__logging_rq as error_log_hndl
import unittest_rq as u_test
import unittest_cli_comm_rq as unittest_cli_comm
import custom_req as c_r
import docstrings_rq as docs_r
import debug_rq as dg_r
#import my utils
import request_utils as ut


class Feature_Base:
    #show request text on screen
    show_request = True

    #set model and temp
    model = oai.gpt_engine_deployment_name
    model_temp = 0.7
    
    #model token settings
	cum_tokens = 0
	max_response_tokens = 3000
	token_limit= 4096

    #filenames
    module_script_fname = "module.py"
	log_fname = "module.log"
    module_utest_name = "module_utest.py"
	json_fname = "response.json"
	custom_json_fname = "custom_json.json"

	#paths
    initial_dir = os.getcwd()
	root = os.getenv("HOME")
	prompt_dirname = "prompt_txt"
	project_dirname = "project"
	json_dirname = "response_json"
	custom_json_dirname = "custom_json"
    #full dir paths
    full_prompt_dirname = f"{initial_dir}/{prompt_dirname}"
    full_project_dirname=f"{initial_dir}/{project_dirname}"
    full_json_dir = f"{initial_dir}/{json_dirname}"
    full_custom_json_dirname = f"{initial_dir}/{custom_json_dirname}"

	#program language
	program_language="Python"

	#program description
	program_description ="No description provided"

    def get_gpt_response(self):
        return self.gpt_response

    def __init__(self):
        super().__init__(program_description=None)
        if program_description is not None
            self.program_description = program_description


    def __init__(self,program_description="No description provided.", gpt_response="No response provided."):
        self.gpt_response = gpt_response
        self.gpt_response_utest = gpt_response

    #request module code
    def send_request(self, sys_mssg, request_to_gpt, summary_new_request, u_test = False):
        this_conversation =[]

        system_message = {"role": "system", "content": sys_mssg}

        this_conversation.append(system_message)

        #request requirements
        this_conversation.append({"role": "user", "content": request_to_gpt})
        
        request_tokens = this_conversation_tokens = ut.num_tokens_from_messages(this_conversation)

        ut.token_limit(request_tokens)

        self.cum_tokens += this_conversation_tokens
        
        #if show_request: #TODO: show on screen the request or not
        print(); print("-"*40)
        print();print(f"\033[44;97mJob Request: {summary_new_request}\033[0m")
        if self.show_request:
            print(f"\n\033[1;97mRequest: CumTokens:{self.cum_tokens} Req_Tokens:{request_tokens}\033[0m: {request_to_gpt}")
        else:
            print(f"\n\033[1;97mRequest Sent: CumTokens:{self.cum_tokens} Req_Tokens:{request_tokens}\033[0m")
        
        print(); print(f"\033[1;97mModel Settings:\033[0m Engine: {self.model[1]}, Temperature: {self.model_temp}")

        #start timer
        stop_event = threading.Event()
        thread = threading.Thread(target=ut.spinning_timer, args=("Awaiting Response...",stop_event))
        thread.start()

        response = oai.openai.ChatCompletion.create(
            model=self.model[0], # The deployment name you chose when you deployed the model.
            messages = this_conversation,
            temperature=self.model_temp,
            max_tokens=self.max_response_tokens,
        )

        clean_response = response['choices'][0]['message']['content'].replace("'''","'").replace('"""','"').replace('```', '`')

        #stop timer
        stop_event.set()
        thread.join()
        print('\r\033[K', end='')  # Clear the line

        this_conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        this_conversation_tokens = ut.num_tokens_from_messages(this_conversation)
        self.cum_tokens += this_conversation_tokens

        ut.token_limit(this_conversation_tokens)

        print("-"*40);
        try:
            pretty_json_response = json.dumps(json.loads(clean_response), indent=2, separators=(',', ':')) #.replace('```', '')
            print(f"\n\033[1;92mResponse: CumTokens:{self.cum_tokens} RespTokens:{this_conversation_tokens}\n\033[0m\033[92m{pretty_json_response}\n\033[0m")
        except Exception as e:
            print(f"Exception on JSON Received: {e}: {clean_response:<10} \n")
            print(); print("RAW print:",clean_response)
            print("-"*40);
            #JSON response invalid, re-request or quit
            return False

        if u_test:
            self.gpt_response_utest = json.loads(clean_response) #.strip("\n") #.replace('```', '')
        else:
            self.gpt_response = json.loads(clean_response) #.strip("\n")  #.replace('```', '')

        #JSON response valid
        return True

    def build_request_args(self):
        self.summary_new_request = self.sys_mssg = self. request_to_gpt = None
        args_tpl = (summary_new_request,sys_mssg,request_to_gpt)
        return args_tpl

    #manage request
    def request_code_enhancement(self, *request_args, u_test):
        #unpack request args for clarity
        summary_new_request,sys_mssg,request_to_gpt = request_args
        #send request to model
        return self.send_request(sys_mssg, request_to_gpt, summary_new_request, u_test)

    def valid_response_file_management(self, filename, full_path_dir, gpt_response, success_mssg = None):
        print(f"\033[43m{success_mssg}\033[0m")
        #version and save
        fm.version_file(full_path_dir, filename, full_path_dir)
        fm.get_dict_value_save_to_file(gpt_response, self.initial_dir, filename, "#!/usr/bin/env python3\n\n")
        #TODO: remove for debugging
        #fm.write_to_file(self.json_fname, self.json_dirname, gpt_response, "w")
        #end remove for debugging

    def get_file_path_from_user(self, mssg):
        while True:
            full_path_to_file = uinteraction.request_input_from_user(mssg)
            if fm.validate_filepath(full_path_to_file) == False
                continue
            else
                return full_path_to_file

    def read_code_from_file(self, full_path_to_script):
        #read script
        code = fm.read_file_stored_to_buffer(os.path.basename(full_path_to_script), os.path.dirname(full_path_to_script))
        return code

        fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir, raw_code.module_name)








# @classmethod
#     def set_show_request(self, show_req):
#         self.show_request = show_req
    
#     #file name settings
#     @classmethod
#     def set_log_fname(self, fn):
#         self.log_fname = fn

#     @classmethod
#     def set_module_script_fname(self, fn):
#         self.module_script_fname = fn

#     @classmethod
#     def set_custom_json_fname(self, fn):
#         self.custom_json_fname = fn
    
#     #directory settings
#     @classmethod
#     def set_project_dirname(self, dn):
#         self.project_dirname = dn

#     @classmethod
#     def set_json_dirname(self, dn):
#         self.json_dirname = dn

#     @classmethod
#     def set_custom_json_dirname(self, dn):
#         self.custom_json_dirname = dn

#     @classmethod
#     def set_program_description(self, prog_desc):
#         self.program_description = prog_desc