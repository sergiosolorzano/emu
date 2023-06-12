#!/usr/bin/env python3


#parent of features(base)
import sys
import os
from pathlib import Path

#import class
import feature_common as ft_common
#import feature request classes
import ft_requests.feature_request_utest as ft_req_utest
import ft_requests.feature_request_loadcode as ft_req_loadcode
import ft_requests.feature_request_rawcode as ft_req_raw
import ft_requests.feature_request_argparse as ft_req_argparse
import ft_requests.feature_request_excpt_and_log as ft_req_excpt_and_log
import ft_requests.feature_request_runutests as ft_req_run_utests
import ft_requests.feature_request_custom_req as ft_req_custom_req
import ft_requests.feature_request_debuglogs as ft_req_deblogs
import ft_requests.feature_request_docstrings as ft_req_docstrings

#manage feature children classes
class Feature_Manager:

	#init feature children
	def __init__(self):
		#class instances
		#self.user_interaction_instance = uinteraction.User_Interaction()
		#self.log_list_handler_instance = log_list_handler.LogListHandler()
		#instantiate feature base class
		self.feature_common_instance = ft_common.Feature_Common()
		self.feature_instance = None

		#dict of feature instances, pass shared common instance
		self.feature_instances = {
		'1': ft_req_raw.Feature_Request_Rawcode(self.feature_common_instance),
		'2': ft_req_loadcode.Feature_Request_Loadcode(self.feature_common_instance),
		'3': ft_req_argparse.Feature_Request_Argparse(self.feature_common_instance),
		'4': ft_req_excpt_and_log.Feature_Request_ExceptionHndl_and_Logging(self.feature_common_instance),
		'5': ft_req_utest.Feature_Request_Utest(self.feature_common_instance),
		'6': ft_req_run_utests.Feature_Request_Run_Unit_Test_Cases(self.feature_common_instance),
		'7': ft_req_custom_req.Feature_Request_CustomRequest(self.feature_common_instance),
		'8': ft_req_deblogs.Feature_Request_DebugLogs(self.feature_common_instance),
		'9': ft_req_docstrings.Feature_Request_Docstrings(self.feature_common_instance)
		#'10': menu_seq.Create_Menu_Sequence(self.feature_common_instance),
		#'11': run_all.Run_All(self.feature_common_instance),
		#'12': exit_app.Exit_Application(self.feature_common_instance)
		}

	def handle_menu_choice(self, choice):
		#get feature instance according to menu choice
		self.feature_instance = self.feature_instances[choice]

		#meet requirements to request args
		ready_to_prepare_request_args, back_to_menu = self.feature_instance.prerequest_args_process()
		#get request args
		if ready_to_prepare_request_args:
			request_args = self.feature_instance.prepare_request_args()

			#do not return back to menu
			return self.feature_instance.request_code(*request_args), back_to_menu
		else:
			#return back to menu
			return True, back_to_menu

	def process_valid_response(self):
		return self.feature_instance.process_successful_response()
