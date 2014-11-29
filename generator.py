#Generator.py
#Date : 15/10/2014

import xml.etree.ElementTree as ET
import random
import os, os.path
import xml.dom.minidom as minidom
import imp
from math import sqrt, floor
import StringIO

from maze import *
from mazeView import *

from lib.utils import *

useTkInter = False

try:
	import Tkinter
	import tkMessageBox
	useTkInter = True
except ImportError:
	print logger.getTimedHeader() + " main :: [WARNING] TkInter not installed, displaying question in console ...."

class Generator:
	'''
	generation of xml file
	'''
	def __init__(self, config="defaultMuseum"):
		self.root = ET.Element('xml')

		self.texturePath = "datas/textures/"

		self.paintingPath = self.texturePath + "paintings/"
		self.listPaintings = os.listdir(self.paintingPath)

		self.texturesWallPath = self.texturePath + "wall/" 
		self.listTexWall = os.listdir(self.texturesWallPath)

		self.texturesCeilingPath = self.texturePath + "ceiling/" 
		self.listTexCeiling = os.listdir(self.texturesCeilingPath)

		self.texturesGroundPath = self.texturePath + "ground/" 
		self.listTexGround = os.listdir(self.texturesGroundPath)

		self.defaultTypeDoors = ["big","normal","void"]

		self.textsPath = "datas/texts/"
		self.textsPaintingsPath = self.textsPath + "paintings/"

		self.prepareDefaultParameters()
		self.generateNewMuseum()
		self.exportToFile(config)

	def prepareDefaultParameters(self):
		'''
		Write defaut parameters on top of the tree
		'''
		tree = ET.parse("museum.xml")											##Default params
		doc = tree.getroot()
		defaultParams = doc.find('default')

		dimensions = defaultParams.find('dimensions')
		self.defaultDimensionsNb = int (sqrt(int(dimensions.get("nb"))))

		paintings = defaultParams.find('paintings')
		self.defaultPaintingsPath = paintings.get("path")

		textures = defaultParams.find('textures')

		groundAndCeil = textures.findall("texture")
		self.defaultGroundTexture = groundAndCeil[0].get("path")
		self.defaultCeilTexture = groundAndCeil[1].get("path")

		walls = textures.find('walls')
		listWall = walls.findall('wall')
		self.defaultWallsTextures = []
		for i in range(len(listWall)):
			self.defaultWallsTextures.append(listWall[i].get('path'))

		signalisation = defaultParams.find('signalisation')
		self.defaultSignalisationDirection = signalisation.get("direction")

		self.root.append(defaultParams)


	def generateNewMuseum(self):
		'''
			Generate a new random museum
		'''
		rowsAsked  = self.defaultDimensionsNb
		colsAsked = self.defaultDimensionsNb
		#Generate a new maze with minimum size
		searchedPath = floor((rowsAsked * colsAsked) * 0.7)

		print logger.getTimedHeader() + "GenerateNewMuseum::. [INFO] Number of row : " + str(rowsAsked)
		print logger.getTimedHeader() + "GenerateNewMuseum::. [INFO] Number of columns : " + str(colsAsked)
		print logger.getTimedHeader() + "GenerateNewMuseum::. [INFO] Minimum size asked for the path: " + str(searchedPath)

		generated = maze_search(rowsAsked,colsAsked, searchedPath)
		maze = self.memoMaze = generated[0]
		cellList = maze.maze
		path = generated[1]

		prepareWall = self.generateWallProperty(maze);
	
		rooms = ET.Element('rooms')

		# fetch row
		for i in range(maze.rows):
			#fetch columns
			for j in range(maze.cols):
				#listWall = self.createWallProperty(maze, i,j)
				listWall = prepareWall[i][j]

				#Select a set of paintings, get path to textures directory
				paintingSelected = self.choosePaintingSet()

				#Select a set of textures for ceiling, ground and wa;;s
				roomTextureSet = self.chooseRoomTexture()

				#calculate new id
				actualID = i * maze.rows + j

				#Signalisation
				signalisation = self.obtainSignalisation(path,i,j)

				#generate xml
				room = self.generateRoomXml(actualID, listWall, paintingSelected, roomTextureSet, signalisation)

				#add it to root xml
				rooms.append(room)

		self.root.append(rooms)

	def generateWallProperty (self, mazeValue):
		cellList = mazeValue.maze
		wallTypes = [[["void",None,"void",None] for j in range(mazeValue.cols)] for i in range(mazeValue.rows)]

		for i in range(mazeValue.rows):
			for j in range(mazeValue.cols):
				#override left parameters if on the first raw
				if (j == 0):
					wallTypes[i][j][0] = "wall"

				if (i == 0):
					wallTypes[i][j][2] = "wall"

				if not cellList[i][j][0]:							#Bottom
					wallTypes[i][j][3] = self.chooseDoorType()
				else:
					wallTypes[i][j][3] = "wall"
					
				if not cellList[i][j][1]:							#Right
					wallTypes[i][j][1] = self.chooseDoorType()
				else:
					wallTypes[i][j][1] = "wall"

		return wallTypes

	def getOppositeDirection(self, direction):
		'''
			return the opposite direction for the direction given in parameters
		'''
		if (direction == 0):
			return 1
		elif (direction == 1):
			return 0
		elif (direction == 2):
			return 3
		elif (direction == 3):
			return 2
		else:
			return 10							#none

	def choosePaintingSet(self):
		'''
			Return path to paintings for the a room using random choice from the list 
			Remove the paintings from the original list to prevent duplication
		'''
		resultRand = random.randint(0, len(self.listPaintings)-1)
		paintingSet = self.listPaintings[resultRand]
		#del self.listPaintings[resultRand]

		return paintingSet

	def chooseRoomTexture(self):
		'''
			Return textures data for the current room
			format return [pathToGround, pathToCeiling, [left,right,up,down]]
		'''
		resultRand = random.randint(0, len(self.listTexGround)-1)
		pathToGround = self.listTexGround[resultRand]

		resultRand = random.randint(0, len(self.listTexCeiling)-1)
		pathToCeiling = self.listTexCeiling[resultRand]

		wallList = []
		for i in range(4):
			resultRand = random.randint(0, len(self.listTexWall)-1)
			wallList.append(self.listTexWall[resultRand])

		return [pathToGround,pathToCeiling,wallList]

	def chooseDoorType(self):
		'''
			return a door type choosen randomy
		'''
		resultRand = random.randint(0, len(self.defaultTypeDoors)-1)
		doorChoosen = self.defaultTypeDoors[resultRand]
		return doorChoosen

	def generateRoomXml(self,id,listWall, paintingSelected, roomTextureSet, signal):
		'''
			Generate XMl tree of a room using the given parameters
		'''
		room = ET.Element('room')
		room.set("id",str(id))

		############Doors part##############
		doors = ET.Element('doors')

		#check all walls
		for w in range( len(listWall)):
			typeDoorCurrent = listWall[w]
			if (typeDoorCurrent != "wall"):
				door = ET.Element('door')
				door.set("direction",self.varToStr(w))
				door.set("type",typeDoorCurrent)
				doors.append(door)
		room.append(doors)

		###########Paintings Part###########
		if (paintingSelected != self.defaultPaintingsPath):		#Default Parameters
			paintings = ET.Element('paintings')

			#old version ; number of textures in files
			#counter = len([name for name in os.listdir(self.defautPaintingPath + paintingSelected) if os.path.isfile(os.path.join(self.defautPaintingPath + paintingSelected, name))])

			#new version ; randint
			counter = random.randrange(4, 15)

			paintings.set("nb",str(counter))
			paintings.set("path",paintingSelected)
			room.append(paintings)

		##########Room Texture set##########
		textures = ET.Element('textures')
		isTexturesFilled = False
		isWallsFilled = False

		if roomTextureSet[0] != self.defaultGroundTexture :
			ground = ET.Element("texture")
			ground.set("path",roomTextureSet[0])
			ground.set("type", "ground")
			textures.append(ground)
			isTexturesFilled = True

		if roomTextureSet[1] != self.defaultCeilTexture :
			ceil = ET.Element("texture")
			ceil.set("path",roomTextureSet[1])
			ceil.set("type", "ceiling")
			textures.append(ceil)
			isTexturesFilled = true

		walls = ET.Element("walls")
		for i in range(len(roomTextureSet[2])):
			if roomTextureSet[2][i] != self.defaultWallsTextures[i] :
				wall = ET.Element("wall")
				wall.set("path",roomTextureSet[2][i])
				wall.set("type",self.varToStr(i))
				walls.append(wall)
				isWallsFilled = True

		if isWallsFilled : textures.append(walls)
		if isTexturesFilled | isWallsFilled: room.append(textures)

		###########Signalisation############
		if (signal != self.defaultSignalisationDirection):		#default parameters, don't write
			signalisation = ET.Element('signalisation')
			signalisation.set("direction",signal)
			room.append(signalisation)

		return room

	def varToStr(self, value):
		"""
			Return string corresponding to the given value
		"""

		if (value == 2):
			return "up"
		elif (value == 3):
			return "down"
		elif (value == 1):
			return "right"
		elif (value == 0):
			return "left"
		else:
			return "unknow"

	def obtainSignalisation(self, path, x, y ):
		"""
			Get the corresponding signalisation ( direction up/down/right/left ) for the actual cell
		"""
		for index, item in enumerate(path):
			if (x,y) == item:
				#We are on the optimal path, searching for the next cell to get signalisation
				if (index == 0) :
					return "begin"
				else :
					if (index + 1 < len(path)):
						nextItem = path[index+1]
						if ((x+1,y) == nextItem):
							return "right"
						elif ((x-1,y) == nextItem):
							return "left"
						elif ((x,y+1) == nextItem):
							return "down"
						elif ((x,y-1) == nextItem):
							return "up"
						else :
							return "WTF"
					else : 
						return "end"
		return "N/A"

	def exportToFile(self, nameFile = "defaultMuseum"):
		fileDirectory = ""
		fileName = nameFile + ".xml"
		fileDirectory = "datas/generated/" + nameFile + "/"
		self.writeDirectory = fileDirectory

		print logger.getTimedHeader() + "exportToFile::. [INFO] Exporting XML Tree to file '" + fileName + "'' in directory '" + fileDirectory + "'"
		
		#check if generated dir exist
		if not os.path.exists("datas/generated"):
			os.makedirs("datas/generated")

		#Generated of the directory for given museum if not exist
		if not os.path.exists(fileDirectory):
			os.makedirs(fileDirectory)

		#delete all files into the directory ( remove img and xml file )
		listFiles = os.listdir(fileDirectory)
		for i in xrange(len(listFiles) ):
			os.remove(fileDirectory + listFiles[i])

		#format the xml nicely
		rough_string = ET.tostring(self.root, method="xml", encoding='UTF-8')
		buf = StringIO.StringIO(rough_string)
		bufferLine = buf.readline()
		resultString = ""

		while len (bufferLine ) > 0:
			list_char = list(bufferLine)
			sizeList = len (list_char)
			while ( sizeList > 0):
				if list_char[0] ==  '<' :
					if (list_char[sizeList-1] == '\n') : 
						del list_char[-1]
					resultString += "".join(list_char)
					break;
				else :
					list_char.pop(0)
				sizeList = len (list_char)
			bufferLine = buf.readline()

		reparsed = minidom.parseString(resultString)
		reparsed = reparsed.toprettyxml(indent="\t")

		#Write to filedddd
		f = open(fileDirectory+ fileName, 'w')
		f.write(reparsed)
		f.close()
		print logger.getTimedHeader() + "exportToFile::. [INFO] Exporting done, new museum generated!"

	def visualizeMuseum(self):
		"""
			Gestion of the museum's map generation & visualisation
			NOTE : you need pygame to run this !
		"""
		print logger.getTimedHeader() + "visualizeMuseum::. [INFO] Trying to launch visualisation of the map of the museum"
		try:
			print logger.getTimedHeader() + "visualizeMuseum::. [INFO] Visualisation loaded, you can close it by closing the window"
			visualize(self.memoMaze, self.writeDirectory)
		except ImportError:
			print logger.getTimedHeader() + "visualizeMuseum::. [ERROR] Visualisation failed, you need to have pygame installed to visualise the map!"

	def generateWikipediaContent(self):
		"""
			Generate content using wikipedia API and manifest files in each folder
			NOTE : this functionnality use the wikipedia module integrated in the museum directory
		"""
		print logger.getTimedHeader() + "generateWikipediaContent::. [INFO] Begin generating content using wikipedia API"
		try:
			import lib.wikipedia as wikipedia
			print logger.getTimedHeader() + "generateWikipediaContent ::. [INFO] Wikipedia Module loaded successfully"
		except ImportError:
			print logger.getTimedHeader() + "generateWikipediaContent ::. [ERROR] Wikipedia Module failed to load, exiting"
			exit(0)

		useProxy = config.ConfigSectionMap("network")['useproxy']
		if useProxy == '1' :
			print logger.getTimedHeader() + "generateWikipediaContent::. [WARNING] Proxy mode is enabled"
			
			hostname = config.ConfigSectionMap("network")['hostname']
			port = config.ConfigSectionMap("network")['port']
			username = config.ConfigSectionMap("network")['username']
			password = config.ConfigSectionMap("network")['password']
			
			print logger.getTimedHeader() + "generateWikipediaContent::. [WARNING] Proxy data :\n\t* Hostname : " + hostname + "\n\t* Port : " + port + "\n\t* Username : " + username + "\n\t* Password : " + config.ConfigSectionMap("network")['password']
			
			#try to make request without proxy ( stupid user ! )
			print logger.getTimedHeader() + "generateWikipediaContent::. [INFO] Try to make url call without proxy ..."
			try:
				
				urllib.urlopen(
					"http://example.com",
					proxies={'http':'http://example.com:8080'}
				)
			except IOError:
				print logger.getTimedHeader() + "generateWikipediaContent::. [ERROR] Can't connect without proxy , use given parameters from config.ini ..."
				try:
					urllib.urlopen(
					"http://example.com",
					proxies = {"http":"http://" + username + ":" + password + "@" + hostname + ":" + port}
					)
					print logger.getTimedHeader() + "generateWikipediaContent::. [INFO] Success, given proxy's configuration is correct."
				except:
					print logger.getTimedHeader() + "generateWikipediaContent::. [CRITICAL] Can't connect with or without proxy , all .data files will be empty !!"
			else:
				print logger.getTimedHeader() + "generateWikipediaContent::. [WARNING] Set FORCEPROXYOFF mode because we can connect without proxy !"
				
				config.forceProxyOff = True

		
		for i in range (len(self.listPaintings)):
			#check if directory exist ....
			activeDirectory = self.textsPaintingsPath + self.listPaintings[i] + "/"

			if os.path.exists(activeDirectory):								#Directory exist, try to read files
				if os.path.exists(activeDirectory + "manifest.xml"):
					print logger.getTimedHeader() + "generateWikipediaContent ::. [INFO] Reading manifest.xml file in " + activeDirectory + "'"
					self.getWikipediaContent(activeDirectory,i)
				else:
					print logger.getTimedHeader() + "generateWikipediaContent ::. [WARNING] Can't open or find manifest.xml in '" + activeDirectory + "'"
					self.createDefaultTextFolder (activeDirectory, i)
					self.getWikipediaContent(activeDirectory,i)
			else:
				print logger.getTimedHeader() + "generateWikipediaContent ::. [WARNING] Directory '" + activeDirectory + "' doesn't exist.... "
				self.createDefaultTextFolder (activeDirectory, i)
				self.getWikipediaContent(activeDirectory,i)


	def createDefaultTextFolder(self, activeDirectory, index):
		"""
			Create defaut text directory in the given activeDirectory, for the index paintings folder
		"""
		print logger.getTimedHeader() + "createDefaultTextFolder ::. [INFO] Creating folder '"+ activeDirectory + "'and basic 'manifest.xml'"

		#Create dir if necessary
		if not(os.path.exists(activeDirectory)):		
			os.makedirs(activeDirectory)

		#Prepare contents of the defaultManifest.xml file
		files = ET.Element('files')
		pathCurrentTextureDir = self.paintingPath + self.listPaintings[index]+ "/"
		listTextures = os.listdir(pathCurrentTextureDir)
		for j in range(len(listTextures)) :
			textureFile = ET.Element('file')

			nameFile = listTextures[j].split(".")

			textureFile.set("index",str(index))
			#Set name of texture as default researchKey
			textureFile.set("nameTexture",nameFile[0])
			textureFile.set("extension",nameFile[1])
			textureFile.set("researchKey", nameFile[0])

			files.append(textureFile)

		xmlString = ET.tostring(files, method="xml", encoding='UTF-8')
		export = minidom.parseString(xmlString)
		export = export.toprettyxml(indent="\t")

		#Write to file
		f = open(activeDirectory+ "manifest.xml", 'w')
		f.write(export)
		f.close()

	def getWikipediaContent(self, activeDirectory, index):
		"""
			Get wikipedia Content using the searchKey from manifest.xml file
		"""
		import lib.wikipedia as wikipedia
		from lib.wikipedia import (PageError)

		print logger.getTimedHeader() + "getWikipediaContent ::. [INFO] Searching for information from wikipedia using manifest in '" + activeDirectory + "'"
		tree = ET.parse(activeDirectory + "manifest.xml")				##Default params
		root = tree.getroot()
		allFiles = root.findall('file')

		#Foreach entry in manifest, get the researchKey and make call to wikipedia for content, then create associated file
		for i in range(len(allFiles)):
			currentFile = allFiles[i]
			index = int(currentFile.get("index"))
			filename = currentFile.get("nameTexture")
			researchKey = currentFile.get("researchKey")
			extension = currentFile.get("extension")

			wikiSummary = "" 
			print logger.getTimedHeader() + "getWikipediaContent ::. [INFO] Get content from wikipedia using keywork '" + researchKey + "' for the file '" + filename + "." + extension + "'" 
			try:
				wikiData = wikipedia.page(researchKey)
				wikiSummary = wikiData.summary
			except:
				print logger.getTimedHeader() + "generateWikipediaContent ::. [ERROR] Wikipedia Module can't find any result that match keywork '" + researchKey +"', fill file with default content" 
				wikiSummary = "Sorry, no result have been found on wikipedia for this painting"

			#Write to file
			print logger.getTimedHeader() + "getWikipediaContent ::. [INFO] Writing file'" + activeDirectory+ filename + ".data" + "' in the directory '" + activeDirectory + "'" 
			f = open(activeDirectory+ filename + ".data", 'w')
			f.write(wikiSummary.encode('UTF-8'))
			f.close()


