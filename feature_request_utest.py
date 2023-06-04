#!/usr/bin/env python3

#import base class
import feature_base as base
#import utils
import file_management as fm
#import request text
import unittest_rq as u_test

#request add unit test to code
class Feature_Request_Utest(Feature_Base):
	
	def prepare_request_args():
        #get cached response as starting point for unit test
        self.gpt_response_utest = self.gpt_response
        #build args
        summary_new_request = "Add Unit tests to the code."
        sys_mssg = u_test.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.gpt_response_utest}.
        \nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object':
        \n{self.program_description}. {ut.concat_dict_to_string(u_test.unittest_instructions_dict)}'''
        #call base
        self.build_request_args()

    #send request to model
    def request_code(*request_args):
        #override base instance vars
        self.u_test= True
        self.model = oai.codex_engine_deployment_name
        self.model_temp = 0.2
        #run base request implementation
        return self.request_code_enhancement(*request_args, self.u_test)

    def process_successful_response():
        #check unittest commands are valid
        if self.validate_unittest_commands() == False:
            print("Unit test functions not created. Re-create unit test code and cli commands.")
            fm.version_file(self.full_project_dirname, self.module_utest_name, self.full_project_dirname)
            return False
        #unittest commands valid
        mssg = "Unit test functions CLI commands succesfully created."
        #call base
        self.valid_response_file_management(self.module_utest_name, self.full_project_dirname, self.gpt_response_utest, success_mssg=mssg)
        return True

    def validate_unittest_commands(self):
        print(); print("-"*40)
        print("Validating Unittest Function CLI commands were created.")
        num_unittests = 0
        num_unittests = ut.count_values_for_keycontain(self.gpt_response_utest, u_test.unittest_cli_command_key)
        if num_unittests > 0: return True
        else:
            print("Unit test functions not created. Re-create unit test code and cli commands.")
            fm.version_file(self.full_project_dirname, self.module_utest_name, self.full_project_dirname)
            return False