from datetime import datetime

from view import *
from scene import *
from shapes import *
from colour import *
from camera import *
from material import *
from lighting import *
from lightbulb import *
from geom3 import Point3, Vector3, Ray3, unit


SHINY_RED = Material(Colour(0.7, 0.3, 0.2), Colour(0.4,0.4,0.4), 100)
SHINY_BLUE = Material(Colour(0.2, 0.3, 0.7), Colour(0.8,0.8,0.8), 200)
MATT_GREEN = Material(Colour(0.1, 0.7, 0.1), None, None)
REFLECTIVE = Material(None, None, None, 1.0)

#import psyco
#psyco.full()

start = datetime.now()

scene = Scene()

#light = FocusedLight(Colour(0.4, 0.4, 0.4),
#                     Point3(0.7, 1.0, -1),
#                     Vector3(-0.1,-0.3,1),
#                     50, scene)

LightBulb(Colour(0.8, 0.8, 0.8), Point3(0.55, 0.4, 0.8), 0.1, scene)
#LightBulb(Colour(0, 0.8, 0), Point3(1, 1, 0), 0.1, scene)
#LightBulb(Colour(0.8, 0, 0), Point3(1, 0.5, 0), 0.1, scene)
AmbientLight(Colour(0.1,0.1,0.1), scene)

Sphere(Point3(0.35,0.6,0.5), 0.25, SHINY_BLUE, scene)
Sphere(Point3(0.75,0.2,0.6), 0.15, SHINY_RED, scene)
Plane(Point3(0.5,0.5,2), Vector3(0,0,-1), REFLECTIVE, scene)

view = View(Point3(0, 0, -1.5), # eye's location
            Vector3(0, 0, 1),    # view direction
            Vector3(0, 1, 0),    # up vector
            45,                  # hfov
            200,                 # height
            200,                 # width
            1)                   # aa level

camera = Camera(view, scene)

img = camera.take_photo()
img.save('image.bmp')    # Display image in default image-viewer application
print "Rendering time:", datetime.now() - start
