#!/usr/bin/env python3

#import base
import feature_base as base
#import utils
import file_management as fm
#import request text
import docstrings_rq.py as docs_r
#import classes
import user_interaction as uinteraction

#request add docstrings to code
class Feature_Request_Docstrings(Feature_Base):
	
	def prepare_request_args():
        #request args
        summary_new_request = "Add docstrings to the script."
        sys_mssg = docs_r.sys_mssg
        request_to_gpt = f'''You will make specific changes to the module key of this JSON object: {self.gpt_response}.\n
        {ut.concat_dict_to_string(docs_r.docstrings_instructions_dict)}'''
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