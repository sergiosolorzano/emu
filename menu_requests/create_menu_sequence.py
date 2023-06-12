#!/usr/bin/env python3

#import utils
import tools.file_management as fm
import tools.request_utils as ut
#import request text
import prompt_txt.docstrings_rq as docs_r

#request add docstrings to code
class Create_Menu_Sequence:

    def __init__(self, user_interaction_instance):
        self.user_interaction_instance = user_interaction_instance

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
