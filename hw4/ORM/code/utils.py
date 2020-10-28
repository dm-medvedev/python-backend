import logging


def get_logger(name):
	"""
	name - module name

	https://docs.python.org/3/howto/logging.html
	https://docs.python.org/3/howto/logging-cookbook.html
	"""
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG) # minimal level
	file_handler = logging.FileHandler("ORM.log")
	file_handler.setLevel(logging.DEBUG)
	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.ERROR) # higher level
	formatter = logging.Formatter('%(asctime)s - %(name)s - '
	                              '%(levelname)s - %(message)s')
	file_handler.setFormatter(formatter)
	console_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)
	return logger