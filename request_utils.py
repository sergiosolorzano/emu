#!/usr/bin/env python3

import tiktoken
import openai_params as oai
import json
import time
import threading

#globals

#calculate tokens in messages list
#def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
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
	
def count_values_for_keycontain(gpt_response, keycontain):
    count = 0
    for k,v in gpt_response.items():
        if keycontain in k:
            count += 1
    return count

#concatinate dict values to a string
def concat_dict_to_string(mydict):
    all_concat_values=""
    all_concat_values = "\n\n".join(this_value for this_value in mydict.values())
    return all_concat_values

def token_limit(tokens_used_snapshot):
    if tokens_used_snapshot >= oai.token_limit:
        print("Reached max tokens. Continue (c) or any key to exit.")
        cont = input("")
        if cont.lower() != "c" or cont.lower() != "C":
            print(); print("Exiting at user request.")
            exit()

def spinning_timer(message, stop_evt):
    spinner = "|/-\\"
    idx = 0
    while not stop_evt.is_set():
        print('\r\033[92m' + message + spinner[idx] + '\033[0m', end='')
        idx = (idx + 1) % len(spinner)
        time.sleep(0.17) #secs



