#!/usr/bin/env python3
#import utils
import tools.file_management as fm
import tools.request_utils as ut
#import config
import config as config

#user upload code from file
class Op_Loadcode:

    def __init__(self, common_instance):
        self.common_instance = common_instance
        self.full_path_to_script = None

    def run_operation(self):
        mssg = f"Enter Path to {config.program_language} Script: "
        # call base
        full_path_to_script = self.common_instance.get_file_path_from_user(mssg)

        print()
        mssg = f"Enter Short Program Description (used for requests): "
        self.common_instance.program_description = self.common_instance.user_interaction_instance.request_input_from_user(mssg)

        # call common
        user_script = self.common_instance.read_code_from_file(full_path_to_script)
        # hack to step script as a gpt code response for continued conversation with gpt
        self.common_instance.gpt_response = fm.insert_script_in_json(user_script)
        # print loaded code
        #code = ut.get_response_value_for_key(self.common_instance.gpt_response, self.common_instance.module_script_fname.split(".")[0])
        #print(code); print()
        print(f"\033[43mScript loaded.\033[0m")

        return True


    def process_successful_response(self):
        #call base: process successful code upload
        self.common_instance.valid_response_file_management(config.module_script_fname, config.full_project_dirname, self.common_instance.gpt_response)
        return True
