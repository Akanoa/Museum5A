
from lxml import etree
import random
import os, os.path



class Generator:

	'''
	generation of xml file
	'''
	def __init__(self, config="museum.xml"):
		self.root = etree.Element('xml')

		self.defaultHeight = 3;
		self.defaultWidth = 10;
		self.defaultLength = 10;
		self.defaultNb = 5;

		self.defautPaintingPath = "datas/textures/paintings/"
		self.listPaintings = ["1/","2/","3/","4/","5/"]

		self.defaultTypeDoors = ["big","normal","void"]
		
		# root.append(etree.Element('child'))
		# child = etree.Element('child')
		# child.set("test","Coucou")
		# child.text = 'some text'
		# root.append(child)
		
		
	'''
	Write defaut parameters on top of the tree
	'''
	def prepareDefaultParameters(self):
		default = etree.Element('default')

		dimensions = etree.Element('dimensions')
		dimensions.set("height",str(self.defaultHeight))
		dimensions.set("width",str(self.defaultWidth))
		dimensions.set("length",str(self.defaultLength))
		dimensions.set("nb",str(self.defaultNb))
		default.append(dimensions)

		paintings = etree.Element('paintings')
		paintings.set("nb","4")
		paintings.set("path","datas/textures/paintings/1/")
		default.append(paintings)

		textures = etree.Element('textures')
		texture = etree.Element('texture')
		texture.set("type","walls")
		texture.set("path","datas/textures/wall/wall1.jpg")
		textures.append(texture)
		texture.set("type","ground")
		texture.set("path","datas/textures/wall/floor1.jpg")
		texture = etree.Element('texture')
		texture.set("type","ceiling")
		texture.set("path","datas/textures/wall/ceiling1.jpg")
		textures.append(texture)

		default.append(textures)

		doors_conf = etree.Element('doors_conf')
		door = etree.Element('texture')
		door.set("type","big")
		door.set("size","4")
		doors_conf.append(door)
		door = etree.Element('door')
		door.set("type","normal")
		door.set("size","2")
		doors_conf.append(door)
		door = etree.Element('door')
		door.set("type","void")
		door.set("size","10")
		doors_conf.append(door)
		door = etree.Element('door')
		door.set("type","wall")
		door.set("size","0")
		doors_conf.append(door)

		default.append(doors_conf)

		doors = etree.Element('doors')
		door = etree.Element('door')
		door.set("direction","up")
		door.set("type","wall")
		doors.append(door)
		door = etree.Element('door')
		door.set("direction","down")
		door.set("type","wall")
		doors.append(door)
		door = etree.Element('door')
		door.set("direction","left")
		door.set("type","wall")
		doors.append(door)
		door = etree.Element('door')
		door.set("direction","big")
		door.set("type","right")
		doors.append(door)

		default.append(doors)

		self.root.append(default)


	'''
		Generate a new random museum
	'''
	def generateNewMuseum(self):
		rooms = etree.Element('rooms')

		#Starting generation of museum
		i = 0;
		oldChoice = "none"
		oldDoorType = "none"
		for i in range(self.defaultNb):
			#Determinate new direction and find from where we come
			fromDirection = self.getFromDirection(oldChoice)
			direction = self.selectRandomDirection(oldChoice, fromDirection)
			
			#Choose a paintings set for the room
			paintingSelected = self.choosePaintingSet()

			#Choose new type of door for the exit
			doorType = self.chooseDoorType()

			room = self.generateRoomXml(i,oldChoice,oldDoorType,direction,fromDirection,paintingSelected,doorType)
			rooms.append(room)

			oldDoorType = doorType
			oldChoice = direction

		#Generation ended
		self.root.append(rooms)

	def selectRandomDirection(self, restriction, fromDirection):
		'''

		'''
		redo = True;
		result = ""
		while(redo):
			redo = False
			result = random.choice('udlr')		#UP/Down/Left/right
			if ( (result == restriction) | (result == fromDirection)):
				redo = True

		return result

	def getFromDirection(self, choice):
		'''
			return the opposite direction for the direction given in parameters
		'''
		if (choice == 'r'):
			return 'l'
		elif (choice == 'l'):
			return 'r'
		elif (choice == 'u'):
			return 'd'
		elif (choice == 'd'):
			return 'u'
		else:
			return 'n'			#none

	def choosePaintingSet(self):
		'''
			Return path to paintings for the a room using random choice from the list 
			Remove the paintings from the original list to prevent duplication
		'''
		resultRand = random.randint(0, len(self.listPaintings)-1)
		paintingSet = self.listPaintings[resultRand]
		del self.listPaintings[resultRand]

		return (self.defautPaintingPath + paintingSet)

	def chooseDoorType(self):
		'''
			return a door type choosen randomy
		'''
		resultRand = random.randint(0, len(self.defaultTypeDoors)-1)
		doorChoosen = self.defaultTypeDoors[resultRand]
		return doorChoosen

	def generateRoomXml(self,id,oldChoice,oldDoorType,direction,fromDirection,paintingSelected,doorType):
		'''
			Generate XMl tree of a room using the given parameters
		'''
		room = etree.Element('room')
		room.set("id",str(id))

		############Doors part##############
		doors = etree.Element('doors')

		#From door
		door = etree.Element('door')
		door.set("direction",self.varToStr(fromDirection))
		door.set("type",oldDoorType)
		doors.append(door)

		#New door
		door = etree.Element('door')
		door.set("direction",self.varToStr(direction))
		door.set("type",doorType)
		doors.append(door)

		room.append(doors)

		###########Paintings Part###########
		paintings = etree.Element('paintings')

		counter = len([name for name in os.listdir(paintingSelected) if os.path.isfile(os.path.join(paintingSelected, name))])

		paintings.set("nb",str(counter))
		paintings.set("path",paintingSelected)

		room.append(paintings)

		return room

	def varToStr(self, value):

		if (value == 'u'):
			return "up"
		elif (value == 'd'):
			return "down"
		elif (value == 'r'):
			return "right"
		elif (value == 'l'):
			return "left"
		else:
			return "unknow"

	def exportToFile(self,nameFile = "generatedMuseum.xml"):
		s = etree.tostring(self.root, pretty_print=True, encoding='UTF-8' )
		f = open(nameFile, 'w')
		f.write(s)
		f.close()

if __name__ == "__main__":
	m = Generator()
	m.prepareDefaultParameters()
	m.generateNewMuseum()
	m.exportToFile()
