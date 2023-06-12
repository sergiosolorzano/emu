#!/usr/bin/env python3

#import utils
import tools.file_management as fm
import tools.request_utils as ut
#import request text
import prompt_txt.docstrings_rq as docs_r

#request add docstrings to code
class Run_All:

    def __init__(self, common_instance):
        self.common_instance = common_instance

