#! /usr/bin/python

import pyglet
from pyglet.gl import *

from museum import Museum

import math


import camera

import xml_tool

myMuseum = None 
myCamera = None
window   = None

try:
	config = Config(sample_buffer=1, samples=4, \
          depth_size=16, double_buffer=True)
	window = pyglet.window.Window(resizable=True, config=config)
	window.set_exclusive_mouse(True)
except:
	window = pyglet.window.Window(resizable=True)
	window.set_exclusive_mouse(True)

def setup():
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_TEXTURE_2D)
	glAlphaFunc(GL_GREATER,0.4)
	glEnable(GL_ALPHA_TEST)

def init():
	global myMuseum, myCamera
	setup()
	myCamera = camera.FirstPersonCamera(window, mouse_sensitivity=0.02)
	myMuseum = Museum("museum.xml")
	myMuseum.init()
	pass


@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70.0, width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
	global scene
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	myCamera.draw()
	#glClearColor(1.0,1.0,1.0,1.0)

	for i in range(3):
		glTranslatef(i*10, 0, 0)
		cube()


	return pyglet.event.EVENT_HANDLED

def cube():
	pyglet.gl.glColor4f(1.0,0,0,1.0)

	pyglet.graphics.draw_indexed(8, pyglet.gl.GL_LINES, [0, 1, 1, 2, 2, 3, 3, 0,
														4, 5, 5, 6, 6, 7, 7, 4,
														0, 4, 1, 5, 2, 6, 3, 7],
														('v3f', (-1, -1, 0,
														1, -1, 0,
														1, 1, 0,
														-1, 1, 0,
														-1, -1, -1,
														1, -1, -1,
														1, 1, -1,
														-1, 1, -1)))
	
def update(dt):
	global horloge

	#horloge = horloge + dt
	myCamera.update(dt)


if __name__ == '__main__' : 
	print "Hello World"
	init()
	# # La fonction update sera appelee toutes les 30eme de seconde
	pyglet.clock.schedule_interval(update, 1.0/12.0)

	pyglet.app.run()

	#print xml_tool.parse(file("museum.xml"))["xml"]["default"]["dimensions"]["@width"]


