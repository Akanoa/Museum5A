#! /usr/bin/python

import pyglet
from pyglet.gl import *

from primitives import loading_textures

from museum import Museum

import camera

myMuseum = None 
myCamera = None
window   = None
textures = {}

try:
	config = Config(sample_buffer=1, samples=4, \
		  depth_size=16, double_buffer=True)
	window = pyglet.window.Window(resizable=True, config=config)
	# window.set_exclusive_mouse(True)
except:
	window = pyglet.window.Window(resizable=True)
	# window.set_exclusive_mouse(True)

def setup():
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_TEXTURE_2D)
	glAlphaFunc(GL_GREATER,0.4)
	glEnable(GL_ALPHA_TEST)

def init():
	global myMuseum, myCamera, textures
	textures = loading_textures()
	setup()
	myCamera = camera.FirstPersonCamera(window, position=(0,0,-5), mouse_sensitivity=1)
	myMuseum = Museum(textures, "generatedMuseum.xml")
	myMuseum.init()

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
	myMuseum.draw()


	return pyglet.event.EVENT_HANDLED
	
def update(dt):
	global horloge

	#horloge = horloge + dt
	myCamera.update(dt)


if __name__ == '__main__' : 
	print "Hello World"
	init()
	# # La fonction update sera appelee toutes les 30eme de seconde
	pyglet.clock.schedule_interval(update, 1.0/30.0)

	pyglet.app.run()


