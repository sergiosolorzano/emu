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

#import self module
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


class Request_Feature:
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
	json_fname = "response.json"
	custom_json_fname = "custom_json.json"

	#paths
	root = os.getenv("HOME")
	prompt_dirname = "prompt_txt"
	project_dirname = "project"
	json_dirname = "response_json"
	custom_json_dirname = "custom_json"
	
	#program language
	program_language="Python"

	#program description
	program_description ="No description provided"

    def __init__(self,program_description="No description provided.", gpt_response="No response provided."):
        self.gpt_response = gpt_response
        self.gpt_response_utest = gpt_response

    #request module code
    def send_request(self, sys_mssg, request_to_gpt, summary_new_request, u_test = False, new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name):
        #set engine
        tmp_deployment_name = oai.deployment_name
        oai.deployment_name = new_engine
        #set engine temp
        temp_oai_temp =  oai.temperature
        oai.temperature = new_temp

        this_conversation =[]

        system_message = {"role": "system", "content": sys_mssg}

        this_conversation.append(system_message)

        #request requirements
        this_conversation.append({"role": "user", "content": request_to_gpt})
        
        request_tokens = this_conversation_tokens = ut.num_tokens_from_messages(this_conversation)

        ut.token_limit(request_tokens)

        oai.cum_tokens += this_conversation_tokens
        
        #if show_request: #TODO: show on screen the request or not
        print(); print("-"*40)
        print();print(f"\033[44;97mJob Request: {summary_new_request}\033[0m")
        if self.get_show_request():
            print(f"\n\033[1;97mRequest: CumTokens:{oai.cum_tokens} Req_Tokens:{request_tokens}\033[0m: {request_to_gpt}")
        else:
            print(f"\n\033[1;97mRequest Sent: CumTokens:{oai.cum_tokens} Req_Tokens:{request_tokens}\033[0m")
        
        print(); print(f"\033[1;97mModel Settings:\033[0m Engine: {oai.deployment_name[1]}, Temperature: {oai.temperature}")

        #start timer
        stop_event = threading.Event()
        thread = threading.Thread(target=ut.spinning_timer, args=("Awaiting Response...",stop_event))
        thread.start()

        response = oai.openai.ChatCompletion.create(
            engine=oai.deployment_name[0], # The deployment name you chose when you deployed the model.
            messages = this_conversation,
            temperature=oai.temperature,
            max_tokens=oai.max_response_tokens,
        )

        clean_response = response['choices'][0]['message']['content'].replace("'''","'").replace('"""','"').replace('```', '`')

        #stop timer
        stop_event.set()
        thread.join()
        print('\r\033[K', end='')  # Clear the line

        this_conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        this_conversation_tokens = ut.num_tokens_from_messages(this_conversation)
        oai.cum_tokens += this_conversation_tokens

        ut.token_limit(this_conversation_tokens)

        #re-set engine
        oai.deployment_name = tmp_deployment_name
        #re-set temp
        oai.temperature = temp_oai_temp

        print("-"*40);
        try:
            pretty_json_response = json.dumps(json.loads(clean_response), indent=2, separators=(',', ':')) #.replace('```', '')
            print(f"\n\033[1;92mResponse: CumTokens:{oai.cum_tokens} RespTokens:{this_conversation_tokens}\n\033[0m\033[92m{pretty_json_response}\n\033[0m")
        except Exception as e:
            print(f"Exception on JSON Received: {e}: {clean_response:<10} \n")
            print(); print("RAW print:",clean_response)
            print("-"*40);
            #JSON invalid, re-request or quit
            return False

        if u_test:
            self.gpt_response_utest = json.loads(clean_response) #.strip("\n") #.replace('```', '')
        else:
            self.gpt_response = json.loads(clean_response) #.strip("\n")  #.replace('```', '')

        return True