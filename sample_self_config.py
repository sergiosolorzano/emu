#Azure EndPoints
self_config_azure_openai = {'OPENAI_API_BASE': 'https://[YOUR AZURE OPENAI NAME].openai.azure.com/',
'OPENAI_API_KEY':'[YOUR KEY]',
'OPENAI_API_TYPE':'azure',
'OPENAI_API_VERSION':'2023-03-15-preview',
'gpt_engine_350301_deployment_name':'[YOUR MODEL DEPLOYMENT NAME]',
'codex_engine_002_deployment_name':'[YOUR MODEL DEPLOYMENT NAME]',
'davincitext_003_deployment_name':'[YOUR MODEL DEPLOYMENT NAME]',
"gpt_engine_350301_name": "[YOUR MODEL NAME]",
"codex_engine_002_name": "[YOUR MODEL NAME]",
"davincitext_engine_003_name": "[YOUR MODEL NAME]"
}

self_config_openai_api = {'OPENAI_API_KEY':'[YOUR KEY]',
'OPENAI_ORGANIZATION':'[YOUR ORGANIZATION ID]',
'gpt_engine_350613_deployment_name':'[YOUR MODEL DEPLOYMENT NAME]',
"codex_engine_002_deployment_name": "[YOUR MODEL DEPLOYMENT NAME]",
'davincitext_003_deployment_name':'[YOUR MODEL DEPLOYMENT NAME]',
"gpt_engine_350613_name": "[YOUR MODEL NAME]",
"codex_engine_002_name": "c[YOUR MODEL NAME]",
"davincitext_engine_003_name": "[YOUR MODEL NAME]"
}

#enhance with other models
self_config_huggingface = {'HUGGINGFACE_CEREBRAS_GPT_111M_BASE':'https://api-inference.huggingface.co/models/cerebras/Cerebras-GPT-111M',
'huggingface_cerberas_GPT_111M_BEARER':'[YOUR KEY]'
}