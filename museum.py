#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------
#
#
#------------------------------------------------

import xml.etree.ElementTree as ET
import os
import random
import struct

import pyglet
from pyglet.gl import *

from primitives import draw_cube, draw_plane

class Museum:

	'''
	create a new museum by using config dict
	'''
	def __init__(self, textures, config="museum.xml"):
		self.default_config = ET.fromstring(file(config).read())
		self.config = {}
		self.textures = textures

	def init(self):
		self.__generate_room_config()

	'''
	use default and user specified config to generate correct configs to rooms
	all parameters can be redefined:
		- height
		- length
		- width
		- wall_texture
		- floor_texture
		- ground_texture
		- nb_paintings
	path to parameters in config dict
	'''
	def __override_default(self, room_id, args):
		"""
		generates given xml tree if it isn't exist 
		"""
		saved = None
		default = self.default_config.findall('./default/'+args)
		path = "./rooms/room[@id='"+str(room_id)+"']"+args
		try:
			custom_root = self.default_config.findall("./rooms/room[@id='"+str(room_id)+"']")[0]
			custom = self.default_config.findall(path)
		except:
			return default[0]
		if custom != []:
			saved = custom[0]
		else:
			saved = default[0]

		return saved

	def jpeg_res(self, filename):
		""""This function prints the resolution
		of the jpeg image file passed into it"""

		# open image for reading in binary mode
		width = 0
		height = 0
		with open(filename,'rb') as jpeg:
			jpeg.read(2)
			b = jpeg.read(1)
			try:
				while (b and ord(b) != 0xDA):
					while (ord(b) != 0xFF): b = jpeg.read(1)
					while (ord(b) == 0xFF): b = jpeg.read(1)
					if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
						jpeg.read(3)
						h, w = struct.unpack(">HH", jpeg.read(4))
						break
					else:
						jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
					b = jpeg.read(1)
				width = int(w)
				height = int(h)
			except struct.error:
				pass
			except ValueError:
				pass

			return (width, height)

	def draw(self):
		pass

	def __generate_room_config(self):
		nb_rooms = int(self.default_config.findall('./default/dimensions')[0].get("nb"))
		width    = int(self.default_config.findall('./default/dimensions')[0].get("width"))
		length   = int(self.default_config.findall('./default/dimensions')[0].get("length"))
		height   = int(self.default_config.findall('./default/dimensions')[0].get("height"))

		#set default config
		self.config["default"] = {}
		#set dimensions
		self.config["default"]["dimensions"]=(width, length, height)

		#set texture
		self.config["default"]["textures"]={}
		#	set ground textures
		self.config["default"]["textures"]["ground"]  = self.default_config.findall("./default/textures/texture[@type='ground']")[0].get("path")
		#	set floor textures
		self.config["default"]["textures"]["ceiling"] = self.default_config.findall("./default/textures/texture[@type='ceiling']")[0].get("path")



		gap_association = {
			"void"   : int(self.default_config.findall("./default/doors_conf/door[@type='void']")[0].get("size")),
			"normal" : int(self.default_config.findall("./default/doors_conf/door[@type='normal']")[0].get("size")),
			"big"    : int(self.default_config.findall("./default/doors_conf/door[@type='big']")[0].get("size")),
			"wall"   : int(self.default_config.findall("./default/doors_conf/door[@type='wall']")[0].get("size"))
		}


		for room_id in range(nb_rooms):
			try:
				print "configuring rooms "+str(room_id)
				#set room
				self.config[room_id] = {"doors":{}}
				#set northern wall
				self.config[room_id]["doors"]=[]
				door = self.__override_default(room_id, "/doors/door[@direction='up']")
				self.config[room_id]["doors"].append({"gap":gap_association[door.get("type")]})
				#set southern wall
				door = self.__override_default(room_id, "/doors/door[@direction='down']")
				self.config[room_id]["doors"].append({"gap":gap_association[door.get("type")]})
				#\tset eastern wall
				door = self.__override_default(room_id, "/doors/door[@direction='left']")
				self.config[room_id]["doors"].append({"gap":gap_association[door.get("type")]})
				#set western wall
				door = self.__override_default(room_id, "/doors/door[@direction='right']")
				self.config[room_id]["doors"].append({"gap":gap_association[door.get("type")]})

				#set numbers of paintings
				nb = int(self.__override_default(room_id, "/paintings").get("nb"))
				absolute_path = "datas/textures/paintings/"+self.__override_default(room_id, "/paintings").get("path")
				list_paintings = os.listdir(absolute_path)
				self.config[room_id]["paintings"]=[]
				for i in range(nb):
					path = absolute_path+os.sep+random.choice(list_paintings)
					self.config[room_id]["paintings"].append([path, self.jpeg_res(path)])

				#set textures
				self.config[room_id]["textures"]={}
				#	set wall textures
				self.config[room_id]["textures"]["wall"] = self.__override_default(room_id, "/textures/texture[@type='walls']").get("path")
				#	set ground textures
				self.config[room_id]["textures"]["ground"] = self.__override_default(room_id, "/textures/texture[@type='ground']").get("path")
				#	set floor textures
				self.config[room_id]["textures"]["ceiling"] = self.__override_default(room_id, "/textures/texture[@type='ceiling']").get("path")

			except Exception,e:
				print e
				pass

		import pprint
		pprint.pprint(self.config)
