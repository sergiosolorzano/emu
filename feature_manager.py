#!/usr/bin/env python3


#parent of features(base)
import sys
import os
from pathlib import Path

#import class
import feature_base as ft_base
#import feature request classes
import ft_requests.feature_request_utest as ft_req_utest
import ft_requests.feature_request_loadcode as ft_req_loadcode
import ft_requests.feature_request_rawcode as ft_req_raw


#manage feature children classes
class Feature_Manager():

	#init feature children
	def __init__(self):
		#class instances
		#self.user_interaction_instance = uinteraction.User_Interaction()
		#self.log_list_handler_instance = log_list_handler.LogListHandler()
		#instantiate feature base class
		self.feature_base_instance = ft_base.Feature_Base()
		self.feature_instance = None

		#dict of feature instances (children). All in herit from same base to share base instance vars
		self.feature_instances = {
		'1': ft_req_raw.Feature_Request_Rawcode(),
		'2': ft_req_loadcode.Feature_Request_Loadcode(),
		#'3': ft_req_utest.Feature_Request_Argparse(ft_base.Feature_Base, self.user_interaction_instance, self.log_list_handler_instance),
		#'4': ft_req_utest.Feature_Request_ExceptionHndl_and_Logging(ft_base.Feature_Base, self.user_interaction_instance, self.log_list_handler_instance),
		'5': ft_req_utest.Feature_Request_Utest()
		#'6': ft_req_utest.Feature_Request_Run_Unit_Test_Cases(ft_base.Feature_Base, self.user_interaction_instance, self.log_list_handler_instance),
		#'7': ft_req_utest.Feature_Request_CustomRequest(ft_base.Feature_Base, self.user_interaction_instance, self.log_list_handler_instance),
		#'8': ft_req_utest.Feature_Request_DebugLogs(ft_base.Feature_Base, self.user_interaction_instance, self.log_list_handler_instance),
		#'9': ft_req_utest.Feature_Request_Docstrings(ft_base.Feature_Base, self.user_interaction_instance, self.log_list_handler_instance)
		}

	def handle_menu_choice(self, choice):
		#get feature instance according to menu choice
		self.feature_instance = self.feature_instances[choice]
		
		#meet requirements to request args
		ready_to_prepare_request_args = self.feature_instance.prerequest_args_process()
		
		#get request args
		if ready_to_prepare_request_args:
			request_args = self.feature_instance.prepare_request_args()
			
			#do not return back to menu
			return self.feature_instance.request_code(*request_args), False
		else:
			#return back to menu
			return True, True

	def process_valid_response(self):
		return self.feature_instance.process_successful_response()
