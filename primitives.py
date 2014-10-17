#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------
#
#
#------------------------------------------------

import pyglet
from pyglet.gl import *

import os
import pprint
import sys

import random

textures = {}
default_texture = None
gap_asso = {}

def set_gap_association(asso):
	global gap_asso

	gap_asso = asso

def loading_textures():
	global textures, default_texture

	def walk(list_, datas, texture):
		#generate recursively tree structure
		if len(list_)>2:
			if not list_[0] in datas:
				datas[list_[0]]={}
			walk(list_[1:], datas[list_[0]], texture)
		else:
			if not list_[0] in datas:
				datas[list_[0]]={}
			datas[list_[0]][list_[-1]]=texture
			return texture


	list_of_textures = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(os.sep.join(["datas","textures"]))) for f in fn]

	for e in list_of_textures:

		try:
			image = pyglet.image.load(e)
		except pyglet.image.codecs.dds.DDSException:
			print '"%s" is not a valid image file' % e
			continue
		texture = image.get_texture()
		walk(e.split(os.sep)[2:], textures, image.get_texture())

	default_texture = textures["wall"]["wall1.jpg"]

	print "finish loading textures"
	#pprint.pprint(textures)
	return textures


def draw_plane(texture=default_texture ,color = (1,0,0), type_texturing="texture", scale_uv=(1,1)):

	if type_texturing != "texture":
		glDisable(GL_TEXTURE_2D)
		glBegin(GL_QUADS)
		glColor3f(*color)
		glVertex3f(  1.0,  1.0, 0.0 )
		glVertex3f( -1.0,  1.0, 0.0 )
		glVertex3f( -1.0, -1.0, 0.0 )
		glVertex3f(  1.0, -1.0, 0.0 )
		glEnd()
	else:
		glEnable(GL_TEXTURE_2D)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
		glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
		glBindTexture(texture.target, texture.id)
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3f(  -1.0,  -1.0, 0.0 )
		glTexCoord2f(1.0*scale_uv[0], 0.0)
		glVertex3f(   1.0,  -1.0, 0.0 )
		glTexCoord2f(1.0*scale_uv[0], 1.0*scale_uv[1])
		glVertex3f(   1.0,   1.0, 0.0 )
		glTexCoord2f(0.0, 1.0*scale_uv[1])
		glVertex3f(  -1.0,   1.0, 0.0 )
		glEnd()

def draw_cube(textures_=[default_texture]*6, colors= [[1,0,0]]*6, type_texturing="texture", scale_uv=(1,1)):

	#avoid trouble with colors

	#tests if all colors are present, whereas adds some number of default color to array
	colors.extend([[1,0,0]]*(6-len(colors)))
	textures_.extend([default_texture]*(6-len(textures_)))

	#draw front face
	glPushMatrix()
	glTranslatef(0,0,1)
	draw_plane(color=colors[0], texture=textures_[0], type_texturing=type_texturing, scale_uv=scale_uv)
	glPopMatrix()

	#draw back face
	glPushMatrix()
	glTranslatef(0,0,-1)
	draw_plane(color=colors[1], texture=textures_[1], type_texturing=type_texturing, scale_uv=scale_uv)
	glPopMatrix()

	#draw left face
	glPushMatrix()
	glTranslatef(1,0,0)
	glRotatef(90, 0,1,0)
	draw_plane(color=colors[2], texture=textures_[2], type_texturing=type_texturing, scale_uv=scale_uv)
	glPopMatrix()

	#draw right face
	glPushMatrix()
	glTranslatef(-1,0,0)
	glRotatef(90, 0,1,0)
	draw_plane(color=colors[3], texture=textures_[3], type_texturing=type_texturing, scale_uv=scale_uv)
	glPopMatrix()

	#draw bottom face
	glPushMatrix()
	glTranslatef(0,-1,0)
	glRotatef(90, 1,0,0)
	draw_plane(color=colors[4], texture=textures_[4], type_texturing=type_texturing, scale_uv=scale_uv)
	glPopMatrix()

	#draw top face
	glPushMatrix()
	glTranslatef(0,1,0)
	glRotatef(90, 1,0,0)
	draw_plane(color=colors[5], texture=textures_[5], type_texturing=type_texturing, scale_uv=scale_uv)
	glPopMatrix()


