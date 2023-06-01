#!/usr/bin/env python3

import logging

class LogListHandler(logging.Handler):
	def __init__(self, *args, **kwargs):
		super(LogListHandler, self).__init__(*args, **kwargs)
		self.log_records = []

	def emit(self, record):
		self.log_records.append(self.format(record))

	def pop(self):
		return self.log_records.pop()

	def print_logs(self):
		print("Logs:")
		for c, l in enumerate(self.log_records):
			print(f"Log {c}: {l}")


#create custom logger
def config_custom_logger():
    # Create an instance of LogListHandler
    log_list_handler = LogListHandler()

    log_list_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_list_handler.setFormatter(formatter)

    #add logger
    logger = logging.getLogger(__name__)
    logger.addHandler(log_list_handler)
    logger.setLevel(logging.DEBUG)

    return logger, log_list_handler
    
