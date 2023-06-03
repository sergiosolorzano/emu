#!/usr/bin/env python3

import feature_base as base

class Feature_Request_Utest(Feature_Base):
	
	@classmethod
    def set_show_request(self, show_req):
    	self.show_request = show_req
    
    #file name settings
    @classmethod
    def set_log_fname(self, fn):
    	self.log_fname = fn

    @classmethod
    def set_module_script_fname(self, fn):
    	self.module_script_fname = fn

    @classmethod
    def set_custom_json_fname(self, fn):
    	self.custom_json_fname = fn
    
    #directory settings
	@classmethod
    def set_project_dirname(self, dn):
    	self.project_dirname = dn

    @classmethod
    def set_json_dirname(self, dn):
    	self.json_dirname = dn

    @classmethod
    def set_custom_json_dirname(self, dn):
    	self.custom_json_dirname = dn

    @classmethod
    def set_program_description(self, prog_desc):
        self.program_description = prog_desc

    def __init__(self):
		super().__init__(program_description=None)
        if program_description is not None
        	self.program_description = program_description
		
	def build_unittest_request_args():
        #get cached response as starting point for unit test
        self.gpt_response_utest = self.gpt_response
        #build args
        summary_new_request = "Add Unit tests to the code."
        sys_mssg = u_test.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.gpt_response_utest}.
        \nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object':
        \n{self.program_description}. {ut.concat_dict_to_string(u_test.unittest_instructions_dict)}'''
        self.build_request_args()

    #send request to model
    def request_code(*request_args):
        #override base instance vars
        self.u_test= True
        self.model = oai.codex_engine_deployment_name
        self.model_temp = 0.7
        #run base request implementation
        return self.request_code_enhancement(*request_args, self.u_test)
