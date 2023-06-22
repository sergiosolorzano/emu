#!/usr/bin/env python3
#import utils
import tools.request_utils as ut
#import request text
import debug_rq as dg_r
#openai
import openai_params as oai
#import config_dir
from config_dir import config as config


#Request model to debug program with logs
class Feature_Request_DebugLogs:

    def __init__(self, common_instance):
        self.common_instance = common_instance
        # error when running the program
        self.error_mssg = None
        # command when error occurred
        self.command = None

    def request_manager(self):
        if self.user_action_debug_or_not():
            args = self.prepare_request_args()
            request_success = self.request_code(args)
            if request_success:
                self.process_successful_response()
                return True
            else:
                return False
        return True

    def prepare_request_args(self):
        #request args
        summary_new_request = "Change the code to correct errors shown in the log file."
        sys_mssg = dg_r.sys_mssg
        request_to_gpt = f'''You will make specific changes to the value of this JSON object which is the code: {self.common_instance.gpt_response}.
                \nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object:\n{self.common_instance.program_description}.
                \n{ut.concat_dict_to_string(dg_r.debug_instructions_dict)}\n\n{dg_r.command}{self.command}\n\n{dg_r.error}{self.error_mssg}'''

        args_tpl = (summary_new_request, sys_mssg, request_to_gpt)
        return args_tpl
            
    def user_action_debug_or_not(self):
        while True:
            print(); choice = input("Request debug with log? y/n: ")
            match choice.lower():
                case 'y':
                    #set engine defaults
                    self.common_instance.model_temp = 0.2
                    self.common_instance.model = oai.secondary_engine_deployment_name
                    #user set engine/temperature
                    self.get_user_model_and_temp()
                    return True
                case 'n':
                    return False
                case _:
                    print("Invalid selection.")
                    continue

    def get_user_model_and_temp(self):
        while True:
            print(); print(f"Default Model: {self.common_instance.model[1]} Temperature: {self.common_instance.model_temp}")
            cont = self.common_instance.user_interaction_instance.request_input_from_user("(A)accept defaults or (C)hange? a/c: ")
            if cont.lower() == "a":
                print(f"Engine selected: {self.common_instance.model[1]} Temperature {self.common_instance.model_temp}")
                return
            elif cont.lower() == "c":
                while True:
                    print(); choice = input(f"1. Gpt-3.5 Turbo\n2. code-davinci-002\n3. text-davinci-003\nChoose model? ")
                    match choice:
                        case '1':
                            self.common_instance.model = oai.primary_engine_deployment_name
                            break
                        case '2':
                            self.common_instance.model = oai.secondary_engine_deployment_name
                            break
                        case '3':
                            self.common_instance.model = oai.tertiary_engine_deployment_name
                            break
                        case _:
                            print("Invalid model selection.")
                            continue
            else:
                print("Invalid selection.")
                continue

            while True:
                print(); u_temp = self.common_instance.user_interaction_instance.request_input_from_user("Enter model temperature (float 0-1): ")
                try:
                    u_temp = float(u_temp)
                except Exception as e:
                    print(f"Invalid temperature {u_temp}. Value must be float or int value 0-1.")
                    continue
                if isinstance(u_temp,float) or isinstance(u_temp, int):
                    if 0 <= u_temp <= 1.0:
                        self.common_instance.model_temp = u_temp
                        print(f"Model selected: {self.common_instance.model[1]} Temperature {self.common_instance.model_temp}")
                        return
                    else:
                        print(f"Invalid temperature {u_temp}. Value must be float or int value 0-1.")
                else:
                    print(f"Invalid temperature {u_temp}. Value must be float or int value 0-1.")

    #send request to model
    def request_code(self, *request_args):
        #run base request implementation
        # override base instance vars
        self.common_instance.model = oai.secondary_engine_deployment_name
        self.common_instance.model_temp = 0.7
        return self.common_instance.request_code_enhancement(*request_args)

    def process_successful_response(self):
        self.common_instance.valid_response_file_management(config.module_script_fname, config.full_project_dirname, self.common_instance.gpt_response)
        return True