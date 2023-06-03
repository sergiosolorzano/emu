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
        '5': ft_req_utest.Feature_Request_Utest(self.feature_base_instance)
        }

	def handle_menu_choice(self, choice):
		#get feature instance according to menu choice
		feature_instance = self.feature_instances[choice]
		#get request args
		request_args = feature_instance.build_unittest_request_args()
		#request code
		return feature_instance.request_code(*request_args)
				

		
