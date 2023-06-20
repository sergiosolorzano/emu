#!/usr/bin/env python3

#import class
import feature_common as ft_common
import user_interaction as uinteraction
#import feature request classes
import ft_operations.op_loadcode as op_loadcode
import ft_operations.op_run_program as op_deblogs
import ft_requests.feature_request_rawcode as ft_req_raw
import ft_requests.feature_request_argparse as ft_req_argparse
import ft_requests.feature_request_excpt_and_log as ft_req_excpt_and_log
import ft_requests.feature_request_custom_req as ft_req_custom_req
import ft_requests.feature_request_docstrings as ft_req_docstrings

#manage feature children classes
class Feature_Manager:

	menu_exit_choice = '10'
	menu_sequence_choice = '8'
	menu_runall_choice = '9'
	menu_op_choices = ['2', '6']
	menu_feature_choices = ['1', '3', '4', '5', '7']
	menu_all_available_choices = ['1','3', '4', '7', '5', '6']

	#init feature children
	def __init__(self):
		#instantiate feature common class
		self.feature_common_instance = ft_common.Feature_Common()
		self.user_interaction_instance = uinteraction.User_Interaction()
		self.feature_instance = None
		self.menu_choice = None
		self.pre_request_complete = False
		self.prepare_args_complete = False
		self.send_request_complete = False
		self.back_to_menu = False
		self.args = None

		#dict of feature instances, pass shared common instance
		self.feature_instances = {
		'1': ft_req_raw.Feature_Request_Rawcode(self.feature_common_instance),
		'2': op_loadcode.Op_Loadcode(self.feature_common_instance),
		'3': ft_req_argparse.Feature_Request_Argparse(self.feature_common_instance),
		'4': ft_req_excpt_and_log.Feature_Request_ExceptionHndl_and_Logging(self.feature_common_instance),
		'5': ft_req_custom_req.Feature_Request_CustomRequest(self.feature_common_instance),
		'6': op_deblogs.Op_Run_Program(self.feature_common_instance),
		'7': ft_req_docstrings.Feature_Request_Docstrings(self.feature_common_instance)
		}

	def get_menu_choice(self):
		sequence = []
		while True:
			#self.reset_vars_end_process()
			self.menu_choice = self.user_interaction_instance.request_menu()

			if self.menu_choice == '10':
				return False

			if self.menu_choice == self.menu_sequence_choice:
				sequence = self.get_sequence()
				print("Executing Sequence:",sequence)

			elif self.menu_choice == self.menu_runall_choice:
				sequence= self.menu_all_available_choices
				print("Executing Sequence:",sequence)

			else:
				sequence = self.menu_choice
			for c in sequence:
				self.menu_choice = str(c)

				if self.menu_choice == '10':
					return False

				self.feature_instance = self.feature_instances[self.menu_choice]
				self.handle_menu_choice()
				self.reset_vars_end_process()

	def handle_menu_choice(self):
		if self.feature_common_instance.gpt_response is None and (self.menu_choice != '1' and self.menu_choice != '2'):
			return
		else:
			while True:
				if self.menu_choice in self.menu_feature_choices:
					if self.pre_request_complete is False:
						self.pre_request_complete = self.feature_instance.prerequest_args_process()

					if self.pre_request_complete and self.prepare_args_complete is False:
						self.args = self.feature_instance.prepare_request_args()
						if self.args:
							self.prepare_args_complete = True

					if self.prepare_args_complete and self.send_request_complete is False:
						self.send_request_complete = self.feature_instance.request_code(self.args)

						if not self.send_request_complete:
							if self.user_interaction_instance.broken_json_user_action():
								# user choice to request code from model again
								print("JSON IS BROKEN, send request again now.")
								continue

				if self.menu_choice in self.menu_op_choices:
					run_op_completed = self.feature_instance.run_operation()

					if not run_op_completed:
						break
				if self.feature_common_instance.gpt_response is not None:
					self.process_valid_response()

				break

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

	def process_valid_response(self):
		self.feature_instance.process_successful_response()


	def reset_vars_end_process(self):
		#print("Resetting vars at manager")
		self.feature_instance = None
		self.menu_choice = None
		self.pre_request_complete = False
		self.prepare_args_complete = False
		self.send_request_complete = False
		self.back_to_menu = False
		self.args = None
