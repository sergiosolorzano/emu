#!/usr/bin/env python3

#parent of features(base)
import feature_base as ft_base
#features (children)
import feature_request_utest as ft_req_utest

#manage feature children classes
class Feature_Manager():

    #init feature children
    def __init__(self):
    	#instantiate feature base class
    	self.feature_base_instance = ft_base.Feature_Base()
    	#dict of feature instances (children). All in herit from same base to share base instance vars
        self.feature_instances = {
        '1': ft_req_utest.Feature_Request_Rawcode(self.feature_base_instance),
        '2': ft_req_utest.Feature_Request_Loadcode(self.feature_base_instance),
        '3': ft_req_utest.Feature_Request_Argparse(self.feature_base_instance),
        '4': ft_req_utest.Feature_Request_ExceptionHndl_and_Logging(self.feature_base_instance),
        '5': ft_req_utest.Feature_Request_Utest(self.feature_base_instance),
        '9': ft_req_utest.Feature_Request_Docstrings(self.feature_base_instance),
        }

	def handle_menu_choice(self, choice):
		#get feature instance according to menu choice
		feature_instance = self.feature_instances[choice]
		#get request args
		request_args = feature_instance.prepare_request_args()
		
		if request_args == None:
			#not a request, do something else
			return feature_instance.choice_not_a_request()
		else:
			#request code
			return feature_instance.request_code(*request_args)

	def process_valid_response(self, success_mssg):
		#if processing fails re-
		return feature_instance.process_successful_response()
				

		
