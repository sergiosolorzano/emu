#!/usr/bin/env python3

import os
from pathlib import Path
#import classes
import user_interaction as uinteraction
import feature_manager as ft_mgr
#import profiler
import cProfile
import pstats
#import tools
import tools.file_management as fm


#TODO: Refactor into config file
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

#manage program workflow with all classes
class Emu_cli:
    #init program classes
    def __init__(self):
        self.feature_manager_instance = ft_mgr.Feature_Manager()
        self.user_interaction_instance = uinteraction.User_Interaction()

    def handle_workflow(self):
        #request menu choice from user
        while True:
            menu_choice = self.user_interaction_instance.request_menu()
            while True:
                success, back_to_menu = self.feature_manager_instance.handle_menu_choice(menu_choice)
                if back_to_menu:
                    break
                if not success:
                    #broken JSON response, ask for user action
                    if self.user_interaction_instance.broken_json_user_action():
                        #user choice to request code from model again
                        continue
                    else:
                        print("JSON is invalid, returning to main menu at user's request.")
                        break
                #valid JSON response received
                else:
                    if not self.feature_manager_instance.process_valid_response():
                        #something went wrong, request again from model
                        continue
                    else:
                        #done
                        break

def main():
    # TODO option to delete
    # del all project module files and responses in json stored
    fm.delete_all_dir_files(full_project_dirname)
    fm.delete_all_dir_files(full_json_dir)
    # delete project files / create project dirs where scripts will be stored
    fm.create_dir(Path(full_project_dirname))
    fm.create_dir(Path(full_json_dir))

    print(); print("-" * 40); print()
    print("\033[43mSlate Clean - Project files deleted. Project directories created.\033[0m")

    #create emu_manager instance
    emu = Emu_cli()
    emu.handle_workflow()

    # profiler
    # print(); print("=" * 10, end="")
    # print("Profiler Stats", end="")
    # print("=" * 10)
    # p = pstats.Stats("profiler_data.out")
    #
    # print(); print("=" * 10, end="")
    # print("Total Cumulative Stats", end=""); print("=" * 10)
    # p.sort_stats("cumulative").print_stats(5)
    #
    # print(); print(f"\033[43mThe program has exited at the user's request.\033[0m"); print()
    #
    # print(); print("-" * 40)
    # print("End of Script"); print()

if __name__ == "__main__":
    #cProfile.run("main()","profiler_data.out")
    main()
