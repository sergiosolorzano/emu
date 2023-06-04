#!/usr/bin/env python3

#import base
import feature_base as base
#import utils
import file_management as fm
import request_utils as ut
#import classes
import user_interaction as uinteraction

#user upload code from file
class Feature_Request_Loadcode(Feature_Base):
	
	def prepare_request_args():
        #no args to build because there is no request
        return None
        
    #choice is read code from file
    def choice_not_a_request():
        mssg = f"Enter Path to {self.program_language} Script: "
        #call base
        full_path_to_script = self.get_file_path_from_user(mssg)
        
        print()
        mssg = f"Program Description: Enter Short Program Description (used in requests): "
        self.program_description = uinteraction.request_input_from_user(mssg)
        
        #call base
        user_script = self.read_code_from_file(full_path_to_script)
        #store code
        self.gpt_response = fm.insert_script_in_json(user_script)
        #print loaded code
        #code = ut.get_response_value_for_key(oai_req_instance.gpt_response,raw_code.module_name.split(".")[0])
        #print(code);print()
        print(f"\033[43mScript loaded.\033[0m")

        return True

    def upload_code_from_file(self):
        while True:
            mssg = f"Enter Path to {self.program_language} Script: "
            full_path_to_script = uinteraction.request_input_from_user(mssg)
            if not os.path.isfile(full_path_to_script):
                print(f"\033[1;31m[ERROR]\033[0m Cannot Find Script File {full_path_to_script}\033[0m")
                continue
            else: 
                print("Script Found.")
                print()
                mssg = f"Program Description: Enter Short Program Description (used in requests): "
                self.program_description = uinteraction.request_input_from_user(mssg)

        return full_path_to_script
        
    def read_code_from_file(self, full_path_to_script):
        #read script
        user_script = fm.read_file_stored_to_buffer(os.path.basename(full_path_to_script), os.path.dirname(full_path_to_script))
        #hack to step script as a gpt code response for continued conversation with gpt
        self.gpt_response =  fm.insert_script_in_json(user_script)
        #print loaded code
        code = ut.get_response_value_for_key(self.gpt_response,self.module_script_fname.split(".")[0])
        #print(code);print()
        print(f"\033[43mScript loaded.\033[0m")

    #send request to model
    def request_code(*request_args):
        #override base instance vars
        self.u_test= False
        self.model = oai.gpt_engine_deployment_name
        self.model_temp = 0.7
        #run base request implementation
        return self.request_code_enhancement(*request_args, self.u_test)

    def process_successful_response():
        #call base: process successful code upload
        self.valid_response_file_management(self.module_script_fname, self.full_project_dirname, self.gpt_response)
        return True