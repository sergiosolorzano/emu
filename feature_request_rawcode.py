#!/usr/bin/env python3

#import base
import feature_base as base
#import utils
import file_management as fm
#import request text
import raw_code_rq as raw_code
#import classes
import user_interaction as uinteraction

#request model raw code from description
class Feature_Request_Rawcode(Feature_Base):
	
	def prepare_request_args():
        mssg= "Program Description: Enter Program Description and Features: "
        self.program_description = uinteraction.userinput_program_description(mssg)
        #build args
        summary_new_request = "Request raw program code."
        sys_mssg = raw_code.sys_mssg
        request_to_gpt = ut.concat_dict_to_string(raw_code.raw_instructions_dict) + "\n\n" + self.program_description
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