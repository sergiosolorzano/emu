#!/usr/bin/env python3
#import utils
import tools.request_utils as ut
#import request text
import debug_rq as dg_r
#openai
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
        # # override base instance vars
        # config.used_api = config.request_debuglogs_api
        # self.common_instance.model = config.model_request_debuglogs
        # self.common_instance.model_temp = config.model_request_debuglogs_temperature

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
                    config.used_api = config.request_debuglogs_api
                    self.common_instance.model = config.model_request_debuglogs
                    self.common_instance.model_temp = config.model_request_debuglogs_temperature
                    #user set engine/temperature
                    self.get_user_model_and_temp()
                    return True
                case 'n':
                    return False
                case _:
                    print("Invalid selection.")
                    continue

    def get_user_model_and_temp(self):
        attribute_name = [attr_name for attr_name, attr_value in vars(config.Model_API).items() if attr_value == config.used_api][0]
        while True:
            print(); print(f"Default Model: {attribute_name} {self.common_instance.model[1]} Temperature: {self.common_instance.model_temp}")
            cont = self.common_instance.user_interaction_instance.request_input_from_user("(A)accept defaults or (C)hange? a/c: ")
            if cont.lower() == "a":
                print(f"Engine selected: {self.common_instance.model[1]} Temperature {self.common_instance.model_temp}")
                return
            elif cont.lower() == "c":
                print();print(f"NOTE: Code-davinci-002 and text-davinci-003 models do not evaluate the logs but only debug the code.\nGpt-3.5 Turbo evaluates the error logs.")
                while True:
                    print();
                    choice = input(f"1. {attribute_name} Gpt-3.5 Turbo\n2. {attribute_name} code-davinci-002\n3. {attribute_name} text-davinci-003\nChoose model? ")
                    match choice:
                        case '1':
                            if config.used_api == config.Model_API.AZURE_OPENAI_API:
                                self.common_instance.model = (config.Azure_OpenAI_Model.gpt35_deployment_name, config.Azure_OpenAI_Model.gpt35_model_name)
                            elif config.used_api == config.Model_API.OPENAI_API:
                                self.common_instance.model = (config.OpenAI_Model.gpt35_deployment_name, config.OpenAI_Model.gpt35_model_name)
                            break
                        case '2':
                            if config.used_api == config.Model_API.AZURE_OPENAI_API:
                                self.common_instance.model = (config.Azure_OpenAI_Model.codex_deployment_name,config.Azure_OpenAI_Model.codex_model_name)
                            elif config.used_api == config.Model_API.OPENAI_API:
                                self.common_instance.model = (config.OpenAI_Model.codex_deployment_name,config.OpenAI_Model.codex_model_name)
                            break
                        case '3':
                            if config.used_api == config.Model_API.AZURE_OPENAI_API:
                                self.common_instance.model = (config.Azure_OpenAI_Model.davincitext_deployment_name, config.Azure_OpenAI_Model.davincitext_model_name)
                            elif config.used_api == config.Model_API.OPENAI_API:
                                self.common_instance.model = (config.OpenAI_Model.davincitext_deployment_name, config.OpenAI_Model.davincitext_model_name)
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
        return self.common_instance.request_code_enhancement(*request_args, debug_mode=True)

    def process_successful_response(self):
        self.common_instance.valid_response_file_management(config.module_script_fname, config.full_project_dirname, self.common_instance.gpt_response)
        return True