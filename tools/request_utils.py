#!/usr/bin/env python3

import tiktoken
import openai_params as oai
import time
#import config_dir
from config_dir import config as config


#calculate tokens in messages list
def num_tokens_from_messages(messages, model=oai.deployment_name[1]):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

#read from gpt-response the list of modules to create, create these in directory
def get_response_value_for_key(gpt_response, key):
    return gpt_response[key]

def count_values_for_keycontain(gpt_response, thiskeycontain):
    count = 0
    for k, v in gpt_response.items():
        if thiskeycontain in k:
            count += 1
    return count

#concatinate dict values to a string
def concat_dict_to_string(mydict):
    all_concat_values = "\n\n".join(this_value for this_value in mydict.values())
    return all_concat_values

def token_limit(tokens_used_snapshot):
    if tokens_used_snapshot >= config.token_limit:
        print(f"Reached max tokens {tokens_used_snapshot} of {config.token_limit}. Continue (c) or any key to exit.")
        cont = input("")
        if cont.lower() != "c":
            print(); print("Exiting at user request.")
            exit()

def spinning_timer(message, stop_evt):
    spinner = "|/-\\"
    idx = 0
    while not stop_evt.is_set():
        print('\r\033[92m' + message + spinner[idx] + '\033[0m', end='')
        idx = (idx + 1) % len(spinner)
        time.sleep(0.17) #secs

#get list of cli command to execute unit tests
def create_unittest_cli_list(unittest_cli_c_list, gpt_response_utest, unittest_cli_command_key):
    #Create Unittest cli command List
    num_unittests = count_values_for_keycontain(gpt_response_utest,unittest_cli_command_key)
    print(); print("Gather list of unit test cli commands to run.")
    for index in range(1, int(num_unittests)+1):
        unittest_cli_c = get_response_value_for_key(gpt_response_utest,"".join([unittest_cli_command_key, str(index)]))
        #print("cli test",unittest_cli_c)
        if len(unittest_cli_c) > 0:
            unittest_cli_c_list.append(unittest_cli_c)
    
    print(f"\033[43mUnit testing CLI Command List Complete.\033[0m") if len(unittest_cli_c_list) > 0 else print("\033[41m[ERROR] Failed to gather Unittesting CLI commands.\033[0m")
    return  unittest_cli_c_list


