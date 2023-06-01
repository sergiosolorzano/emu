#!/usr/bin/env python3

import sys
import os
import subprocess
import json
from pathlib import Path

#TODO: add user option for programming language and module filename
#TODO:fn and dir module
m_root = os.getenv("HOME")
m_prompt_dirname = "prompt_txt"
m_project_dirname = "project"
m_json_dirname = "response_json"

sys.path.append(m_root)
initial_dir = os.getcwd()
sys.path.append(f'{initial_dir}/{m_prompt_dirname}')
#dir to store module files
modules_dir=f"{initial_dir}/{m_project_dirname}"
json_dir = f"{initial_dir}/{m_json_dirname}"

#import initial raw code request requirements, requires paths above
import raw_code_rq as raw_code
#import my utils
import sg_utils as ut

m_json_filename = "response.json"
m_custom_json_dirname = "custom_json"
m_custom_json_filename = "custom_json.json"
m_module_log_filename = raw_code.module_log_fname

def create_empty_module(module_name, initial_dir):
	#change to modules dir
	print()
	os.chdir(modules_dir)

    #create module file and chmod
	path_and_fn = Path(modules_dir) / module_name
	path_and_fn.touch()
	print("-"*40)
	print(f"File created: {path_and_fn}")
	
	#return back to initial dir
	os.chdir(initial_dir)

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
		full_path=os.path.join(path, filename)
		Path(full_path).write_text(snippet)
		print(Path(full_path).read_text())

def clean_up_module(code):
	code = code.replace("```", "")
	return code

def trunc_file(filename,path):
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
				print(); print(f"\033[43mResponse saved to JSON file {full_path}\033[0m");

def get_dict_value_save_to_file(gpt_response, initial_dir, filename, header=""):
    print(); print("-"*40)
    code = ut.get_response_value_for_key(gpt_response,raw_code.module_name.split(".")[0])
    print("Code:"); print(); print(code)
    destination_full_name = os.path.join(modules_dir, filename)
    if not os.path.exists(destination_full_name):
        create_empty_module(filename, initial_dir)
    #add bash to script
    code = header + code
    write_to_file(filename,modules_dir,code, "w")

def version_module(path_original_fn, original_fn, path_dest_fn):
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
			
	command = f"cp {original_full_path_fn} {destination_full_name}"
	subprocess.run(command, shell=True)
	print(); print("-"*40);print()
	print(f"\033[43mVersion saved: {command}\033[0m")

def read_file_stored_to_buffer(filename,path):
		full_path=os.path.join(path, filename)
		path_to_file = Path(path,filename)
		ext = path_to_file.name.split(".")[1]

		if ext != "json":
			return Path(full_path).read_text()

		#https://gist.github.com/tomschr/86a8c6f52b81e35ac4723fef8435ec43
		with Path(full_path).open(encoding="UTF-8") as buff:
			return json.load(buff)

def print_json_on_screen(json_data):
        #print(); print("JSON Data:\n");
        print(json.dumps(json_data, indent=2, separators=(',', ':')))

def insert_script_in_json(a_script):
    json_dict = {"module":a_script}
    #return json obj
    json_str = json.dumps(json_dict)
    a = json.loads(json_str)
    return json.loads(json_str)

def delete_all_dir_files(target_dir):
		#del all project module files
		with os.scandir(target_dir) as this_dir:
			for file_name in this_dir:
				if file_name.is_file():
					os.remove(os.path.join(modules_dir, file_name))

def create_dir(target_dir):
        #os.makedirs(target_dir, exist_ok=True)
        target_dir.mkdir(parents=False, exist_ok=True)


