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
    #model generates the code according to user description
    print("1.  Generate Raw Code")
    #you can upload your script instead of the model generating the code
    print("2.  Upload Raw Code Script From File")
    #add argparse
    print("3.  Add Argparse")
    print("4.  Exception Handling and Logging")
    print("5.  Add Unit Test Cases")
    print("6.  Run Unit Test Cases")
    print("7.  User Custom Request")
    print("8.  Run Program And Enter Debug/Logs Loop")
    print("9.  Add Docstrings To Program Code.")
    print("10. Set Menu Sequence")
    print("11. Run All")
    print("12. Exit")

    #TODO: move version_module() to class

    while True:
        print()
        if choice == None:
            choice = input("Choose your request: ")
        else:
            print("Choose your request: ",choice)

        match choice:
            case '1':
                #request code
                oai_req_instance.program_description = "Program Description: " + input("Enter Program Description and Features: ")
                oai_req_instance.request_raw_code(new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name)
                #Validate and correct JSON object
                oai_req_instance.validate_and_clean_json(new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name)
                #Save code into module file
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir, raw_code.module_name)
                return False
            case '2':
                #load user script
                while True:
                    path_to_script = input(f"Enter Path to {raw_code.program_language} Script: ");
                    #check user updated custom json for the request
                    if not os.path.isfile(path_to_script):
                        print(f"\033[1;31m[ERROR]\033[0m Cannot Find Script File {path_to_script}.\033[0m")
                        continue
                    else: 
                        print("Script Found.")
                        break
                
                print()
                oai_req_instance.program_description = "Program Description: " + input("Enter Short Program Description: "); print()

                #read script
                user_script = fm.read_file_stored_to_buffer(os.path.basename(path_to_script), os.path.dirname(path_to_script))
                #hack to step script as a gpt code response for continued conversation with gpt
                oai_req_instance.gpt_response =  fm.insert_script_in_json(user_script)
                print(f"\033[43mScript uploaded.\033[0m")
                return False
            case '3':
                #add argparse
                request_args = oai_req_instance.build_request_input_and_argparse_args()
                oai_req_instance.request_code_enhancement(*request_args, u_test = False, new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name)
                #Validate and correct JSON object
                oai_req_instance.validate_and_clean_json(new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name)
                fm.version_module(fm.modules_dir,raw_code.module_name,fm.modules_dir)
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir, raw_code.module_name)
                return False
            case '4':
                #add exception handling and logging
                request_args = oai_req_instance.build_request_exception_handl_req_args()
                oai_req_instance.request_code_enhancement(*request_args, u_test = False, new_temp = 0.2, new_engine = oai.codex_engine_deployment_name)
                #Validate and correct JSON object
                oai_req_instance.validate_and_clean_json(new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name)
                fm.version_module(fm.modules_dir,raw_code.module_name,fm.modules_dir)
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir, raw_code.module_name)
                return False
            case '5':
                #get cached response as starting point for unit test
                oai_req_instance.gpt_response_utest = oai_req_instance.gpt_response

                #add unit test cases
                request_args = oai_req_instance.build_request_unittest_args()
                while True:
                    oai_req_instance.request_code_enhancement(*request_args, u_test=True, new_temp=0.2, new_engine=oai.codex_engine_deployment_name)
                    #Validate and correct JSON object
                    oai_req_instance.validate_and_clean_json(u_test=False, custom_json=u_test.json_required_format, new_temp=oai.temperature, new_engine=oai.gpt_engine_deployment_name)
                    #Validate unittest cli prompts
                    if oai_req_instance.validate_unittest_functions() == False:
                        print("Unit test functions not created. Re-create unit test code and cli commands.")
                        fm.version_module(fm.modules_dir,raw_code.module_utest_name,fm.modules_dir)
                        continue
                    else:
                        print("\033[43mUnit test functions CLI commands succesfully created.\033[0m")
                        #version and save
                        fm.version_module(fm.modules_dir,raw_code.module_utest_name,fm.modules_dir)
                        fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response_utest(), fm.initial_dir, raw_code.module_utest_name)
                        #TODO: remove for debugging
                        fm.write_to_file(fm.m_json_filename,fm.json_dir, oai_req_instance.get_gpt_response_utest())
                        #end remove for debugging
                        break
                return False
            case '6':
                #run unittests
                #TODO: remove - for debugging
                #if not os.path.exists(os.path.join(fm.json_dir + "/" + fm.m_json_filename)):
                #    print(); print(f"\033[41mJSON file not available.\033[0m")
                #    break
                #print("TEMP - To Remove: JSON Object now only READS from json file I store on instance gpt_response:"); fm.print_json_on_screen(fm.read_file_stored_to_buffer(fm.m_json_filename, fm.json_dir))
                #oai_req_instance.set_gpt_response(fm.read_file_stored_to_buffer(fm.m_json_filename, fm.json_dir))
                #end TODO remove
                #TODO:Tests unit tests were built in the code before executing them
                oai_req_instance.run_unittests()
                fm.version_module(fm.modules_dir,raw_code.module_utest_name,fm.modules_dir)
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response_utest(), fm.initial_dir, raw_code.module_utest_name)
                return False
            case '7':
                #add user custom request
                print(); print(f"\n\033[1;31m[WARNING]\033[0m Unit tests generated by model is not by this option.\033[0m")
                inputs = get_user_inputs_custom_request()
                #check user updated custom json for the request
                if isinstance(inputs, bool) and inputs == False:
                    print(f"\n\033[1;31m[ERROR]\033[0m Cannot process request if the custom json file is not updated.\033[0m")
                    return False

                path_to_json = os.path.join(fm.m_custom_json_dirname + "/" + fm.m_custom_json_filename)
                if not os.path.exists(path_to_json):
                    print(); print(f"\n\033[1;31m[ERROR]\033[0m Cannot Find Custom JSON File {path_to_json}.\033[0m")
                    return False
                custom_json = fm.read_file_stored_to_buffer(fm.m_custom_json_filename, fm.m_custom_json_dirname)

                #build prompt request
                #user inputs tuple into variable for clarity
                custom_sys_req_input = inputs[0]
                custom_conv_req_input = inputs[1]

                request_args = oai_req_instance.build_request_custom_user_args(custom_sys_req_input, custom_conv_req_input, custom_json)
                #send request
                oai_req_instance.request_code_enhancement(*request_args, u_test = False, new_temp = 0.2, new_engine = oai.codex_engine_deployment_name)

                #Validate and correct JSON object
                oai_req_instance.validate_and_clean_json(new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name)
                fm.version_module(fm.modules_dir,raw_code.module_name,fm.modules_dir)
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir, raw_code.module_name)

                #print(); print(f"\033[41mPending Implementation.\033[0m")
                return False
            
            case '8':
                #TODO: run program and enter debug log loop
                print(); print(f"\033[41mPending Implementation.\033[0m")
                return False
            case '9':
                #add docstrings
                #TODO:consider sphinx to present to users for Read the Docs platform support
                request_args = oai_req_instance.build_request_docstrings_args()
                oai_req_instance.request_code_enhancement(*request_args, u_test = False, new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name)
                #Validate and correct JSON object
                oai_req_instance.validate_and_clean_json(new_temp = oai.temperature, new_engine = oai.gpt_engine_deployment_name)
                fm.version_module(fm.modules_dir,raw_code.module_name,fm.modules_dir)
                fm.get_dict_value_save_to_file(oai_req_instance.get_gpt_response(), fm.initial_dir, raw_code.module_name)
                return False  
            case '10':
                #TODO: User Set Menu Sequence
                print(); print(f"\033[41mPending Implementation.\033[0m")
                return False    
            case '11':
                #run all menu configurations
                print(); print("-"*40);print()
                #TODO: update range to menu range
                for i in range(1,10):
                    request_menu(oai_req_instance, str(i))
                return False
            case '12':
                #exit program
                return True
            case _:
                print(); print(f"\033[41mInvalid Option\033[0m")
                return False

