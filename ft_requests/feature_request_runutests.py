#!/usr/bin/env python3

#import libraries
import sys
import os
import subprocess
import shlex
#import config
import config as config
#import utils
import tools.file_management as fm
import tools.request_utils as ut
#import request text
import unittest_cli_comm_rq as unittest_cli_comm
#openai
import openai_params as oai

#run unit tests
class Feature_Request_Run_Unit_Test_Cases:

    def __init__(self, common_instance):
        self.common_instance = common_instance
        self.test_counter = 0
        self.restart_all_unittests = False
        self.comm = None

    def prerequest_args_process(self):
        #run unit tests
        while True:
            self.test_counter = 0
            self.restart_all_unittests = False

            #Create unittesting cli command list from gpt response
            unittest_cli_c_list = []
            print(); print("-"*40)
            unittest_cli_c_list = ut.create_unittest_cli_list(unittest_cli_c_list, self.common_instance.gpt_response_utest, config.unittest_cli_command_key)
            for unitt in unittest_cli_c_list:
                print("Unittest command:", unitt)

            #run unittests
            print(f"Running Unittests: {len(unittest_cli_c_list)} tests."); print()
            os.chdir(config.full_project_dirname)
            for bt in unittest_cli_c_list:
                try:
                    self.run_utest_command(bt)
                except subprocess.CalledProcessError as e:
                    user_choice_at_exception = self.handle_unittest_exception(e)
                    if user_choice_at_exception == "m":
                        #skip all tests - back to menu
                        return False, True
                    elif user_choice_at_exception == "s":
                        #skip this test
                        continue
            break

        print(); print(f"\033[43mUnit Testing Complete.\033[0m")
        os.chdir(config.initial_dir)
        return False, True

    def prepare_request_args(self):
        #request args upon exception when running utest
        summary_new_request = "Request re-generation of cli commands for existing unittest functions in the code."
        sys_mssg = self.common_instance.unittest_cli_comm.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.common_instance.gpt_response_utest}.\n
        {ut.concat_dict_to_string(unittest_cli_comm.unittest_regen_cli_comm_instructions_dict)}'''
        return self.common_instance.build_request_args(summary_new_request,sys_mssg,request_to_gpt)

    def run_utest_command(self, test_comm):
        bt_c = test_comm.replace("python ","")
        bt_c = bt_c.replace("python3","")
        comm_list = shlex.split(bt_c)
        self.comm = ['python'] + comm_list
        print(f"Running command: {self.comm}")
        subprocess.run(self.comm, check=True)
        self.test_counter += 1
        print(); print("-" * 40)
        print(); print("Test:",bt_c)

    def handle_unittest_exception(self, e):
        print(f"\n\033[31mError or Exception Thrown running a unit test cli command.:{self.comm}: {e}\n\033[0m")
        #TODO: if "No such file or directory" in str(e) or "returned non-zero exit status" in str(e):
        print(); print("="*40)
        print(); print("Please review the code. Attempt to correct or skip:")
        print(f"\n\033[1;31m[INFO]\033[0m If you skip all unit tests, you can send a Custom Request of the error or auto-debug the logs, both available from the main Menu.", end ="")
        print()

        #interact with user:
        #choice skip current test, skip all, or request model re-generate unittest commands
        mssg = "=>Press \033[1m(m)\033[0m to go back to (M)enu.\n=>Press \033[1m(s)\033[0m to (S)kip the current unit test and continue to the next one.\n\nChoice: "
        mssg_option1 = "\033[41mBack to menu and cancel all unit tests.\033[0m"
        mssg_option3 = "\033[41mContinue testing and skip this unit test.\033[0m"
        choice = self.common_instance.user_interaction_instance.user_choice_two_options(mssg, option1="m", option2="s", mssg_option1=mssg_option1, mssg_option2=None, mssg_option3=mssg_option3)
        print(); print("="*40)

        #take action according to user choice to handle exception
        return choice

    #send request to model
    def request_code(self, *request_args):
        #validate unit test functions
        if self.process_utest_response():
            #override base instance vars
            self.common_instance.u_test_bool = True
            self.common_instance.model = oai.codex_engine_deployment_name
            self.common_instance.model_temp = 0.2
            #run base request implementation
            return self.common_instance.request_code_enhancement(*request_args)
        else:
            return False

    #process new response with unit tests
    def process_utest_response(self):
        #check unittest commands are valid
        if not self.validate_unittest_commands():
            print("Unit test functions not created. Re-create unit test code and cli commands.")
            fm.version_file(config.full_project_dirname, config.module_utest_name, config.full_project_dirname)
            return False
        #unittest commands valid
        mssg = "Unit test functions CLI commands succesfully created."
        return True

    def validate_unittest_commands(self):
        print(); print("-"*40)
        print("Validating Unittest Function CLI commands were created.")
        num_unittests = 0
        num_unittests = ut.count_values_for_keycontain(self.common_instance.gpt_response_utest, config.unittest_cli_command_key)
        if num_unittests > 0:
            return True
        else:
            print("Unit test functions not created. Re-create unit test code and cli commands.")
            return False

    def process_successful_response(self):
        #not a request option
        return True