if __name__ == "__main__":
	asciiDesc = "#####################################################\n###################MUSEUM GENERATOR##################\n#####################################################\n\n"
	usage = "Usage : python generator.py -v param -n 'nameHere'\n\n-v Y/N - Permit visualisation of the output using pygame\n\n-n 'nameHere' - Permit to give a name to your generated file, if not explicitly put it override the default museum\n\n-c Y/N - Generate Content using Wikipedia API\n\n NOTE: you must have a pair number of parameters or the script will stop"

	if ( len(argv) <= 1):
		print asciiDesc + usage
	else:
		launchParameters = argv
		launchParameters.pop(0) 	#remove name of the script
		nbOptions = len(launchParameters)

		index = 0
		listCommands = {}
		for x in range(0,nbOptions,2):
			if (x+1 < nbOptions):
				listCommands[launchParameters[x]] = launchParameters[x+1]
			else :
				print usage
				exit(0)

		#Generating or reading configFile
		print logger.getTimedHeader() + "__main__::. [INFO] Accessing to configFile"

		print logger.getTimedHeader() + "__main__::. [INFO] Initializing :: Parsing parameters :: " + str(listCommands)

		#DEFAULT parameters
		nameMuseum = "defaultMuseum"

		#name generated museum 
		if "-n" in listCommands :
			nameMuseum = listCommands["-n"]
			if nameMuseum == "defaultMuseum":																	#same name that the default
				print logger.getTimedHeader() + "__main__::. [INFO] NameMuseum :: Waiting for user input..."
				if useTkInter :
					top = Tkinter.Tk()
					top.withdraw()
					result = tkMessageBox.askquestion("Overwrite", "Your are about to overwrite the default xml configuration, continue?", icon='warning')
					top.destroy()
					if result == 'no':
						print "aborting...."
						exit(0)
				else :
					print "Your are about to overwrite the default xml configuration, continue? ( Y/N)"
					answer = raw_input("Continuer : ") 
					if answer != "Y":
						print "aborting...."
						exit(0)

			elif os.path.exists("datas/generated/" + nameMuseum):												#file already exist
				print logger.getTimedHeader() + "__main__::. [INFO] NameMuseum :: Waiting for user input..."
				if useTkInter :
					top = Tkinter.Tk()
					top.withdraw()
					result = tkMessageBox.askquestion("Overwrite", "There is already a museum with the given name, do you want to replace it?", icon='warning')
					top.destroy()
					if result == 'no':
						print "aborting...."
						exit(0)
				
				else:
					print "There is already a museum with the given name, do you want to replace it?"
					answer = raw_input("Remplacer (Y/N) : ") 
					if answer != "Y":
						print "aborting...."
						exit(0)
		else :
			print logger.getTimedHeader() + "__main__::. [INFO] NameMuseum :: Waiting for user input..."
			if useTkInter :
				top = Tkinter.Tk()
				top.withdraw()
				result = tkMessageBox.askquestion("Overwrite", "Your are about to overwrite the default xml configuration, continue? ( Y/N)", icon='warning')
				top.destroy()
				if result == 'no':
					print "aborting...."
					exit(0)
			else:
				print "Your are about to overwrite the default xml configuration, continue? ( Y/N)"
				answer = raw_input("Continuer : ") 
				if answer != "Y":
					print "aborting...."
					exit(0)

		print logger.getTimedHeader() + "__main__::. [INFO] Start museum generation"
		m = Generator(nameMuseum)

		#Generate view !
		if "-v" in listCommands :
			if listCommands["-v"] == 'Y':
				m.visualizeMuseum()

		#Generate content from wikipedia
		if "-c" in listCommands :
			if listCommands["-c"] == 'Y':
				m.generateWikipediaContent()







