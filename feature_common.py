#!/usr/bin/env python3

# import libraries
import os
import threading
import json
import textwrap
import dataclasses
import user_interaction as uinteraction
import log_list_handler
#import tools
import tools.file_management as fm
import tools.request_utils as ut
# import openai libs/modules
import openai_params as oai
#import config
import config as config

class Feature_Common:
    # show request text on screen
    show_request = True

    # set model and temp
    model = oai.gpt_engine_deployment_name
    model_temp = 0.7

    # program description
    program_description = None

    def __init__(self, program_description=None):
        self.cum_tokens = 0
        # set common instances
        self.user_interaction_instance = None
        self.set_user_interaction_instance(uinteraction.User_Interaction())
        #self.log_list_handler_instance = None
        self.logger_instance = None
        self.log_list_handler_instance = None
        self.set_log_list_handler_instance(log_list_handler.config_custom_logger())
        #set prog desc
        if program_description is not None:
            self.program_description = program_description
        #init responses
        self.gpt_response = None
        self.gpt_response_utest = None

    def set_user_interaction_instance(self, user_interaction_instance):
        self.user_interaction_instance = user_interaction_instance

    def set_log_list_handler_instance(self, log_list_handler_instance):
        self.logger_instance, self.log_list_handler_instance = log_list_handler_instance

    #request module code
    def send_request(self, sys_mssg, request_to_gpt, summary_new_request):
        this_conversation = []

        system_message = {"role": "system", "content": sys_mssg}

        this_conversation.append(system_message)

        # request requirements
        this_conversation.append({"role": "user", "content": request_to_gpt})

        request_tokens = this_conversation_tokens = ut.num_tokens_from_messages(this_conversation)

        ut.token_limit(request_tokens)

        self.cum_tokens += this_conversation_tokens

        print(); print("-" * 40); print()
        print(f"\033[44;97mJob Request: {summary_new_request}\033[0m")
        if self.show_request:
            print(
                f"\n\033[1;97mRequest: CumTokens:{self.cum_tokens} Req_Tokens:{request_tokens}\033[0m: System Message:{sys_mssg}\nPrompt:{request_to_gpt}")
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
            max_tokens=config.max_response_tokens,
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
                                              separators=(',', ':'))
            print(f"\n\033[1;92mResponse: CumTokens:{self.cum_tokens} RespTokens:{this_conversation_tokens}\n\033[0m\033[92m{pretty_json_response}\n\033[0m")
        except Exception as e:
            print(f"Exception on JSON Received: {e}: {clean_response:<10} \n")
            #print("RAW response:", clean_response)
            print("-" * 40)
            # JSON response invalid re-request or quit
            return False

        self.gpt_response = json.loads(clean_response)  # .strip("\n")  #.replace('```', '')

        return True

    def build_request_args(self, summary_new_request, sys_mssg, request_to_gpt):
        args_tpl = (summary_new_request, sys_mssg, request_to_gpt)
        return args_tpl

    # manage request
    def request_code_enhancement(self, request_args):
        # unpack request args for clarity. pass request_to_gpt to change value for utests and standard
        summary_new_request, sys_mssg, request_to_gpt = request_args
        # send request to model
        return self.send_request(sys_mssg, request_to_gpt, summary_new_request)

    @staticmethod
    def valid_response_file_management(filename, full_path_dir, gpt_response, success_mssg=None):
        if success_mssg is not None:
            print(f"\033[43m{success_mssg}\033[0m")
        # version and save
        fm.version_file(full_path_dir, filename, full_path_dir)
        fm.get_dict_value_save_to_file(gpt_response, config.initial_dir, filename, "#!/usr/bin/env python3\n\n")
        print(f"Code:\n", fm.get_code_from_dict(gpt_response, config.code_key_in_json))

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