def get_user_inputs_custom_request():
    print(); print("Enter request to change the code:")
    custom_sys_req_input = input("Part 1/3 - Enter Short System Prompt: "); print()
    custom_conv_req_input = input("Part 2/2 - Enter Conversation Prompt: ")
    
    while True:
        #update custom json response
        custom_json_req_input = input("Part 3/3 - Did you update your JSON Response? y/n: ")

        #cannot process request if custom json not updated
        if custom_json_req_input.lower() == "n":
            return False
        elif custom_json_req_input.lower() == "y":
            break
        else:
            continue

    return (custom_sys_req_input, custom_conv_req_input)

def prompt_user_cont_or_menu(mssg):
    while True:
        print(mssg)
        choice = input("=>Press \033[1m(c)\033[0m to Continue.\n=>Press \033[1m(m)\033[0m back to Menu.\n\nChoice: ")
        print(); print("="*40)

        #take action according to user choice
        exception_handling(choice)
        
        match choice.lower():
            case 'c':
                return True
            case 'm':
                return False
            case _:
                continue

def main():
    #delete project files / create project dirs where scripts will be stored
    fm.create_dir(Path(fm.modules_dir))
    fm.create_dir(Path(fm.json_dir))

    #del all project module files
    #TODO option to delete
    fm.delete_all_dir_files(fm.modules_dir)
    print(); print("-"*40);print()
    print("\033[43mSlate Clean - Project files deleted. Project directories created.\033[0m")

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




    