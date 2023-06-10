#!/usr/bin/env python3

# import libraries
import sys
import os
import threading

# from pathlib import Path
import json

import dataclasses
import user_interaction as uinteraction
import log_list_handler

#import tools
import tools.file_management as fm
import tools.request_utils as ut

# import openai libs/modules
import openai_params as oai
#import ft_requests
import prompt_txt.raw_code_rq as raw_code

class Feature_Common:
    #region Class Variables Region
    # show request text on screen
    show_request = True

    # set model and temp
    model = oai.gpt_engine_deployment_name
    model_temp = 0.7

    # model token settings
    cum_tokens = 0
    token_limit = 4096
    max_response_tokens = 3000

    # paths
    initial_dir = os.getcwd()
    root = os.getenv("HOME")
    prompt_dirname = "prompt_txt"
    project_dirname = "project"
    json_dirname = "response_json"
    custom_json_format_dirname = "custom_json_format"
    # full dir paths
    full_prompt_dirname = f"{initial_dir}/{prompt_dirname}"
    full_project_dirname = f"{initial_dir}/{project_dirname}"
    full_json_dir = f"{initial_dir}/{json_dirname}"
    full_custom_json_format_dirname = f"{initial_dir}/{custom_json_format_dirname}"

    # filenames
    module_script_fname = "module.py"
    log_fname = "module.log"
    module_utest_name = "module_utest.py"
    json_fname = "response.json"
    custom_json_format_fname = "custom_json_format.json"

    # program language
    program_language = "Python"

    # program description
    program_description = "No description provided"

    # unittest json command key
    unittest_cli_command_key = "unittest_cli_"
    #endregion

    def get_gpt_response(self):
        return self.gpt_response

    def __init__(self, program_description=None):
        # set base common instances
        self.user_interaction_instance = None
        self.log_list_handler_instance = None
        self.set_user_interaction_instance(uinteraction.User_Interaction())
        self.set_log_list_handler_instance(log_list_handler.LogListHandler())
        #utest flag
        self.u_test_bool = False
        #set prog desc
        if program_description is not None:
            self.program_description = program_description
        #init responses
        self.gpt_response = None
        self.gpt_response_utest = None

    def set_user_interaction_instance(self, user_interaction_instance):
        self.user_interaction_instance = user_interaction_instance
        #print("******base holds ",self.user_interaction_instance)

    def set_log_list_handler_instance(self, log_list_handler_instance):
        self.log_list_handler_instance = log_list_handler_instance

    # request module code
    def send_request(self, sys_mssg, request_to_gpt, summary_new_request):
        this_conversation = []

        system_message = {"role": "system", "content": sys_mssg}

        this_conversation.append(system_message)

        # request requirements
        this_conversation.append({"role": "user", "content": request_to_gpt})

        request_tokens = this_conversation_tokens = ut.num_tokens_from_messages(this_conversation)

        ut.token_limit(request_tokens)

        self.cum_tokens += this_conversation_tokens

        # if show_request: #TODO: show on screen the request or not
        print(); print("-" * 40); print()
        print(f"\033[44;97mJob Request: {summary_new_request}\033[0m")
        if self.show_request:
            print(
                f"\n\033[1;97mRequest: CumTokens:{self.cum_tokens} Req_Tokens:{request_tokens}\033[0m: {request_to_gpt}")
        else:
            print(f"\n\033[1;97mRequest Sent: CumTokens:{self.cum_tokens} Req_Tokens:{request_tokens}\033[0m")

        print()
        print(f"\033[1;97mModel Settings:\033[0m Engine: {self.model[1]}, Temperature: {self.model_temp}")

        # start timer
        stop_event = threading.Event()
        thread = threading.Thread(target=ut.spinning_timer, args=("Awaiting Response...", stop_event))
        thread.start()
        response = oai.openai.ChatCompletion.create(
            engine=self.model[0],
            messages=this_conversation,
            temperature=self.model_temp,
            max_tokens=self.max_response_tokens,
        )

        clean_response = response['choices'][0]['message']['content'].replace("'''", "'").replace('"""', '"').replace(
            '```', '`')

        # stop timer
        stop_event.set()
        thread.join()
        print('\r\033[K', end='')  # Clear the line

        this_conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        this_conversation_tokens = ut.num_tokens_from_messages(this_conversation)
        self.cum_tokens += this_conversation_tokens

        ut.token_limit(this_conversation_tokens)

        print("-" * 40)
        try:
            pretty_json_response = json.dumps(json.loads(clean_response), indent=2,
                                              separators=(',', ':'))  # .replace('```', '')
            print(f"\n\033[1;92mResponse: CumTokens:{self.cum_tokens} RespTokens:{this_conversation_tokens}\n\033[0m\033[92m{pretty_json_response}\n\033[0m")
        except Exception as e:
            print(f"Exception on JSON Received: {e}: {clean_response:<10} \n"); print()
            print("RAW response:", clean_response)
            print("-" * 40)
            # JSON response invalid, re-request or quit
            return False

        if self.u_test_bool:
            print(f"*****u_test_bool {self.u_test_bool}")
            self.gpt_response_utest = json.loads(clean_response)  # .strip("\n") #.replace('```', '')
        else:
            print(f"*****u_test_bool {self.u_test_bool}")
            self.gpt_response = json.loads(clean_response)  # .strip("\n")  #.replace('```', '')

        # JSON response valid
        self.u_test_bool = False
        return True

    @staticmethod
    def build_request_args(summary_new_request, sys_mssg, request_to_gpt):
        args_tpl = (summary_new_request, sys_mssg, request_to_gpt)
        return args_tpl

    # manage request
    def request_code_enhancement(self, *request_args):
        # unpack request args for clarity
        summary_new_request, sys_mssg, request_to_gpt = request_args
        # send request to model
        return self.send_request(sys_mssg, request_to_gpt, summary_new_request)

    def valid_response_file_management(self, filename, full_path_dir, gpt_response, success_mssg=None):
        if success_mssg is not None:
            print(f"\033[43m{success_mssg}\033[0m")
        # version and save
        fm.version_file(full_path_dir, filename, full_path_dir)
        fm.get_dict_value_save_to_file(gpt_response, self.initial_dir, filename, "#!/usr/bin/env python3\n\n")

    # TODO: remove for debugging
    # fm.write_to_file(self.json_fname, self.json_dirname, gpt_response, "w")
    # end remove for debugging

    def get_file_path_from_user(self, mssg):
        while True:
            full_path_to_file = self.user_interaction_instance.request_input_from_user(mssg)
            if not fm.validate_filepath(full_path_to_file):
                continue
            else:
                return full_path_to_file

    @staticmethod
    def read_code_from_file(full_path_to_script):
        # read script
        code = fm.read_file_stored_to_buffer(os.path.basename(full_path_to_script),
                                             os.path.dirname(full_path_to_script))
        return code
