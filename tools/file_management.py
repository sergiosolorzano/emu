#!/usr/bin/env python3

import os
import subprocess
import shutil
import json
from pathlib import Path
#import my utils
import tools.request_utils as ut
#import config_dir
from config_dir import config as config


def create_empty_module(module_name, ini_dir):
	#change to modules dir
	print()
	os.chdir(config.full_project_dirname)

	#create module file and chmod
	path_and_fn = Path(config.full_project_dirname) / config.module_script_fname
	path_and_fn.touch()
	print("-"*40)
	print(f"File created: {path_and_fn}")
	
	#return back to initial dir
	os.chdir(ini_dir)

def get_unlabelled_dict(labelled_list, target_label):
	for pos, ele in enumerate(labelled_list):
		if ele[0] == target_label:
			mod_desc = {}
			for mod,desc in ele[1].items():
				mod_desc[mod] = desc
			return mod_desc

def get_unlabelled_list(labelled_list, target_label):
	unlabelled_list = []
	for pos, ele in enumerate(labelled_list):
		if ele[0] == target_label:
			for e in labelled_list[pos]:
				if e != target_label:
					unlabelled_list.append(e)
			return unlabelled_list

def write_snippet_to_file(filename,path,snippet):
	if len(snippet) > 0:
		full_path = os.path.join(path, filename)
		Path(full_path).write_text(snippet)
		print(Path(full_path).read_text())

def clean_up_module(code):
	code = code.replace("```", "")
	return code

def trunc_file(filename, path):
	#check file exists else create
	if not os.path.exists(os.path.join(path, filename)):
		create_empty_module(filename, path)
	#truncate file
	path_to_file = Path(path,filename)
	with path_to_file.open("w") as f:
		f.truncate(0)

def write_to_file(filename,path,content, access_mode):
	if len(content) > 0:
		print("-"*40)
		path_to_file = Path(path,filename)
		ext = path_to_file.name.split(".")[1]
		full_path=os.path.join(path, filename)
		if ext == "py" or ext == "log":
			if access_mode != "a":
				#Path(full_path).write_text(f"#!/usr/bin/env python3\n\n{content}")
				Path(full_path).write_text(content)
			else:
				with Path(full_path).open(access_mode) as f:
					f.write(content)

			if ext == "py":
				comm = ["sudo", "chmod", "+x", full_path]
				subprocess.run(comm)
				print(f"Executed command {comm}")
				print("-"*40); print()
				print(f"\033[43mCode saved to module file {full_path}\033[0m")
		elif ext == "json":
			#overwrite only
			with Path(full_path).open("w") as target: 
				json.dump(content, target)
				print(); print(f"\033[43mResponse saved to JSON file {full_path}\033[0m")

def get_dict_value_save_to_file(gpt_response, ini_dir, filename, header=""):
	print(); print("-"*40)
	#code = ut.get_response_value_for_key(gpt_response, raw_code.module_name.split(".")[0])
	code = get_code_from_dict(gpt_response, config.code_key_in_json)
	#print("Code:"); print(); print(code)
	destination_full_name = os.path.join(config.full_project_dirname, filename)
	if not os.path.exists(destination_full_name):
		create_empty_module(filename, ini_dir)
	#add bash to script
	code = header + code
	write_to_file(filename, config.full_project_dirname, code, "w")

def get_code_from_dict(gpt_response, dict_key):
	return ut.get_response_value_for_key(gpt_response, dict_key)

def version_file(path_original_fn, original_fn, path_dest_fn):
	original_full_path_fn = os.path.join(path_original_fn, original_fn)
	extension = original_fn.split(".")[1]
	fn = original_fn.split(".")[0]
	counter = 1

	while True:
		new_filename = f"{fn}_{counter}.{extension}"
		destination_full_name = os.path.join(path_dest_fn, new_filename)
		if not os.path.exists(original_full_path_fn):
			break
		elif os.path.exists(destination_full_name):
			counter += 1
		else:
			break

	print(); print("-" * 40); print()
	try:
		shutil.copy(original_full_path_fn, destination_full_name)
		print(f"\033[43mVersion saved: {destination_full_name}\033[0m")
	except FileNotFoundError as e:
		print(f"\033[43mNo versioning at this point.\033[0m")
		pass

def read_file_stored_to_buffer(filename, path):
	full_path = os.path.join(path, filename)
	path_to_file = Path(path, filename)
	# if not os.path.isfile(path_to_file):
	# 	print(f"\033[1;31m[ERROR]\033[0m Cannot Find Script File {path_to_file}\033[0m")
	ext = path_to_file.name.split(".")[1]

	if ext != "json":
		return Path(full_path).read_text()

	#thanks to https://gist.github.com/tomschr/86a8c6f52b81e35ac4723fef8435ec43
	with Path(full_path).open(encoding="UTF-8") as buff:
		return json.load(buff)

def print_json_on_screen(json_data):
	print(json.dumps(json_data, indent=2, separators=(',', ':')))

def insert_script_in_json(a_script):
	script_dict = {"module": a_script}
	return script_dict

def delete_all_dir_files(target_dir):
	#del all project module files
	if os.path.exists(target_dir):
		with os.scandir(target_dir) as this_dir:
			for file_name in this_dir:
				if file_name.is_file():
					os.remove(os.path.join(config.full_project_dirname, file_name))

def create_dir(target_dir):
	#os.makedirs(target_dir, exist_ok=True)
	target_dir.mkdir(parents=False, exist_ok=True)

def validate_filepath(full_path_to_script):
	if not os.path.isfile(full_path_to_script):
		print(f"\033[1;31m[ERROR]\033[0m Cannot Find File {full_path_to_script}\033[0m")
		return False
	else:
		print("File Found.")
		if os.access(full_path_to_script, os.R_OK):
			return True
		else:
			print(f"\033[1;31m[ERROR]\033[0m File {full_path_to_script} not readable\033[0m")
			return False



