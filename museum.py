#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------
#
#
#------------------------------------------------

import xml.etree.ElementTree as ET
import os, sys
import random
import struct
import traceback
import pprint

import pyglet
from pyglet.gl import *


from primitives import draw_cube, draw_plane, draw_wall, draw_room, draw_painting, set_gap_association

class Museum:

	'''
	create a new museum by using config dict
	'''
	def __init__(self, textures, config="museum.xml"):
		self.default_config = ET.fromstring(file(config).read())
		self.config = {}
		self.textures = textures

	def init(self):
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
		self.__generate_room_config()

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

	def draw(self):

		#draw rooms
		k=0
		for i in range(-30, 50, 20):

			for j in range(-30, 50, 20):
				glPushMatrix()
				glTranslatef(j, 0 ,i)
				draw_room(gap=self.config[k]["doors"], textures_=self.config[k]["textures"]["walls"]+[self.config[k]["textures"]["ground"], self.config[k]["textures"]["ceiling"]], dimensions=[[self.config[k]["dimensions"][e] for e in [0,2,3]]]*4, pediment=[False]*4, signalisation= self.config[k]["signalisation"], paintings=self.config[k]["paintings"] )
				glPopMatrix()
				k+=1

	def get_player_position(self):
		return self.config["default"]["player_position"]

	def __generate_room_config(self):
		nb_rooms = int(self.default_config.findall('./default/dimensions')[0].get("nb"))
		width    = int(self.default_config.findall('./default/dimensions')[0].get("width"))
		length   = int(self.default_config.findall('./default/dimensions')[0].get("length"))
		height   = int(self.default_config.findall('./default/dimensions')[0].get("height"))
		thick    = float(self.default_config.findall('./default/dimensions')[0].get("thick"))

		#set default config
		self.config["default"] = {}
		#set dimensions
		self.config["default"]["dimensions"]= (width, length, height, thick)

		#set texture
		self.config["default"]["textures"]= {}
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

		paint_asso = {
			"wall"  : 3,
			"big"   : 2,
			"normal": 2,
			"void"  : 0
		}

		set_gap_association(gap_association)

		signal_association ={
			"up"	:	180,
			"down"	:	0,		
			"right"	:	270,
			"left"	:	90,		#OK
			"begin"	:	-2,
			"end"	:	-3,
			"N/A"	:	-1,
		}

		room = int(self.default_config.findall("./rooms/room/signalisation[@direction='begin']/..")[0].get('id'))
		k=0
		loop = True
		for i in range(-30, 50, 20):
			if not loop:
				break
			for j in range(-30, 50, 20):
				if k==room:
					self.config["default"]["player_position"]=[-j,-2,-i]
					loop=False
					break
				k+=1

		for room_id in range(nb_rooms):
			try:
				#set room
				self.config[room_id] = {"doors":{}}
				#set northern wall
				self.config[room_id]["doors"] = []
				door = self.__override_default(room_id, "/doors/door[@direction='up']")
				self.config[room_id]["doors"].append(door.get("type"))
				#set southern wall
				door = self.__override_default(room_id, "/doors/door[@direction='down']")
				self.config[room_id]["doors"].append(door.get("type"))
				#\tset eastern wall
				door = self.__override_default(room_id, "/doors/door[@direction='left']")
				self.config[room_id]["doors"].append(door.get("type"))
				#set western wall
				door = self.__override_default(room_id, "/doors/door[@direction='right']")
				self.config[room_id]["doors"].append(door.get("type"))

				#signalisation
				signalisation = self.__override_default(room_id, "/signalisation").get("direction")
				self.config[room_id]["signalisation"] = signal_association[signalisation]

				#set numbers of paintings
				nb = int(self.__override_default(room_id, "paintings").get("nb"))
				absolute_path = os.sep.join(["datas","textures","paintings", ""])+self.__override_default(room_id, "/paintings").get("path")
				list_paintings_ = os.listdir(absolute_path)
				list_paintings = []
				for i in range(nb):
					path = absolute_path[-1]+os.sep+random.choice(list_paintings_)
					list_paintings.append(path)

				paintings = {0: [[], 3], 1: [[], 3], 2: [[], 3], 3: [[], 3]}
				for key in paintings.keys():
					paintings[key][1]=paint_asso[self.config[room_id]["doors"][key]]

				run = True
				potential = range(4)

				while run:
					for wall in potential:
						#if no paintings left
						if len(list_paintings)==0:
							run = False
							break
						if paintings[wall][1]==0:
							potential.pop(potential.index(wall))
							if len(potential)==0:
								run = False
								break
							continue
						chosen = list_paintings.pop(list_paintings.index(random.choice(list_paintings))).split(os.sep)
						paintings[wall][0].append(self.textures["paintings"][chosen[0]][chosen[1]])
						paintings[wall][1]-=1
						break

				self.config[room_id]["paintings"]=[paintings[key][0] for key in paintings.keys()]

				#set dimensions
				width    = int(self.__override_default(room_id, "dimensions").get("width"))
				length   = int(self.__override_default(room_id, "dimensions").get("length"))
				height   = int(self.__override_default(room_id, "dimensions").get("height"))
				thick    = float(self.__override_default(room_id, "dimensions").get("thick"))

				self.config[room_id]["dimensions"]=(width, length, height, thick)				

				#set textures
				self.config[room_id]["textures"]={}
				#	set wall textures
				self.config[room_id]["textures"]["walls"] = []
				#upper wall
				self.config[room_id]["textures"]["walls"].append(self.textures["wall"][self.__override_default(room_id, "/textures/walls/wall[@type='up']").get("path")])
				#down wall
				self.config[room_id]["textures"]["walls"].append(self.textures["wall"][self.__override_default(room_id, "/textures/walls/wall[@type='down']").get("path")])
				#left wall
				self.config[room_id]["textures"]["walls"].append(self.textures["wall"][self.__override_default(room_id, "/textures/walls/wall[@type='left']").get("path")])
				#right wall
				self.config[room_id]["textures"]["walls"].append(self.textures["wall"][self.__override_default(room_id, "/textures/walls/wall[@type='right']").get("path")])

				#	set ground textures
				self.config[room_id]["textures"]["ground"] = self.textures["ground"][self.__override_default(room_id, "/textures/texture[@type='ground']").get("path")]
				#	set floor textures
				self.config[room_id]["textures"]["ceiling"] = self.textures["ceiling"][self.__override_default(room_id, "/textures/texture[@type='ceiling']").get("path")]

			except Exception,e:
				traceback.print_exc()
				pass
