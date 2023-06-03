#!/usr/bin/env python3

#import libraries
import sys
import os
import subprocess
import shlex
import time
import threading
from pathlib import Path
import logging

import shlex
import log_list_handler as c_log
import json

#profiler
import cProfile

#self import modules
import request_utils as ut

#TODO: make class
sys.path.append(fm.m_root)
sys.path.append(f'{fm.initial_dir}/{fm.m_prompt_dirname}')

#import openai libs/modules
import openai_params as oai

#import program classes
import openai_requests as oai_requests

#import data to request module code
#import initial raw code request requirements
import raw_code_rq as raw_code
import unittest_rq as u_test
import file_management as fm

#NEW: import request functionality classes (base's children)
import feature_request_utest as ft_req_utest
#import tools
import user_interaction as uinteraction
import feature_manager as ft_mgr
import file_management as fm
import request_utils as req_utils #TODO:need this?
import log_list_requests as custom_log_hdl # TODO:need this?

#manage program workflow with all classes
class Selfgen_Manager():
    #init program classes
    def __init__(self):
        self.user_interaction = uinteraction.User_Interaction()
        self.feature_manager = ft_mgr.Feature_Manager()
        #self.file_manager = fm.File_Manager()
        #self.request_utils = req_utils.Request_Utils()#TODO:need this?
        self.log_list_handler = custom_log_hdl.LogListHandler() #TODO:need this?


    def handle_workflow(self):
    #request menu choice from user
    while True:
        menu_choice = uinteraction.request_menu()
        while True:
            if self.feature_manager.handle_menu_choice(menu_choice) == False
            #broken JSON response, ask for user action
                if uinteraction.broken_json_user_action() == True:
                    continue
                else:
                    return False
            #valid JSON response received
            return True







def main():
    #create selfgen_manager instance
    selfgen_mgr = Selfgen_Manager()
    selfgen_mgr.handle_workflow()

if __name__ == "__main__":
    cProfile.run("main()","profiler_data.out")

