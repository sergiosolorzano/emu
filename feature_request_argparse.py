#!/usr/bin/env python3

#import base
import feature_base as base
#import utils
import file_management as fm
#import request text
import input_and_argparse_rq as input_and_argparse
#import classes
import user_interaction as uinteraction

#request add argparse to code
class Feature_Request_Argparse(Feature_Base):
	
	def prepare_request_args():
        #request args
        summary_new_request = "Add User Input and Argparse functionality to the code."
        sys_mssg = input_and_argparse.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.gpt_response}.
        This is the description of what the program does in the the code found in the value for key 'module' of the JSON object':
        {self.program_description} \n\n{ut.concat_dict_to_string(input_and_argparse.input_and_argparse_instructions_dict)}'''
        #call base
        self.build_request_args()

    #send request to model
    def request_code(*request_args):
        #override base instance vars
        self.u_test= False
        self.model = oai.gpt_engine_deployment_name
        self.model_temp = 0.7
        #run base request implementation
        return self.request_code_enhancement(*request_args, self.u_test)

    def process_successful_response():
        #call base
        self.valid_response_file_management(self.module_script_fname, self.full_project_dirname, self.gpt_response)
        return True