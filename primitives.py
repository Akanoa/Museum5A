#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------
#
#
#------------------------------------------------

import pyglet
from pyglet.gl import *

import os

textures = {}
default_texture = None

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



	list_of_textures = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser("datas/textures")) for f in fn]

	print len(list_of_textures)

	for e in list_of_textures:

		try:
			image = pyglet.image.load(e)
		except pyglet.image.codecs.dds.DDSException:
			print '"%s" is not a valid image file' % e
			continue
		texture = image.get_texture()
		walk(e.split(os.sep)[2:], textures, image.get_texture())

		glBindTexture(GL_TEXTURE_2D,texture.id)
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
		#glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

	default_texture = textures["wall"]["wall1.jpg"]

	print default_texture

	print "finish loading textures"

	return textures


def draw_plane(texture=default_texture ,color = (1,0,0), type_texturing="texture"):

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
		glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
		glBindTexture(texture.target, texture.id)
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3f(  -1.0,  -1.0, 0.0 )
		glTexCoord2f(1.0, 0.0)
		glVertex3f(   1.0,  -1.0, 0.0 )
		glTexCoord2f(1.0, 1.0)
		glVertex3f(   1.0,   1.0, 0.0 )
		glTexCoord2f(0.0, 1.0)
		glVertex3f(  -1.0,   1.0, 0.0 )
		glEnd()

def draw_cube(textures_=[default_texture]*6, colors= [[1,0,0]]*6, type_texturing="texture"):

	#avoid trouble with colors

	#tests if all colors are present, whereas adds some number of default color to array
	colors.extend([[1,0,0]]*(6-len(colors)))
	textures_.extend([default_texture]*(6-len(textures_)))

	#draw front face
	glPushMatrix()
	glTranslatef(0,0,1)
	draw_plane(color=colors[0], texture=textures_[0], type_texturing=type_texturing)
	glPopMatrix()

	#draw back face
	glPushMatrix()
	glTranslatef(0,0,-1)
	draw_plane(color=colors[1], texture=textures_[1], type_texturing=type_texturing)
	glPopMatrix()

	#draw left face
	glPushMatrix()
	glTranslatef(1,0,0)
	glRotatef(90, 0,1,0)
	draw_plane(color=colors[2], texture=textures_[2], type_texturing=type_texturing)
	glPopMatrix()

	#draw right face
	glPushMatrix()
	glTranslatef(-1,0,0)
	glRotatef(90, 0,1,0)
	draw_plane(color=colors[3], texture=textures_[3], type_texturing=type_texturing)
	glPopMatrix()

	#draw bottom face
	glPushMatrix()
	glTranslatef(0,-1,0)
	glRotatef(90, 1,0,0)
	draw_plane(color=colors[4], texture=textures_[4], type_texturing=type_texturing)
	glPopMatrix()

	#draw top face
	glPushMatrix()
	glTranslatef(0,1,0)
	glRotatef(90, 1,0,0)
	draw_plane(color=colors[5], texture=textures_[5], type_texturing=type_texturing)
	glPopMatrix()
