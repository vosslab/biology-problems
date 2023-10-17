import logging

def setup_logger():
	# Create a logger object
	logger = logging.getLogger()

	# Configure logger to DEBUG level
	logger.setLevel(logging.DEBUG)

	# Create a console handler and set level to debug
	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.DEBUG)

	# Create a formatter
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

	# Add formatter to the handler
	console_handler.setFormatter(formatter)

	# Add the handler to logger
	logger.addHandler(console_handler)
