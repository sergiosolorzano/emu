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
    #init program classes
    def __init__(self):
        self.feature_manager_instance = ft_mgr.Feature_Manager()
        self.menu_choice = None
        self.success = None
        self.back_to_menu = None

    def handle_workflow(self):
        if self.feature_manager_instance.get_menu_choice() is False:
            return



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
    emu.handle_workflow()
    os.chdir(config.initial_dir)
    # profiler
    print()
    print("=" * 10, end="")
    print("Profiler Stats", end="")
    print("=" * 10)

    print()
    print("=" * 10, end="")
    print("Total Cumulative Stats", end="")
    print("=" * 10)
    p = pstats.Stats(profiler_file)
    p.sort_stats("cumulative").print_stats(5)

    print(f"\033[43mThe program has exited at the user's request.\033[0m"); print()

    print("-" * 40)
    print("End of Script"); print()

if __name__ == "__main__":
    profiler_file = "profiler_data.out"
    cProfile.run("main()",profiler_file)
