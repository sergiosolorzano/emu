#!/usr/bin/env python3
import os
#import base
import feature_base as base
#import utils
import tools.file_management as fm
import tools.request_utils as ut

#user upload code from file
class Feature_Request_Loadcode(base.Feature_Base):

    def __init__(self):
        super().__init__()  # Call parent class's __init__ method

    def prerequest_args_process(self):
        mssg = f"Enter Path to {self.program_language} Script: "
        # call base
        full_path_to_script = self.get_file_path_from_user(mssg)

        print()
        mssg = f"Program Description: Enter Short Program Description (used in requests): "
        self.program_description = self.user_interaction_instance.request_input_from_user(mssg)

        # call base
        user_script = self.read_code_from_file(full_path_to_script)
        # hack to step script as a gpt code response for continued conversation with gpt
        self.gpt_response = fm.insert_script_in_json(user_script)
        # print loaded code
        #code = ut.get_response_value_for_key(self.gpt_response, self.module_script_fname.split(".")[0])
        # print(code);print()
        print(f"\033[43mScript loaded.\033[0m")

        return False

    def prepare_request_args(self):
        #no args to build because there is no request
        return None

    # def upload_code_from_file(self):
    #     while True:
    #         mssg = f"Enter Path to {self.program_language} Script: "
    #         full_path_to_script = self.user_interaction_instance.request_input_from_user(mssg)
    #         if not os.path.isfile(full_path_to_script):
    #             print(f"\033[1;31m[ERROR]\033[0m Cannot Find Script File {full_path_to_script}\033[0m")
    #             continue
    #         else:
    #             print("Script Found.")
    #             print()
    #             mssg = f"Program Description: Enter Short Program Description (used in requests): "
    #             self.program_description = user_interaction_instance.request_input_from_user(mssg)
    #
    #     return full_path_to_script

    def process_successful_response(self):
        #call base: process successful code upload
        self.valid_response_file_management(self.module_script_fname, self.full_project_dirname, self.gpt_response)
        return True
