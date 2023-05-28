#!/usr/bin/env python3

#import libraries
import sys
import os
import subprocess
import shlex
import time
import threading
from pathlib import Path

#profiler
import cProfile

#self import modules
import file_management as fm

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

#gpt user request menu
def request_menu(oai_req_instance, choice=None):
    print(); print("-"*40);print()
    print("1.  Raw Code: Program Description Code")
    print("2.  User Input and Argparse")
    print("3.  Exception Handling and Logging")
    print("4.  Add Unittest Code")
    print("5.  User custom request")
    print("6.  Run Unittest")
    print("7.  Update 'main()' For User Interaction")
    print("8.  Run Program and enter debug/log loop")
    print("9.  Add Docstrings to program code.")
    print("10. Run All")
    print("11. Exit")

    #TODO: move version_module() to class

    while True:
        print()
        if choice == None:
            choice = input("Choose your request: ")
        else:
            print("Choose your request: ",choice)

        match choice:
            case '1':
                #create project dirs where scripts will be stored
                fm.create_dir(Path(fm.modules_dir))
                fm.create_dir(Path(fm.json_dir))

                #del all project module files
                #TODO option to delete
                fm.delete_all_dir_files(fm.modules_dir)

                #request code
                oai_req_instance.request_raw_code()
                #Validate and correct JSON object
                oai_req_instance.validate_and_clean_json()
                #Save code into module file
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir)
                return False
            case '2':
                #request enhancements to code
                request_args = oai_req_instance.build_request_input_and_argparse_args()
                oai_req_instance.request_code_enhancement(*request_args)
                #Validate and correct JSON object
                oai_req_instance.validate_and_clean_json()
                fm.version_module(fm.modules_dir,raw_code.module_name,fm.modules_dir)
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir)
                return False
            case '3':
                #request enhancements to code
                request_args = oai_req_instance.build_request_exception_handl_req_args()
                oai_req_instance.request_code_enhancement(*request_args, new_temp = 0.2, new_engine = oai.codex_engine_deployment_name)
                #Validate and correct JSON object
                oai_req_instance.validate_and_clean_json()
                fm.version_module(fm.modules_dir,raw_code.module_name,fm.modules_dir)
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir)
                return False
            case '4':
                #request enhancements to code
                request_args = oai_req_instance.build_request_unittest_args()
                while True:
                    oai_req_instance.request_code_enhancement(*request_args, new_temp = 0.2, new_engine = oai.codex_engine_deployment_name)
                    #Validate and correct JSON object
                    oai_req_instance.validate_and_clean_json(u_test.json_required_format)
                    #Validate unittest cli prompts
                    if oai_req_instance.validate_unittest_functions() == False:
                        print("Unit test functions not created. Re-create unit test code and cli commands.")
                        fm.version_module(fm.modules_dir,raw_code.module_name,fm.modules_dir)
                        continue
                    else:
                        print("\033[43mUnit test functions CLI commands succesfully created.\033[0m")
                        #version and save
                        fm.version_module(fm.modules_dir,raw_code.module_name,fm.modules_dir)
                        fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir)
                        #TODO: remove, for debugging
                        fm.write_to_file(fm.m_json_filename,fm.json_dir, oai_req_instance.get_gpt_response())
                        break
                return False
            case '5':
                #TODO user custom requested enhancements to code
                #custom_json='''''
                #self.validate_and_clean_json(custom_json)
                print(); print(f"\033[41mPending Implementation.\033[0m")
                return False
            case '6':
                #run unittests
                #TODO: remove - for debugging
                if not os.path.exists(os.path.join(fm.json_dir + "/" + fm.m_json_filename)):
                    print(); print(f"\033[41mJSON file not available.\033[0m")
                    break
                print("TEMP - To Remove: JSON Object now only READS from json file I store on instance gpt_response:"); fm.print_json_on_screen(fm.read_file_stored_to_buffer(fm.m_json_filename, fm.json_dir))
                oai_req_instance.set_gpt_response(fm.read_file_stored_to_buffer(fm.m_json_filename, fm.json_dir))
                #end of TODO remove -- for debugging
                #TODO:Tests unit tests were built in the code before executing them
                oai_req_instance.run_unittests()
                fm.version_module(fm.modules_dir,raw_code.module_name,fm.modules_dir)
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir)
                return False
            case '7':
                #TODO: update for main to execute with user inputs, not uttest
                print(); print(f"\033[41mPending Implementation.\033[0m")
                return False    
            case '8':
                #TODO: run program and enter debug log loop
                print(); print(f"\033[41mPending Implementation.\033[0m")
                return False
            case '9':
                #consider sphinx to present to users for Read the Docs platform support
                print(); print(f"\033[41mPending Implementation.\033[0m")
                return False  
            case '10':
                #run all menu configurations
                print(); print("-"*40);print()
                #TODO: update range to menu range
                for i in range(1,10):
                    request_menu(oai_req_instance, str(i))
                return False
            case '11':
                #exit program
                return True
            case _:
                print(); print(f"\033[41mInvalid Option\033[0m")
                return False

def main():
    #set showing request text on screen
    oai_requests.Openai_Requests.set_show_request(True)
    #create openai request instance
    oai_req_instance = oai_requests.Openai_Requests()

    exit_user_request = False

    #launch menu
    while exit_user_request == False:
        #print(); print("-"*40);print()
        exit_user_request = request_menu(oai_req_instance)

    #profiler
    print(); print("="*10,end=""); print("Profiler Stats",end="");print("="*10)
    import pstats
    p = pstats.Stats("profiler_data.out")

    print(); print("="*10,end=""); print("Total Cumulative Stats",end="");print("="*10)
    p.sort_stats("cumulative").print_stats(5)

    print(); print(f"\033[43mThe program has exited at the user's request.\033[0m");print()
    #exit(0)

    #Run the program
    # print(); print("-"*40)
    # print(f"Show help to execute program {os.path.join(fm.modules_dir, mr_atomic.module_name)}")
    # os.chdir(fm.modules_dir)
    # this_program=mr_atomic.module_name
    # comm_list = shlex.split(this_program)
    # comm = ['python'] + comm_list
    # print()
        
    # try:    
    #     print(f"Running command: {comm}")
    #     subprocess.run(comm)
    # except Exception as e:
    #     print(f"Exception running {mr_atomic.module_name} script: {e}")

    # os.chdir(fm.initial_dir)


    print(); print("-"*40); print("End of Script"); print()

if __name__ == "__main__":
    #true if your code is invoked directly(stand-alone), e.g. python3 source_file.py
    #main()

    cProfile.run("main()","profiler_data.out")




    