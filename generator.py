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
		self.listTexGround= os.listdir(self.texturesGroundPath)

		self.defaultTypeDoors = ["big","normal","void"]

		self.prepareDefaultParameters()
		self.generateNewMuseum()
		self.exportToFile(config)

	def prepareDefaultParameters(self):
		'''
		Write defaut parameters on top of the tree
		'''
		tree = ET.parse("museum.xml")					##Default params
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

		print "Number of row : " + str(rowsAsked)
		print "Number of columns : " + str(colsAsked)
		print "Minimum size asked for the path: " + str(searchedPath)

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
			return 10			#none

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

		print "Exporting XML Tree to file : " + fileName + " in directory :" + fileDirectory
		
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
		rough_string = ET.tostring(self.root, method="xml", encoding='UTF-8' )
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

		#Write to file
		f = open(fileDirectory+ fileName, 'w')
		f.write(reparsed)
		f.close()
		print "Exporting done, new museum generated!\n\n"

	def visualizeMuseum(self):
		"""
			Gestion of the museum's map generation & visualisation
			NOTE : you need pygame to run this !
		"""
		print "\n#######VISUALISATION########\nTrying to launch visualisation of the map of the museum "
		try:
			print "Visualisation loaded, you can close it by closing the window"
			visualize(self.memoMaze, self.writeDirectory)
		except ImportError:
			print "<!> ERROR : Visualisation failed, you need to have pygame installed to visualise the map!"

if __name__ == "__main__":
	usage = "Usage : python generator.py -v param -n 'nameHere'\n\n-v Y/N - Permit visualisation of the output using pygame\n\n-n 'nameHere' - Permit to give a name to your generated file, if not explicitly put it override the default museum\n\n\n NOTE: you must have a pair number of parameters or the script will stop"

	if ( len(argv) <= 1):
		print usage
	else:
		launchParameters = argv
		launchParameters.pop(0) 	#remove name of the script
		nbOptions = len(launchParameters)

		index = 0
		listCommands = {}
		for x in range(0,nbOptions,2):
			if (x+1 < nbOptions):
				listCommands[launchParameters[x]] =launchParameters[x+1]
			else :
				print usage
				exit(0)

		#DEFAULT parameters
		nameMuseum = "defaultMuseum"

		if "-n" in listCommands :
			nameMuseum = listCommands["-n"]
			if nameMuseum == "defaultMuseum":
				print "Vous etes sur le point de remplacer la configuration xml de base, etes vous sur? ( Y/N)"
				answer = raw_input("Continuer : ") 
				if answer != "Y":
					print "aborting...."
					exit(0)
			elif os.path.exists("datas/generated/" + nameMuseum):
				print "Un musee portant ce nom existe deja, voulez-vous le remplacer?"
				answer = raw_input("Remplacer (Y/N) : ") 
				if answer != "Y":
					print "aborting...."
					exit(0)
		else :
			print "Vous etes sur le point de remplacer la configuration xml de base, etes vous sur? ( Y/N)"
			answer = raw_input("Continuer : ") 
			if answer != "Y":
				print "aborting...."
				exit(0)

		m = Generator(nameMuseum)

		if "-v" in listCommands :
			if listCommands["-v"] == 'Y':
				m.visualizeMuseum()


