#!/usr/bin/env python3
#import config
import config as config

#import utils
import tools.request_utils as ut
#import request text
import input_and_argparse_rq as input_and_argparse
#openai
import openai_params as oai
#import config
import config as config

#request add argparse to code
class Feature_Request_Argparse:
    def __init__(self, common_instance):
        self.common_instance = common_instance

    def prerequest_args_process(self):
        return True

    def prepare_request_args(self):
        #request args
        summary_new_request = "Add User Input and Argparse functionality to the code."
        sys_mssg = input_and_argparse.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.common_instance.gpt_response}.
        This is the description of what the program does in the the code found in the value for key 'module' of the JSON object':
        {self.common_instance.program_description} \n\n{ut.concat_dict_to_string(input_and_argparse.input_and_argparse_instructions_dict)}'''
        #call base
        return self.common_instance.build_request_args(summary_new_request,sys_mssg,request_to_gpt)

    #send request to model
    def request_code(self, *request_args):
        #override base instance vars
        self.common_instance.model = oai.gpt_engine_deployment_name
        self.common_instance.model_temp = 0.7
        #run base request implementation
        return self.common_instance.request_code_enhancement(*request_args)

    def process_successful_response(self):
        #call base
        self.common_instance.valid_response_file_management(config.module_script_fname, config.full_project_dirname, self.common_instance.gpt_response)
        return True
