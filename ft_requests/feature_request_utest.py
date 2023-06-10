#!/usr/bin/env python3
#import base class
import feature_common as base
#import utils
import tools.file_management as fm
import tools.request_utils as ut
#openai
import openai_params as oai
#import request text
import prompt_txt.unittest_rq as u_test

#request add unit test to code
class Feature_Request_Utest():

	def __init__(self, common_instance):
		self.common_instance = common_instance

	def prerequest_args_process(self):
		# send additional requests, not back to menu
		return True, False

	def prepare_request_args(self):
		#get cached response as starting point for unit test
		self.common_instance.gpt_response_utest = self.common_instance.gpt_response
		#build args
		summary_new_request = "Add Unit tests to the code."
		sys_mssg = u_test.sys_mssg
		self.common_instance.request_to_gpt = f'''You will make specific changes to this JSON object: {self.common_instance.gpt_response_utest}.
		\nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object':
		\n{self.common_instance.program_description}. {ut.concat_dict_to_string(u_test.unittest_instructions_dict)}'''
		#call base
		return self.common_instance.build_request_args(summary_new_request, sys_mssg, self.common_instance.request_to_gpt)

	#send request to model
	def request_code(self, *request_args):
		#override base instance vars
		self.common_instance.u_test_bool = True
		self.common_instance.model = oai.codex_engine_deployment_name
		self.common_instance.model_temp = 0.2
		#run base request implementation
		return self.common_instance.request_code_enhancement(*request_args)

	def process_successful_response(self):
		#check unittest commands are valid
		if not self.common_instance.validate_unittest_commands():
			print("Unit test functions not created. Re-create unit test code and cli commands.")
			fm.version_file(self.common_instance.full_project_dirname, self.common_instance.module_utest_name, self.common_instance.full_project_dirname)
			return False
		#unittest commands valid
		mssg = "Unit test functions CLI commands successfully created."
		#call base
		self.common_instance.valid_response_file_management(self.common_instance.module_utest_name, self.common_instance.full_project_dirname, self.common_instance.gpt_response_utest, success_mssg=mssg)
		return True

	def validate_unittest_commands(self):
		print(); print("-"*40)
		print("Validating Unittest Function CLI commands were created.")
		num_unittests = 0
		num_unittests = ut.count_values_for_keycontain(self.common_instance.gpt_response_utest, u_test.unittest_cli_command_key)
		if num_unittests > 0: return True
		else:
			print("Unit test functions not created. Re-create unit test code and cli commands.")
			fm.version_file(self.common_instance.full_project_dirname, self.common_instance.module_utest_name, self.common_instance.full_project_dirname)
			return False
