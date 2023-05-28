Generates the code for a program description requested by the user using OpenAI API gpt-3.5-turbo and code-davinci-002 models.

Code additions are added on a per-menu-request basis.

Selected log entries from running unit-tests and the resulting program are sent to GPT for debug.

Project is work in progress.

Repo file structure:
```
.
├── file_management.py		#file management utilities
├── openai_params.py		
├── openai_requests.py		#build, receive and send requests
├── project					#dir: resulting script saved here
├── prompt_txt				#text prompt requests for openai model
│			├── clean_json_rq.py
│			├── error_hndl__logging_rq.py
│			├── input_and_argparse_rq.py
│			├── module_requirements_all.py
│			├── module_requirements_atomic_2.py
│			├── module_requirements_atomic.py
│			├── raw_code_rq.py
│			├── unittest_cli_comm_rq.py
│			└── unittest_rq.py
├── README.md
├── requirements.txt
├── response_json			#dir: response json files
├── sample_self_config.py	#Sample: openai/azure models keys.
├── sg_utils.py				#request management utilities
└── simple_selfgen.py		#Menu block. Requires pointing scripts that import self_config.py (e.g sys.path.append) to dir where you save self_config.py
```