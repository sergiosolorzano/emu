#!/usr/bin/env python3
import cProfile
import os
from pathlib import Path
#import config
import config as config
#import classes
import user_interaction as uinteraction
import feature_manager as ft_mgr
import pstats
#import tools
import tools.file_management as fm

#manage program workflow with all classes
class Emu_cli:
    #menu choice that does not create a feature / instantiate a class
    menu_type_choices = [8, 9, 10]

    #init program classes
    def __init__(self):
        self.feature_manager_instance = ft_mgr.Feature_Manager()
        self.user_interaction_instance = uinteraction.User_Interaction()
        self.menu_choice = None
        self.success = None
        self.back_to_menu = None

    def handle_workflow(self):
        while True:
            print("In while loop handle_workflow choice ", self.menu_choice)
            # implementation of selected feature
            self.success, self.back_to_menu = self.feature_manager_instance.handle_menu_choice(self.menu_choice)
            if self.back_to_menu:
                print("Going back to menu")
                return True
            if not self.success:
                #broken JSON response, back to menu
                if self.user_interaction_instance.broken_json_user_action():
                    #user choice to request code from model again
                    print("JSON IS BROKEN")
                    continue
                else:
                    print("JSON is invalid, returning to main menu at user's request.")
                    return True
            #valid JSON response received
            else:
                print("At Else")
                if not self.feature_manager_instance.process_valid_response():
                    #something went wrong, request again from model
                    print("VALID RESPONSE NOT VALID")
                    continue
                else:
                    if self.back_to_menu:
                        print("At bottom back to menu")
                        return True
                    else:
                        #done
                        print("AT ELSE BOTTOM")
                        continue

    def reset_vars(self):
        self.menu_choice = None
        self.success = None
        self.back_to_menu = None

    def menu_user_choice(self):
        print("At top menu_user_choice choice ", self.menu_choice)
        # request menu choice from user
        if self.menu_choice is None:
            self.menu_choice = self.user_interaction_instance.request_menu()
        print("At medium menu_user_choice choice ", self.menu_choice)
        outcome = True
        match self.menu_choice:
            case '1' | '2' | '3' | '4' | '5' | '6' | '7':
                self.menu_choice = str(self.menu_choice)
                outcome = self.handle_workflow()
                self.reset_vars()
                return outcome
            case '8':
                requested_seq = self.get_sequence()
                for seq_num in requested_seq:
                    self.menu_choice = str(seq_num)
                    outcome = self.handle_workflow()
                    self.reset_vars()
                return outcome
            case '9':
                for seq_num in [1,3,4,5,6,7]:
                    self.menu_choice=str(seq_num)
                    outcome = self.handle_workflow()
                    self.reset_vars()
                return outcome
            case '10':
                #exit
                return False
            case _:
                #back to menu
                return True

    def get_sequence(self):
        while True:
            mssg = "Provide number sequence in menu execution separated by commas: "
            user_seq = self.user_interaction_instance.request_input_from_user(mssg)
            numbers = []

            for item in user_seq.split(','):
                item = item.strip()
                if item.isdigit():
                    numbers.append(int(item))
                else:
                    print("Invalid sequence.")

            return numbers

def main():
    # TODO option to delete
    # del all project module files and responses in json stored
    fm.delete_all_dir_files(config.full_project_dirname)
    fm.delete_all_dir_files(config.full_json_dir)
    # delete project files / create project dirs where scripts will be stored
    fm.create_dir(Path(config.full_project_dirname))
    fm.create_dir(Path(config.full_json_dir))

    print(); print("-" * 40); print()
    print("\033[43mSlate Clean - Project files deleted. Project directories created.\033[0m")

    #create emu_manager instance
    emu = Emu_cli()
    while True:
        print("Calling emu.handle_workflow() from main")
        emu.reset_vars()
        if emu.menu_user_choice() is False:
            break

    #profiler
    print(); print("=" * 10, end="")
    print("Profiler Stats", end="")
    print("=" * 10)
    p = pstats.Stats("profiler_data.out")

    print(); print("=" * 10, end="")
    print("Total Cumulative Stats", end=""); print("=" * 10)
    p.sort_stats("cumulative").print_stats(5)

    print(f"\033[43mThe program has exited at the user's request.\033[0m"); print()

    print("-" * 40)
    print("End of Script"); print()

if __name__ == "__main__":
    cProfile.run("main()","profiler_data.out")
