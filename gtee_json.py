#!/usr/bin/env python3
import requests
#import credentials
from creds.self_config import self_config
#import tools
import tools.file_management as fm
#import config
import config as config

#Call cerebras/Cerebras-GPT-111M to guarantee JSON format
class Guarantee_JSON:
    cerebras_gpt_111_Base = self_config['HUGGINGFACE_CEREBRAS_GPT_111M_BASE']
    cerebras_gpt_111_Bearer = self_config['huggingface_cerberas_GPT_111M_BEARER']
    def __init__(self):
        self.API_URL = self.cerebras_gpt_111_Base
        self.headers = {"Authorization": self.cerebras_gpt_111_Bearer}

    API_URL = cerebras_gpt_111_Base
    headers = {"Authorization": cerebras_gpt_111_Bearer}

    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()


json_test=fm.read_file_stored_to_buffer("test.txt",config.initial_dir)
guarantee = Guarantee_JSON()
print(guarantee.cerebras_gpt_111_Base, guarantee.cerebras_gpt_111_Bearer)
#json_test = """Correct this JSON object: {""module"": ""def program():\n    #import necessary modules\n    import sqlite3\n\n    #create a connection to the database\n    conn = sqlite3.connect(\'clients.db\')\n\n    #create a cursor object\n    c = conn.cursor()\n\n    #create a table for clients\n    c.execute(\'CREATE TABLE clients\n                (id INTEGER PRIMARY KEY,\n                name TEXT,\n                age INTEGER,\n                email TEXT,\n                phone TEXT)\')\n\n    #add clients to the table\n    c.execute("INSERT INTO clients(name, age, email, phone)\n                VALUES(\'John Doe\', 30, \'johndoe@email.com\', \'555-555-5555\')")\n    c.execute("INSERT INTO clients (name, age, email, phone)\n                VALUES (\'Jane Doe\', 25, \'janedoe@email.com\', \'555-555-5556\')")\n\n    #commit changes to the database\n    conn.commit()\n\n    #close the connection\n    conn.close()\n\nif __name__ == \'__main__\':\n    program()"}"""
#json_test = "My Name is Thomas"
output = guarantee.query({
    "inputs": json_test
})

print("Query output:", output)



