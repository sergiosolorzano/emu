#!/usr/bin/env python3

#import utils
import tools.request_utils as ut
#import request text
import error_hndl_logging_rq as error_log_hndl
#openai
import openai_params as oai
#import config_dir
from config_dir import config as config


#request model raw code from description
class Feature_Request_ExceptionHndl_and_Logging:

    def __init__(self, common_instance):
        self.common_instance = common_instance

    def prerequest_args_process(self):
        # send additional requests, not back to menu
        return True, False

    def prepare_request_args(self):
        #request args
        summary_new_request = "Add Logs and Exception Handling to the code."
        sys_mssg = error_log_hndl.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.common_instance.gpt_response}.
        \nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object:\n
        {self.common_instance.program_description}\n\n{ut.concat_dict_to_string(error_log_hndl.err_hndl_instructions_dict)}'''
        #call base
        return self.common_instance.build_request_args(summary_new_request,sys_mssg,request_to_gpt)

    #send request to model
    def request_code(self, *request_args):
        #override base instance vars
        self.common_instance.model = oai.primary_engine_deployment_name
        self.common_instance.model_temp = 0.2
        #call base
        return self.common_instance.request_code_enhancement(*request_args)

    def process_successful_response(self):
        #call base
        self.common_instance.valid_response_file_management(config.module_script_fname, config.full_project_dirname, self.common_instance.gpt_response)
        return True
