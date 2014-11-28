import time
from math import ceil

class Logger:
	"""
		Contain static vars for logger use 
	"""
	startTime = 0;
	version = "0.1.0"
	header = ".:: Museum v" + version + " :: "

	def __init__(self):
		self.setStartTime()

	def setStartTime (self):
		"""
			Set start Time
			Can be called only once
		"""
		if self.startTime == 0 : self.startTime = time.time()

	def getTimedHeader (self):
		"""
			Return header with integrated timestamp
		"""
		currentTime = time.time() - self.startTime
		currentTime = ceil(currentTime * 100000) / 100000.0

		result = self.header + str(currentTime) + " :: "
		return result


logger = Logger()