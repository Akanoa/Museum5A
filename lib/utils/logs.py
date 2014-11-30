import time
from math import ceil

from lib.colorama import init, Fore, Back, Style

class Logger:
	"""
		Contain static vars for logger use 
	"""

	separatorColor = Fore.YELLOW + Style.BRIGHT
	nameAppColor = Fore.CYAN + Style.NORMAL
	timeColor = Fore.MAGENTA + Style.NORMAL
	fromModuleColor = Fore.WHITE + Style.BRIGHT

	#TAG COLOR SECTION
	criticalTagColor = Fore.RED + Style.BRIGHT
	errorTagColor = Fore.RED + Style.NORMAL
	warningTagColor = Fore.YELLOW + Style.BRIGHT
	infoTagColor = Fore.GREEN + Style.NORMAL 
	otherTagColor = Fore.CYAN
	debugTagColor = Fore.MAGENTA + Style.BRIGHT

	resetConsole = Fore.RESET + Style.NORMAL + Back.RESET

	version = "0.1.0"
	startTime = 0;
	pathToFile = None
	logMode = 3;
	tagColors = {}

	def __init__(self):
		self.setStartTime()
		
		#init colorama lib
		init()

		self.tagColors["CRITICAL"] = self.criticalTagColor
		self.tagColors["ERROR"] = self.errorTagColor
		self.tagColors["WARNING"] = self.warningTagColor
		self.tagColors["INFO"] = self.infoTagColor
		self.tagColors["DEBUG"] = self.debugTagColor
		self.tagColors["OTHERS"] = self.otherTagColor

		self.separator = self.separatorColor + " :: " + self.resetConsole
		self.header = 	self.separatorColor + ".::" + self.resetConsole +\
						self.nameAppColor + " Museum v" + self.version + self.resetConsole + \
			 			self.separatorColor + " :: " + self.resetConsole

	def setVariableFromConfig(self, logModeValue, pathToFileValue):
		"""
			Set variables for the logging system from the config.ini file
		"""
		self.logMode = int(logModeValue)
		self.pathToFile = pathToFileValue

		self.logIt (fromModule = "logs - setVariableFromConfig" , tag = "INFO", content = "Log mode is setting to : " + str(logModeValue))
		self.logIt (fromModule = "logs - setVariableFromConfig" , tag = "INFO", content = "Path to file is setting to : " + pathToFileValue)

		#overwrite previous log if necessary
		if (self.logMode == 3 or self.logMode == 2):
			f = open(self.pathToFile + "museum.log", 'w')
			f.close()

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

	def logIt (self, fromModule = "Unknow Module" , tag = "INFO", content = "No content received" ):
		"""
			Main function which handle the incoming request from the whole program to print some log ( in file or in console, depending on settings)
		"""
		#no logs mode ?

		if self.logMode != 0:
			currentTime = time.time() - self.startTime
			currentTime = ceil(currentTime * 100000) / 100000.0

			selectedTagColor = "";

			if tag in self.tagColors :
				selectedTagColor = self.tagColors[tag]
			else:
				selectedTagColor = self.tagColors["OTHERS"]

			#if console mode
			if (self.logMode == 3) or (self.logMode == 1):
				print( 	self.header +
						self.timeColor + str(currentTime) + self.resetConsole + self.separator +
						self.fromModuleColor + fromModule + self.resetConsole +
						self.separatorColor + " ::. " + self.resetConsole +
						self.separatorColor + "[" + self.resetConsole +
						selectedTagColor + tag + self.resetConsole + 
						self.separatorColor + "] " + self.resetConsole +
						content
						)

			#log file
			if (self.logMode == 3) or (self.logMode == 2):
				toLog = ".:: Museum v" + self.version + " :: " + str(currentTime) + " :: " + fromModule + " ::. [" + tag + "] " + content + "\n"
				f = open(self.pathToFile + "museum.log", 'a')
				f.write(toLog.encode('UTF-8'))
				f.close()




