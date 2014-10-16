#Generator.py
#Date : 15/10/2014

import xml.etree.ElementTree as ET
import random
import os, os.path
import xml.dom.minidom as minidom
import imp
from math import sqrt

from maze import *
from mazeView import *

class Generator:
	'''
	generation of xml file
	'''
	def __init__(self, config="generatedMuseum.xml"):
		self.root = ET.Element('xml')

		self.defautPaintingPath = "datas/textures/paintings/"
		self.listPaintings = os.listdir(self.defautPaintingPath)

		self.defaultTypeDoors = ["big","normal","void"]

		

	def prepareDefaultParameters(self):
		'''
		Write defaut parameters on top of the tree
		'''
		tree = ET.parse("museum.xml")
		doc = tree.getroot()
		defaultParams = doc.find('default')
		dimensions = defaultParams.find('dimensions')
		self.defaultNb = int (sqrt(int(dimensions.get("nb"))))
		print str(self.defaultNb)
		self.root.append(defaultParams)


	def generateNewMuseum(self):
		'''
			Generate a new random museum
		'''

		#Generate a new maze
		maze = Maze(self.defaultNb,self.defaultNb)
		self.memoMaze = maze
		cellList = maze.maze

		#solution path, usefull for signalisation  // TODO
		maze.solve_maze()
		path = maze.solutionpath
		print path
		print path[1]

		prepareWall = self.generateWallProperty(maze);
	
		rooms = ET.Element('rooms')

		# fetch row
		print "Number of row :" + str(maze.rows)
		print "Number of columns :" + str(maze.cols)
		for i in range(maze.rows):
			#fetch columns
			for j in range(maze.cols):
				#listWall = self.createWallProperty(maze, i,j)
				listWall = prepareWall[i][j]

				#Select a set of paintings, get path to textures directory
				paintingSelected = self.choosePaintingSet()

				#calculate new id
				actualID = i * maze.rows + j

				#Signalisation
				signalisation = self.obtainSignalisation(path,i,j)

				#generate xml
				room = self.generateRoomXml(actualID, listWall, paintingSelected, signalisation)

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

	def chooseDoorType(self):
		'''
			return a door type choosen randomy
		'''
		resultRand = random.randint(0, len(self.defaultTypeDoors)-1)
		doorChoosen = self.defaultTypeDoors[resultRand]
		return doorChoosen

	def generateRoomXml(self,id,listWall, paintingSelected, signal):
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
		paintings = ET.Element('paintings')

		counter = len([name for name in os.listdir(self.defautPaintingPath + paintingSelected) if os.path.isfile(os.path.join(self.defautPaintingPath + paintingSelected, name))])

		paintings.set("nb",str(counter))
		paintings.set("path",paintingSelected)
		room.append(paintings)

		###########Signalisation############
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

	def exportToFile(self, nameFile = "generatedMuseum.xml"):
		print "Exporting XML Tree to file : " + nameFile
		rough_string = ET.tostring(self.root, method="xml", encoding='UTF-8' )
		reparsed = minidom.parseString(rough_string)
		reparsed = reparsed.toprettyxml(indent="\t")
		f = open(nameFile, 'w')
		f.write(reparsed)
		f.close()
		print "Exporting done, new museum generated!"
	def visualizeMuseum(self):
		print "Trying to launch visualisation of the map of the museum "
		try:
			print "Visualisation loaded, you can close it by closing the window"
			visualize(self.memoMaze)
			found = True
		except ImportError:
			print "Visualisation failed, you need to have pygame installed to visualise the map!"
			found = False

if __name__ == "__main__":
	if ( len(argv) <= 1):
		print "Usage : python generator.py -v true\n\n-v O/N - Permit visualisation of the output using pygame"
	else:
		m = Generator()
		m.prepareDefaultParameters()
		m.generateNewMuseum()
		m.exportToFile()
		if (argv[1] == "-v") & (argv[2] == 'O'):
			m.visualizeMuseum()
