#!/usr/bin/env python3

#import base
import feature_base as base
#import utils
import tools.request_utils as ut
# import openai libs/modules
import openai_params as oai
#import request text
import raw_code_rq as raw_code

#request model raw code from description
class Feature_Request_Rawcode(base.Feature_Base):
	
    def __init__(self):
        super().__init__()  # Call parent class's __init__ method

    def prerequest_args_process(self):
        mssg = "Enter Program Description and Features: "
        self.program_description = self.user_interaction_instance.request_input_from_user(mssg)
        return True

    def prepare_request_args(self):
        #build args
        summary_new_request = "Request raw program code."
        sys_mssg = raw_code.sys_mssg
        request_to_gpt = ut.concat_dict_to_string(raw_code.raw_instructions_dict) + "\n\n" + self.program_description
        #call base
        return self.build_request_args(summary_new_request, sys_mssg, request_to_gpt)

    #send request to model
    def request_code(self, *request_args):
        #override base instance vars
        self.u_test_bool = False
        self.model = oai.gpt_engine_deployment_name
        self.model_temp = 0.7
        #run base request implementation
        return self.request_code_enhancement(*request_args)

    def process_successful_response(self):
        #call base
        self.valid_response_file_management(self.module_script_fname, self.full_project_dirname, self.gpt_response)
        return True
