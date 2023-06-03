#!/usr/bin/env python3

import request_feature as parent

class Request_Utest(Request_Feature):
	
	@classmethod
    def set_show_request(self, show_req):
    	self.show_request = show_req
    
    #model settings
    @classmethod
    def set_model_and_temperature(self, model, temp):
    	self.model = model
    	self.model_temp = temp
    
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

    def __init__(self):
		super().__init__(program_description=None)
        if program_description is not None
        	self.program_description = program_description
		
	