def draw_wall(gap="wall", dimensions=(10,11,0.1), textures_=[default_texture]*6, colors= [[1,0,0]]*6, type_texturing="texture", pediment=False, paintings=[]):
	#A wall involve two flattened cube separe by a gap in the middle

	#draw paintings
	if gap == "wall":

		def drange(start, stop, step):
			r = start
			while r < stop:
				yield r
				r += step

		n = len(paintings)
		begin = -dimensions[0]/2.0 + dimensions[0]/float(n+1)
		end   = -dimensions[0]/2.0 + (n+1)*dimensions[0]/float(n+1)
		step  = dimensions[0]/float(n+1)

		k=0
		for x in drange(begin, end, step):
			glPushMatrix()
			glTranslatef(2*x,dimensions[1]/2.0,0.2)
			draw_painting(paintings[k])
			glPopMatrix() 
			k+=1

		# sys.exit(0)


	gap = gap_asso[gap]

	if gap<=0:
		gap = 0

	if gap >= dimensions[0]:
		return

	#print dimensions

	l = (dimensions[0]-gap)/2.0
	x1 = -gap/1.0 - l
	x2 = -x1

	#draw first doorpost
	glPushMatrix()
	glTranslatef(x1, 1, 0)
	glScalef(l, dimensions[1]-1, dimensions[2])
	draw_cube(textures_=[default_texture]*6, colors= [[1,0,0]]*6, type_texturing="texture", scale_uv=(dimensions[0]/(2*l), dimensions[1]))
	glPopMatrix()

	#draw second doorpost
	glPushMatrix()
	glTranslatef(x2, 1, 0)
	glScalef(l, dimensions[1]-1, dimensions[2])
	draw_cube(textures_=[default_texture]*6, colors= [[1,0,0]]*6, type_texturing="texture", scale_uv=(dimensions[0]/(2*l), dimensions[1]))
	glPopMatrix()

	#draw pediment
	if pediment and gap:
		h = dimensions[1]/3.0
		y = 2*h
		x3 = 0

		glPushMatrix()
		glTranslatef(x3, y+1, 0)
		glScalef(gap, h-1, dimensions[2])
		draw_cube(textures_=[default_texture]*6, colors= [[1,0,0]]*6, type_texturing="texture", scale_uv=(gap/2.0, h))
		glPopMatrix()




def draw_room(gap=[0]*4, dimensions=[[10,11,0.1]]*4, textures_=[[default_texture]*6]*4, colors= [[[1,0,0]]*6]*4, type_texturing=["texture"]*4, pediment=[False]*4, paintings=[], signalisation=-1):
	
	# pprint.pprint(paintings)

	#draw northern wall
	dim = dimensions[0]
	glPushMatrix()
	glTranslatef(0,0,-dim[0]-dim[2]/2.0)
	draw_wall(gap=gap[0], dimensions=dim, textures_=textures_[0], colors=colors[0], type_texturing=type_texturing[0], pediment=pediment[0], paintings=paintings[0])
	glPopMatrix()

	#draw southern wall
	dim = dimensions[1]
	glPushMatrix()
	glTranslatef(0,0,dim[0]+dim[2]/2.0)
	glRotatef(180,0,1,0)
	draw_wall(gap=gap[1], dimensions=dim, textures_=textures_[1], colors=colors[1], type_texturing=type_texturing[1], pediment=pediment[1], paintings=paintings[1])
	glPopMatrix()

	#draw eastern wall
	dim = dimensions[2]
	glPushMatrix()
	glTranslatef(-dim[0]-dim[2]/2.0,0,0)
	glRotatef(90, 0, 1, 0)
	draw_wall(gap=gap[2], dimensions=dim, textures_=textures_[2], colors=colors[2], type_texturing=type_texturing[2], pediment=pediment[2], paintings=paintings[2])
	glPopMatrix()

	#draw western wall
	dim = dimensions[3]
	glPushMatrix()
	glTranslatef(dim[0]+dim[2]/2.0,0,0)
	glRotatef(-90, 0, 1, 0)
	draw_wall(gap=gap[3], dimensions=dim, textures_=textures_[3], colors=colors[3], type_texturing=type_texturing[3], pediment=pediment[3], paintings=paintings[3])
	glPopMatrix()

	#draw signalisation 
	if (signalisation != -1):		#Don't draw anything
		if signalisation == -2 :	#Begin
			glPushMatrix()
			glTranslatef(0,-0.95,0);
			#Rotate to put it on the ground
			glRotatef(90, 1,0,0)
			draw_plane(texture = textures["signalisation"]["home.png"])
			glPopMatrix()

		elif signalisation == -3 : 	#end
			glPushMatrix()
			glTranslatef(0,-0.95,0);
			#Rotate to put it on the ground
			glRotatef(90, 1,0,0)
			draw_plane(texture = textures["signalisation"]["door.png"])
			glPopMatrix()
		else :
			glPushMatrix()
			glTranslatef(0,-0.95,0);
			glRotatef(signalisation, 0, 1, 0)
			#Rotate to put it on the ground
			glRotatef(90, 1,0,0)
			draw_plane(texture = textures["signalisation"]["arrow.png"])
			glPopMatrix()

def draw_painting(texture):

	glPushMatrix()
	glScalef(1,1,0.05)
	draw_cube(textures_=[texture], colors= [[1,0,0]]*6, type_texturing="texture", scale_uv=(1,1))
	glPopMatrix()