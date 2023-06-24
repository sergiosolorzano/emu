#!/usr/bin/env python3
from enum import Enum
#openai key/base, models
from creds.self_config import self_config_azure_openai
from creds.self_config import self_config_openai_api

import openai

#api enum
class Model_API:
    #avaialble APIs
    AZURE_OPENAI_API=0
    OPENAI_API=1

#set api for this session
used_api = Model_API.AZURE_OPENAI_API

#available models
primary_engine_deployment_name=None
secondary_engine_deployment_name=None
tertiary_engine_deployment_name=None

if used_api == Model_API.AZURE_OPENAI_API:
    primary_engine_deployment_name = (self_config_azure_openai['gpt_engine_35_deployment_name'], "gpt-3.5-turbo-0301")
    secondary_engine_deployment_name = (self_config_azure_openai['codex_engine_deployment_name'], "code-davinci-002")
    tertiary_engine_deployment_name = (self_config_azure_openai['davincitext_engine_deployment_name'], "text-davinci-003")

    openai.api_type = self_config_azure_openai['OPENAI_API_TYPE']
    openai.api_version = self_config_azure_openai['OPENAI_API_VERSION']
    openai.api_base = self_config_azure_openai['OPENAI_API_BASE']
    openai.api_key = self_config_azure_openai['OPENAI_API_KEY']

    temperature = 0.7

elif used_api == Model_API.OPENAI_API:
    primary_engine_deployment_name = (self_config_openai_api['gpt_engine_35_deployment_name'], "gpt-3.5-turbo-0613")
    secondary_engine_deployment_name = (self_config_openai_api['davinci3_engine_deployment_name'], "text-davinci-003")

    openai.organization = self_config_openai_api['OPENAI_ORGANIZATION']
    openai.api_key = self_config_openai_api['OPENAI_API_KEY']

    temperature = 0.7
else:
    pass

#set model
deployment_name = primary_engine_deployment_name
#print("***",deployment_name,openai.api_key,openai.organization)
#openai.Model.list()