#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------
#
#
#------------------------------------------------

import pyglet
from pyglet.gl import *


def draw_plane(color = (1,0,0)):
	glBegin(GL_QUADS)
	glColor3f(*color)
	glVertex3f(  1.0,  1.0, 0.0 )
	glVertex3f( -1.0,  1.0, 0.0 )
	glVertex3f( -1.0, -1.0, 0.0 )
	glVertex3f(  1.0, -1.0, 0.0 )
	glEnd()

def draw_cube(colors= [[1,0,0]]*6):

	#avoid trouble with colors

	#tests if all colors are present, whereas adds some number of default color to array
	colors.extend([[1,0,0]]*(6-len(colors)))

	#draw front face
	glPushMatrix()
	glTranslatef(0,0,1)
	draw_plane(colors[0])
	glPopMatrix()

	#draw back face
	glPushMatrix()
	glTranslatef(0,0,-1)
	draw_plane(colors[1])
	glPopMatrix()

	#draw left face
	glPushMatrix()
	glTranslatef(1,0,0)
	glRotatef(90, 0,1,0)
	draw_plane(colors[2])
	glPopMatrix()

	#draw right face
	glPushMatrix()
	glTranslatef(-1,0,0)
	glRotatef(90, 0,1,0)
	draw_plane(colors[3])
	glPopMatrix()

	#draw bottom face
	glPushMatrix()
	glTranslatef(0,-1,0)
	glRotatef(90, 1,0,0)
	draw_plane(colors[4])
	glPopMatrix()

	#draw top face
	glPushMatrix()
	glTranslatef(0,1,0)
	glRotatef(90, 1,0,0)
	draw_plane(colors[5])
	glPopMatrix()
