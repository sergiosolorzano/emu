#!/usr/bin/env python3

#import libraries
import sys
import os
import subprocess
import shlex
import time
import threading
from pathlib import Path
import json

#import self module
import file_management as fm

#TODO: create dirs module
sys.path.append(fm.m_root)
sys.path.append(f'{fm.initial_dir}/{fm.m_prompt_dirname}')

#import openai libs/modules
import tiktoken
import openai
import openai_params as oai

#import data to request module code
#import request requirements
import raw_code_rq as raw_code
import clean_json_rq as clean_json
import input_and_argparse_rq as input_and_argparse
import error_hndl__logging_rq as error_log_hndl
import unittest_rq as u_test
import unittest_cli_comm_rq as unittest_cli_comm
import custom_req as c_r
import docstrings_rq as docs_r
import debug_rq as dg_r
#import my utils
import request_utils as ut

class Openai_Requests:
    show_request = True

    def __init__(self,program_description="No description provided.", gpt_response="No response provided."):
        self.program_description = program_description
        self.gpt_response = gpt_response
        self.gpt_response_utest = gpt_response
        #TODO: set engine and engine as instance objs
        #self.deployment_name
        #self.temperature

    #getter instance method get gpt_resp
    def get_gpt_response(self):
        return self.gpt_response

    #setter instance method set gpt_resp
    def set_gpt_response(self, gpt_response):
        self.gpt_response = gpt_response

    #getter instance method get gpt u_test resp
    def get_gpt_response_utest(self):
        return self.gpt_response_utest

    @classmethod
    def get_show_request(cls):
        return cls.show_request

    #request module code
    def send_request(self, sys_mssg, request_to_gpt, summary_new_request, u_test = False, new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name):
        #set engine
        tmp_deployment_name = oai.deployment_name
        oai.deployment_name = new_engine
        #set engine temp
        temp_oai_temp =  oai.temperature
        oai.temperature = new_temp

        this_conversation =[]

        system_message = {"role": "system", "content": sys_mssg}

        this_conversation.append(system_message)

        #request requirements
        this_conversation.append({"role": "user", "content": request_to_gpt})
        
        request_tokens = this_conversation_tokens = ut.num_tokens_from_messages(this_conversation)

        ut.token_limit(request_tokens)

        oai.cum_tokens += this_conversation_tokens
        
        #if show_request: #TODO: show on screen the request or not
        print(); print("-"*40)
        print();print(f"\033[44;97mJob Request: {summary_new_request}\033[0m")
        if self.get_show_request():
            print(f"\n\033[1;97mRequest: CumTokens:{oai.cum_tokens} Req_Tokens:{request_tokens}\033[0m: {request_to_gpt}")
        else:
            print(f"\n\033[1;97mRequest Sent: CumTokens:{oai.cum_tokens} Req_Tokens:{request_tokens}\033[0m")
        
        print(); print(f"\033[1;97mModel Settings:\033[0m Engine: {oai.deployment_name[1]}, Temperature: {oai.temperature}")

        #start timer
        stop_event = threading.Event()
        thread = threading.Thread(target=ut.spinning_timer, args=("Awaiting Response...",stop_event))
        thread.start()

        response = oai.openai.ChatCompletion.create(
            engine=oai.deployment_name[0], # The deployment name you chose when you deployed the model.
            messages = this_conversation,
            temperature=oai.temperature,
            max_tokens=oai.max_response_tokens,
        )

        clean_response = response['choices'][0]['message']['content'].replace("'''","'").replace('"""','"').replace('```', '`')

        #stop timer
        stop_event.set()
        thread.join()
        print('\r\033[K', end='')  # Clear the line

        this_conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        this_conversation_tokens = ut.num_tokens_from_messages(this_conversation)
        oai.cum_tokens += this_conversation_tokens

        ut.token_limit(this_conversation_tokens)

        #re-set engine
        oai.deployment_name = tmp_deployment_name
        #re-set temp
        oai.temperature = temp_oai_temp

        print("-"*40);
        try:
            pretty_json_response = json.dumps(json.loads(clean_response), indent=2, separators=(',', ':')) #.replace('```', '')
            print(f"\n\033[1;92mResponse: CumTokens:{oai.cum_tokens} RespTokens:{this_conversation_tokens}\n\033[0m\033[92m{pretty_json_response}\n\033[0m")
        except Exception as e:
            print(f"Exception on JSON Received: {e}: {clean_response:<10} \n")
            print(); print("RAW print:",clean_response)
            print("-"*40);
            #JSON invalid, re-request or quit
            return False

        if u_test:
            self.gpt_response_utest = json.loads(clean_response) #.strip("\n") #.replace('```', '')
        else:
            self.gpt_response = json.loads(clean_response) #.strip("\n")  #.replace('```', '')

        return True

    #build args for exception handling request request
    def build_request_exception_handl_req_args(self):
        #request args
        summary_new_request = "Add Error and Exception Handling to the code."
        sys_mssg = error_log_hndl.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.gpt_response}.
        \nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object:\n
        {self.program_description}\n\n{ut.concat_dict_to_string(error_log_hndl.err_hndl_instructions_dict)}'''

        args_tpl = (summary_new_request,sys_mssg,request_to_gpt)
        return args_tpl

    #build args to debug log
    def build_request_debug_log_req_args(self,error, command):
        #request args
        summary_new_request = "Change the code to correct errors shown in the log file."
        sys_mssg = dg_r.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.gpt_response}.
        \nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object:\n{self.program_description}.
        \n{ut.concat_dict_to_string(dg_r.debug_instructions_dict)}\n\n{dg_r.command}{command}\n\n{dg_r.error}{error}'''

        args_tpl = (summary_new_request,sys_mssg,request_to_gpt)
        return args_tpl

    #build args for input and argpase request
    def build_request_input_and_argparse_args(self):
        #request args
        summary_new_request = "Add User Input and Argparse functionality to the code."
        sys_mssg = input_and_argparse.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.gpt_response}.
        This is the description of what the program does in the the code found in the value for key 'module' of the JSON object':
        {self.program_description} \n\n{ut.concat_dict_to_string(input_and_argparse.input_and_argparse_instructions_dict)}
        '''

        args_tpl = (summary_new_request,sys_mssg,request_to_gpt)
        return args_tpl

    #build args for unit testing request
    def build_request_unittest_args(self):
        #request args
        summary_new_request = "Add Unit tests to the code."
        sys_mssg = u_test.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.gpt_response_utest}.
        \nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object':
        \n{self.program_description}. {ut.concat_dict_to_string(u_test.unittest_instructions_dict)}
        '''

        args_tpl = (summary_new_request,sys_mssg,request_to_gpt)
        return args_tpl

    def build_request_custom_user_args(self, custom_sys_req_input, custom_conv_req_input, custom_json):
        json_required_format ='''JSON Object Template:'''
        custom_sys_req_input = c_r.sys_mssg + ". " + custom_sys_req_input
        custom_json_str = json.dumps(custom_json).replace("\n","")
        custom_conv_req_input = str("Your job for this request: " + custom_conv_req_input.replace("\n","") + ". " 
        + f"This is the description of what the program does in the the code found in the value for key 'module' of the JSON object':{self.program_description}."
        + f"You will make specific changes to this JSON object: {self.gpt_response}."
        + c_r.json_object_requirements + ". " + custom_json_str + "\n"
        + c_r.comments)

        #build request and send
        request_args = ("Your Custom Request",custom_sys_req_input,custom_conv_req_input)

        return request_args

        summary_new_request = "Add Unit tests to the code."
        sys_mssg = u_test.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.gpt_response}.
        \nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object':
        \n{self.program_description}. {ut.concat_dict_to_string(u_test.unittest_instructions_dict)}
        '''

    #build args for request to re-generate unit test cli commands
    def build_request_regenerate_unittest_cli_comm_args(self):
        #request args
        summary_new_request = "Request re-generation of cli commands for existing unittest functions in the code."
        sys_mssg = unittest_cli_comm.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.gpt_response_utest}.\n
        {ut.concat_dict_to_string(unittest_cli_comm.unittest_regen_cli_comm_instructions_dict)}
        '''

        args_tpl = (summary_new_request,sys_mssg,request_to_gpt)
        return args_tpl

    #build args for request to add docstrings
    def build_request_docstrings_args(self):
        #request args
        summary_new_request = "Add docstrings to the script."
        sys_mssg = docs_r.sys_mssg
        request_to_gpt = f'''You will make specific changes to the module key of this JSON object: {self.gpt_response}.\n
        {ut.concat_dict_to_string(docs_r.docstrings_instructions_dict)}'''

        args_tpl = (summary_new_request,sys_mssg,request_to_gpt)
        return args_tpl

    #build args to request raw code
    def build_request_raw_code_req_args(self):
        #request args
        summary_new_request = "Request raw program code."
        sys_mssg = raw_code.sys_mssg
        request_to_gpt = ut.concat_dict_to_string(raw_code.raw_instructions_dict) + "\n\n" + self.program_description

        args_tpl = (summary_new_request,sys_mssg,request_to_gpt)
        return args_tpl

    #build args for miscellaneous code enhancements
    def request_code_enhancement(self, *request_args, u_test, new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name):
        #unpack request args for clarity
        summary_new_request,sys_mssg,request_to_gpt = request_args
        while True:
            #send request, response JSON may be broken in which case possible re-request
            resp = self.send_request(sys_mssg, request_to_gpt, summary_new_request, u_test, new_temp = new_temp, new_engine = new_engine)
            if resp == False: 
                #broken JSON
                if self.broken_json_user_action() == True:
                    continue
                else:
                    return False
            #valid JSON response received
            return True

    def broken_json_user_action(self):
        while True:
            user_choice = input("The model's JSON response is broken, re-request? y/n: ")
            match user_choice.lower():
                case 'y':
                    return True
                case 'n':
                    return False
                case _:
                    print("Invalid selection.")
                    continue

    

    

    #validate construction of unit test commands
    def validate_unittest_functions(self):
        print(); print("-"*40)
        print("Validating Unittest Function CLI commands were created.")
        num_unittests = 0
        num_unittests = ut.count_values_for_keycontain(self.gpt_response_utest, u_test.unittest_cli_command_key)
        return True if num_unittests > 0 else False

    #get list of cli command to execute unit tests
    def create_unittest_cli_list(self, unittest_cli_c_list):
        #Create Unittest cli command List
        num_unittests = ut.count_values_for_keycontain(self.gpt_response_utest,u_test.unittest_cli_command_key)
        print(); print("Gather list of unit test cli commands to run.")
        for index in range(1,int(num_unittests)+1):
            #print("looking for ","".join([u_test.unittest_cli_command_key, str(index)]))
            unittest_cli_c = ut.get_response_value_for_key(self.gpt_response_utest,"".join([u_test.unittest_cli_command_key, str(index)]))
            #print("cli test",unittest_cli_c)
            if len(unittest_cli_c) > 0:
                unittest_cli_c_list.append(unittest_cli_c)
        
        print(f"\033[43mUnit testing CLI Command List Complete.\033[0m") if len(unittest_cli_c_list) > 0 else print("\033[41m[ERROR]Failed to gather Unittesting CLI commands.\033[0m")

    def run_unittests(self, new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name):
        #unit test exception handling
        def exception_handling(choice):
                #request re-populate unittest cli commands
                if choice == "r" or choice == "R":
                    #build request args
                    request_args = self.build_request_regenerate_unittest_cli_comm_args()

                    self.request_code_enhancement(*request_args, u_test = True, new_temp = new_temp, new_engine = new_engine)

                    #goes back to beg while loop
                elif choice == "c" or choice == "C":
                    print(); print("\033[41mContinue testing and skip this unit test.\033[0m")
                else:
                    print(); print("\033[41mSkip running all unit tests.\033[0m")
                    #restore gpt_response to originally received in this function
                    self.gpt_response_utest = tmp_gpt_response

        #store received gpt_response
        tmp_gpt_response = self.gpt_response_utest
        #skip_all = False
        #skip_any = False
        exit_loop = False
        
        #run unit tests
        while True:
            #control var to exit while loop: skip all tests after exception
            exit_loop = False
            if exit_loop:
                break

            unittest_cli_c_list = []

            #Create unittesting cli command list from gpt response
            print(); print("-"*40)
            #Create Unittest CLI command list provided by GPT
            self.create_unittest_cli_list(unittest_cli_c_list)
            for unitt in unittest_cli_c_list:
                print("Unittest command:",unitt)

            #run unittests
            print(); print("-"*40)
            print(f"Running Unittests: {len(unittest_cli_c_list)} tests.")
            print()
            os.chdir(fm.modules_dir)

            comm = None
            test_counter = 0
            for bt in unittest_cli_c_list:
                try:
                    bt_c = bt.replace("python ","")
                    bt_c = bt_c.replace("python3","")
                    comm_list = shlex.split(bt_c)
                    comm = ['python'] + comm_list
                    #TODO: user choose request re-code failure with log: print(); print(f"Running command: {comm}"). Get array cli errors
                    print(f"Running command: {comm}")
                    subprocess.run(comm, check=True)
                    test_counter += 1
                    print(); print("Test:",bt_c)
                except subprocess.CalledProcessError as e:
                    print(f"\n\033[31mError or Exception Thrown running a unit test cli command.:{comm}: {e}\n\033[0m")
                    #TODO: if "No such file or directory" in str(e) or "returned non-zero exit status" in str(e):
                    #error: user interaction
                    print(); print("="*40)
                    print(); print("Please review the code. Attempt to correct or skip:")
                    print(f"\n\033[1;31m[INFO]\033[0m If you skip all unit tests, you can send a Custom Request of the error or auto-debug the logs, both available from the main Menu.", end ="")
                    print()
                    choice = input("=>Press \033[1m(r)\033[0m for the engine to (R)egenerate all cli command errors.\n=>Press \033[1m(s)\033[0m to (S)kip the current unit test and continue to the next one.\n=>Press \033[1m(any key)\033[0m to skip running unit tests.\n\nChoice: ")
                    print(); print("="*40)

                    #take action according to user choice
                    exception_handling(choice)
                    
                    match choice.lower():
                        #regenerate all cli commands
                        case 'r':
                            break
                        #skip this test, continue with the rest
                        case 's':
                            test_counter += 1
                        #skip all tests
                        case _:
                            exit_loop = True
                            break
            
            print("exit loop bottom ",exit_loop, " total-len:", len(unittest_cli_c_list), " counter ",test_counter)
            if exit_loop == True or test_counter == len(unittest_cli_c_list):
                break

        print(); print(f"\033[43mUnit Testing Complete.\033[0m") if not exit_loop else print(f"\033[43mSkipped Unit Tests. Code changes when running these unit tests ignored.\033[0m")

        os.chdir(fm.initial_dir)

    def get_user_debug_request(self):
        while True:
            print(); choice = input("Request debug with log file? y/n: ")
            match choice.lower():
                case 'y':
                    #set engine defaults
                    def_temp = 0.2
                    def_engine = oai.codex_engine_deployment_name
                    #user set engine/temperature
                    return(self.get_user_model_and_temp(def_engine,def_temp))
                    break
                case 'n':
                    return False
                case _:
                    print("Invalid selection.")
                    continue

    def get_user_model_and_temp(self, def_engine,def_temp):
        while True:
            print(); print(f"Default Model: {def_engine[1]} Temperature: {def_temp}")
            cont = input("(A)ccept defaults or (C)hange? a/c: ")
            if cont.lower() == "a":
                print(f"Engine selected: {def_engine[1]} Temperature {def_temp}")
                return (def_engine, def_temp)
            elif cont.lower() == "c":
                while True:
                    print(); choice = input(f"1. Gpt-3.5 Turbo\n2. Codex\nChoose model? ")
                    match choice:
                        case '1':
                            engine = oai.gpt_engine_deployment_name
                            break
                        #skip this test, continue with the rest
                        case '2':
                            engine = oai.codex_engine_deployment_name
                            break
                        case _:
                            print("Invalid model selection.")
                            continue
            else:
                print("Invalid selection.")
                continue

            while True:
                print(); u_temp = input("Enter model temperature (float 0-1): ")
                try:
                    u_temp = float(u_temp)
                except Exception as e:
                    print(f"Invalid temperature {u_temp}. Value must be float or int value 0-1.")
                    continue
                if isinstance(u_temp,float) or isinstance(u_temp, int):
                    if(u_temp >= 0 and u_temp <= 1.0):
                        temp = u_temp
                        print(f"Engine selected: {engine[1]} Temperature {temp}")
                        return (engine,temp)
                    else:
                        print(f"Invalid temperature {u_temp}. Value must be float or int value 0-1.")
                else:
                    print(f"Invalid temperature {u_temp}. Value must be float or int value 0-1.")





