#!/usr/bin/env python3
import shlex
import subprocess
# import utils
import tools.file_management as fm
import tools.request_utils as ut
# import request text
import ft_operations.op_run_program as op_deblogs
import ft_requests.feature_request_debuglogs as req_deblogs
import debug_rq as dg_r
# openai
import openai_params as oai
# import config
import config as config


# Request model to debug program with logs
class Op_Run_Program:

    def __init__(self, common_instance):
        self.common_instance = common_instance
        # error when running the program
        self.error_mssg = None
        # command when error occurred
        self.command = None
        self.request_debug_instance = req_deblogs.Feature_Request_DebugLogs(self.common_instance)

    def run_operation(self):
        if self.user_confirm_requirements_for_request():
            while True:
                user_comm_tail = self.get_user_command()
                if user_comm_tail is False:
                    return False

                code_success = self.execute_code(user_comm_tail)
                #exception
                if not code_success:
                    success_request = self.request_debug_instance.request_manager()
                    #if success_request:
                    #    continue

                another_op = self.user_action_next_command_or_menu()
                if another_op:
                    continue
                else:
                    #back to menu
                    return False
        else:
            #back to menu
            return False

    def user_action_next_command_or_menu(self):
        #user choose another command or back to menu
        mssg= "Run another (C)ommand or (M)enu: "
        mssg_option3 = "Invalid choice."

        user_choice = self.common_instance.user_interaction_instance.user_choice_two_options(mssg, mssg_option3=mssg_option3, option1="c",option2="m")
        if user_choice == "c":
            #execute program again
            return True
        else:
            return False

    def get_user_command(self):
        #print(f"\033[44;97mJob: Your Custom Request:\033[0m")
        # user ensure the code has the requirements to run this option
        while True:
            user_comm_tail = self.common_instance.user_interaction_instance.request_input_from_user(
                f"\n(Q)uit or Enter the rest of the CLI command to execute program:\npython3 {config.full_path_module}: ")
            if user_comm_tail.lower() == "q":
                return False
            else:
                return user_comm_tail

    def user_confirm_requirements_for_request(self):
        # run the program with debug/logs loop
        while True:
            user_action = self.common_instance.user_interaction_instance.request_input_from_user(
                f"\n\033[1;31m[WARNING]\033[0m Note on option requirements:\n\t=> Requires logging functionality, logs will be written to {config.initial_dir}/{config.log_fname}\n\t=> Program execution via CLI, you can add args to the code with the Argparse option.\n\t=> This option is not compatible to run unit tests.\n\n(C)ontinue or back to (M)Menu: \033[0m")
            if user_action.lower() == "c":
                return True
            else:
                #back to menu
                return False

    def execute_code(self, user_comm_tail):
        # user enter cli comm and execute
        print("-" * 40)
        self.command = self.request_debug_instance.command = ['python'] + shlex.split(config.full_path_module) + shlex.split(user_comm_tail)
        exception_str = ""
        try:
            # truncate log file
            fm.trunc_file(config.log_fname, config.full_project_dirname)
            print()
            print(f"Running command: {self.command}")
            result = subprocess.run(self.command, check=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
            print("Command executed successfully")
            print(f"Command output: {result.stdout}")
            print(f"Command return code: {result.returncode}")
            print(f"Command stderr: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print("=" * 40)
            print(f"\033[31mSubprocess Exception thrown, log:\033[0m")
            print(f"Command failed with exit code {e.returncode}")
            print(f"Command output: {e.output}")
            print(f"Command error: {e.stderr}")
            if e.stderr or e.returncode != 0 or "error" in e.output.lower():
                exception_str += "subprocess.CalledProcessError command returncode:" + str(e.returncode) \
                                 + f"\nsubprocess.CalledProcessError command error:" + str(e.stderr) \
                                 + f"\nsubprocess.CalledProcessError command output:" + str(e.output)
        except Exception as e:
            print("=" * 40)
            print(f"\033[31mProgram exception thrown, log in file:\033[0m {e}")
            # print("RAW Exception",e);print()
            # print log to logfile and screen
            exception_str += e

        if exception_str != "":
            # add exception message to log_list_handler
            self.common_instance.logger_instance.exception(exception_str)
            # pop log exception
            self.error_mssg = self.request_debug_instance.error_mssg = self.common_instance.log_list_handler_instance.pop()
            # print exception on terminal
            # log_list_handler.print_logs()
            return False

        return True

    def process_successful_response(self):
        self.common_instance.valid_response_file_management(config.module_script_fname, config.full_project_dirname, self.common_instance.gpt_response)
        return True
