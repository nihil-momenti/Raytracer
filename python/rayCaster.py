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

import psyco
psyco.full()

SHINY_RED = Material(Colour(0.7, 0.3, 0.2), Colour(0.4,0.4,0.4), 100)
SHINY_BLUE = Material(Colour(0.2, 0.3, 0.7), Colour(0.8,0.8,0.8), 200)
MATT_GREEN = Material(Colour(0.1, 0.7, 0.1), None, None)
MATT_BLUE = Material(Colour(0.1, 0.1, 0.7), None, None)
MATT_RED = Material(Colour(0.7, 0.1, 0.1), None, None)
REFLECTIVE = Material(None, None, None, 1.0)

import psyco
psyco.full()

start = datetime.now()

scene = Scene()

#light = FocusedLight(Colour(0.4, 0.4, 0.4),
#                     Point3(0.7, 1.0, -1),
#                     Vector3(-0.1,-0.3,1),
#                     50, scene)

LightBulb(Colour(0.8, 0.8, 0.8), Point3(0.95, -0.2, 0.55), 0.01, scene)
#LightBulb(Colour(0, 0.8, 0), Point3(1, 1, 0), 0.1, scene)
#LightBulb(Colour(0.8, 0, 0), Point3(1, 0.5, 0), 0.1, scene)
AmbientLight(Colour(0.1,0.1,0.1), scene)

# Sphere(Point3(0.35,0.6,0.5), 0.25, SHINY_BLUE, scene)
# Sphere(Point3(0.75,0.2,0.6), 0.15, SHINY_RED, scene)
# plane1 = Plane(Point3(0.5,0.5,2), Vector3(0,0,-1), MATT_GREEN, scene)
# plane2 = Plane(Point3(0,0.5,2), Vector3(-1,0,0), MATT_BLUE, scene)
# plane3 = Plane(Point3(0.5,0,2), Vector3(0,1,0), MATT_RED, scene)
CSG([
  CSGPlane(Point3(0.5,0.5,2), Vector3(0,0,1)),
  CSGPlane(Point3(0,0.5,3), Vector3(1,0,0)),
  CSGPlane(Point3(1,0.5,3), Vector3(-1,0,0)),
  CSGPlane(Point3(0.5,0,3), Vector3(0,1,0)),
  CSGPlane(Point3(0.5,1,3), Vector3(0,-1,0)),
  CSGPlane(Point3(0.5,0.5,4), Vector3(0,0,-1))
  ],
  MATT_GREEN,
  scene)
Sphere(Point3(0,0,2), 0.1, SHINY_RED, scene)
Sphere(Point3(1,0,2), 0.1, SHINY_RED, scene)
Sphere(Point3(0,1,2), 0.1, SHINY_RED, scene)
Sphere(Point3(1,1,2), 0.1, SHINY_RED, scene)
Sphere(Point3(1,1,4), 0.1, SHINY_RED, scene)
Sphere(Point3(0,1,4), 0.1, SHINY_RED, scene)
Sphere(Point3(1,0,4), 0.1, SHINY_RED, scene)
Sphere(Point3(0,0,4), 0.1, SHINY_RED, scene)

view = View(Point3(-0.5, 0.5, -1), # eye's location
            Vector3(0, 0, 1),    # view direction
            Vector3(0, 1, 0),    # up vector
            45,                  # hfov
            256,                 # height
            256,                 # width
            1)                   # aa level

camera = Camera(view, scene)

img = camera.take_photo_new()
img.save('image.bmp')    # Display image in default image-viewer application
print "Rendering time:", datetime.now() - start