#Get raw code JSON object
        #self.program_description = "Program Description: " + "the program is a calculator, collects two numbers from a user and the arithmetic operation to perform being a choice of sum, subtract, multiply or divide. Then print the result on the terminal."
        #self.program_description = "Program Description: " + "The program will prompt the user to enter a sentence or paragraph, and it will count the number of words in the input."
        #self.program_description = "Program Description: " + "The program will generate a random number, and the user will be prompted to guess the number. The program will provide feedback on whether the guess is too high, too low, or correct."
        #self.program_description = "Program Description: " + "The program allows the user to add tasks to a todo list, view the list, and mark tasks as completed."
        #self.program_description = "Program Description: " + "The program allows the user to add tasks to a todo list, view the list, and mark tasks as completed. The code writes, updates and read the resulting list to a file."
        #self.program_description = "Program Description: " + input("")
        


#request ai to validate and clean returned json
    # def validate_and_clean_json(self, u_test = False, custom_json=None, new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name):
    #     print(); print("-"*40);print()
    #     print("Validate JSON Object format.")
        
    #     while True:
    #         try:
    #             #Validate JSON object
    #             if u_test:
    #                 code = ut.get_response_value_for_key(self.gpt_response_utest, raw_code.module_name.split(".")[0])
    #             else:
    #                 code = ut.get_response_value_for_key(self.gpt_response, raw_code.module_name.split(".")[0])
    #             print("\033[43mJSON object is valid.\033[0m")
    #             break
    #         except Exception as e:
    #             #Validation failed - args for JSON clean request
    #             summary_new_request = "JSON Validation failed: Request clean format with existing data."
    #             sys_mssg = clean_json.sys_mssg
    #             json_format = None
    #             if custom_json is not None:
    #                 json_format ='''.JSON Object Template:
    #                 {
    #                 "module":""
    #                 }
    #                 '''
    #             else:
    #                 json_format = custom_json

    #             #request engine to clean JSON obj with existing data
    #             if u_test:
    #                 request_to_gpt = ut.concat_dict_to_string(clean_json.clean_json_instructions_dict) + json_format + ".This is the JSON object for you to validate and correct:" + self.gpt_response_utest
    #             else:
    #                 request_to_gpt = ut.concat_dict_to_string(clean_json.clean_json_instructions_dict) + json_format + ".This is the JSON object for you to validate and correct:" + self.gpt_response

    #             self.send_request(sys_mssg, request_to_gpt,summary_new_request, u_test, new_temp = new_temp, new_engine = new_engine)
