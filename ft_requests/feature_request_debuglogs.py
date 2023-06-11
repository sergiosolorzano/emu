#!/usr/bin/env python3
import shlex
import subprocess
#import utils
import tools.file_management as fm
import tools.request_utils as ut
#import request text
import debug_rq as dg_r
#openai
import openai_params as oai

#Request model to debug program with logs
class Feature_Request_DebugLogs:

    def __init__(self, common_instance):
        self.common_instance = common_instance
        # error when running the program
        self.error_mssg = None
        # command when error occurred
        self.command = None

    def prerequest_args_process(self):
        #user ensure the code has the requirements to run this option
        if self.user_confirm_requirements_for_request():
            while True:
                user_comm_tail = self.common_instance.user_interaction_instance.request_input_from_user(
                    f"\n(Q)uit or Enter the rest of the CLI command to execute program:\npython3 {self.common_instance.full_path_module}: ")
                if user_comm_tail.lower() == "q":
                    return False, True

                if not self.execute_prog(user_comm_tail.lower()):
                    #exception occurred
                    #write exception to log file: append cos program writes logs to same log file. Next loop log file is truncated.
                    fm.write_to_file(self.common_instance.log_fname,self.common_instance.full_project_dirname, str("\n\n" + self.error_mssg), "a")
                    print("="*40)

                    if self.user_action_debug_or_not():
                        #user chose to send logs on request for debug, not back to menu
                        return True, False
                else:
                    #user chose not debug current error
                    if self.user_action_next_command_or_menu():
                        #user chose run another command
                        continue
                    else:
                        #user chose back to menu
                        return False, True

        else:
            #no further request, back to menu
            return False, True

    def execute_prog(self, user_comm_tail):
        #user enter cli comm and execute
        print("-"*40)
        exception_flag = False
        self.command = ['python'] + shlex.split(self.common_instance.full_path_module) + shlex.split(user_comm_tail)
        exception_str = ""
        try:
            #truncate log file
            fm.trunc_file(self.common_instance.log_fname, self.common_instance.full_project_dirname)
            print(); print(f"Running command: {self.command}")
            result = subprocess.run(self.command, check=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
            print("Command executed successfully")
            print(f"Command output: {result.stdout}")
            print(f"Command return code: {result.returncode}")
            print(f"Command stderr: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print("="*40); print(f"\033[31mSubprocess Exception thrown, log:\033[0m")
            exception_flag = True
            print(f"Command failed with exit code {e.returncode}")
            print(f"Command output: {e.output}")
            print(f"Command error: {e.stderr}")
            if e.stderr or e.returncode != 0 or "error" in e.output.lower():
                exception_str += "subprocess.CalledProcessError command returncode:" + str(e.returncode) \
                + f"\nsubprocess.CalledProcessError command error:" + str(e.stderr) \
                + f"\nsubprocess.CalledProcessError command output:" + str(e.output)
        except Exception as e:
            print("="*40); print(f"\033[31mProgram exception thrown, log:\033[0m")
            exception_flag = True
            #print("RAW Exception",e);print()
            #print log to logfile and screen
            exception_str += e

        if exception_str != "":
            # add exception message to log_list_handler
            self.common_instance.logger_instance.exception(exception_str)
            # pop log exception
            self.error_mssg = self.common_instance.log_list_handler_instance.pop()
            # print exception on terminal
            # log_list_handler.print_logs()
            return False

        return True

    def user_action_next_command_or_menu(self):
        #user choose another command or back to menu
        mssg= "Run another (C)ommand or (M)enu: "

        if self.common_instance.user_interaction_instance.user_choice_two_options(mssg, option1="c",option2="m") == "c":
            #execute program again
            return True
        else:
            return False

    def prepare_request_args(self):
        #request args
        summary_new_request = "Change the code to correct errors shown in the log file."
        sys_mssg = dg_r.sys_mssg
        request_to_gpt = f'''You will make specific changes to this JSON object: {self.common_instance.gpt_response}.
        \nThis is the description of what the program does in the the code found in the value for key 'module' of the JSON object:\n{self.common_instance.program_description}.
        \n{ut.concat_dict_to_string(dg_r.debug_instructions_dict)}\n\n{dg_r.command}{self.command}\n\n{dg_r.error}{self.error_mssg}'''

        args_tpl = (summary_new_request, sys_mssg, request_to_gpt)
        return args_tpl
            
    def user_confirm_requirements_for_request(self):
        #run the program with debug/logs loop
        while True:
            user_action = self.common_instance.user_interaction_instance.request_input_from_user(f"\n\033[1;31m[WARNING]\033[0m Note on option requirements:\n\t=> Requires logging functionality, logs will be written to {fm.initial_dir}/{fm.m_module_log_filename}\n\t=> Program execution via CLI, you can add args to the code with the Argparse option.\n\t=> This option is not compatible to run unit tests.\n\n(C)ontinue or back to (M)Menu: \033[0m")
            if user_action.lower() == "c":
                #request logging from model
                return True
            else:
                return False

    def user_action_debug_or_not(self):
        while True:
            print(); choice = input("Request debug with log file? y/n: ")
            match choice.lower():
                case 'y':
                    #set engine defaults
                    self.common_instance.model_temp = 0.2
                    self.common_instance.model = oai.codex_engine_deployment_name
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
                    print(); choice = input(f"1. Gpt-3.5 Turbo\n2. Codex\nChoose model? ")
                    match choice:
                        case '1':
                            self.common_instance.model = oai.gpt_engine_deployment_name
                            break
                        case '2':
                            self.common_instance.model = oai.codex_engine_deployment_name
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
                    else:
                        print(f"Invalid temperature {u_temp}. Value must be float or int value 0-1.")
                else:
                    print(f"Invalid temperature {u_temp}. Value must be float or int value 0-1.")

    #send request to model
    def request_code(self, *request_args):
        #override base instance vars
        self.common_instance.u_test_bool = False
        #run base request implementation
        return self.common_instance.request_code_enhancement(*request_args)

    def process_successful_response(self):
        self.common_instance.valid_response_file_management(self.common_instance.module_script_fname, self.common_instance.full_project_dirname, self.common_instance.gpt_response)
        return True