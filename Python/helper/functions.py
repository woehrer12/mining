import logging
import os

def initlogger(file):
	if not os.path.isdir("./logs"):
		os.mkdir("./logs")
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	handler = logging.FileHandler("logs/"+ file)
	formatter = logging.Formatter('%(asctime)s:%(levelname)s-%(message)s')
	handler.setFormatter(formatter)
	handler.setLevel(logging.INFO)
	logger.addHandler(handler)
