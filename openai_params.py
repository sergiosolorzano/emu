
#openai key/base, models
from creds.self_config import self_config
import tiktoken
import openai

#available models
gpt_engine_deployment_name = (self_config['gpt_engine_deployment_name'], "gpt-3.5-turbo-0301")
codex_engine_deployment_name = (self_config['gpt_engine_deployment_name'], "code-davinci-002")
#set model
deployment_name = gpt_engine_deployment_name

#auth
openai.api_type = self_config['OPENAI_API_TYPE']
openai.api_version = self_config['OPENAI_API_VERSION']
openai.api_base = self_config['OPENAI_API_BASE']
openai.api_key = self_config['OPENAI_API_KEY']

#token accounting
cum_tokens = 0
max_response_tokens = 3000
token_limit= 4096
#we don't accumulate conversations
#arch_conversation=[]
#module_conversation=[]

#openai request params#TODO delete temp, now set at request_feature
temperature = 0.7
