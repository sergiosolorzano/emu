#!/usr/bin/env python3

#import utils
import tools.file_management as fm
import tools.request_utils as ut
#import request text
import prompt_txt.docstrings_rq as docs_r
#openai
import openai_params as oai
#import config
import config as config

#request add docstrings to code
class Feature_Request_Docstrings:

    def __init__(self, common_instance):
        self.common_instance = common_instance

    def prerequest_args_process(self):
        return True, False

    def prepare_request_args(self):
        #request args
        summary_new_request = "Add docstrings to the script."
        sys_mssg = docs_r.sys_mssg
        request_to_gpt = f'''You will make specific changes to the module key of this JSON object: {self.common_instance.gpt_response}.\n
        {ut.concat_dict_to_string(docs_r.docstrings_instructions_dict)}'''
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
