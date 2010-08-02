from datetime import datetime

from view import *
from scene import *
from shapes import *
from colour import *
from camera import *
from material import *
from lighting import *
from geom3 import Point3, Vector3, Ray3, unit


SHINY_RED = Material(Colour(0.7, 0.3, 0.2), Colour(0.4,0.4,0.4), 100)
SHINY_BLUE = Material(Colour(0.2, 0.3, 0.7), Colour(0.8,0.8,0.8), 200)
MATT_GREEN = Material(Colour(0.1, 0.7, 0.1), None, None)

start = datetime.now()

light = DirectionalLight(0.8,              # Intensity
                         Vector3(1,1,1))  # Direction to light

ambientLight = AmbientLight(0.1)

lighting = [ambientLight, light]

scene = Scene([Sphere(Point3(0.35,0.6,0.5), 0.25, SHINY_BLUE),
         Sphere(Point3(0.75,0.2,0.6), 0.15, SHINY_RED),
         Plane(Point3(0.5,0.5,2), Vector3(0,0,1), MATT_GREEN)])

view = View(Point3(0.5, 0.5, -1), # eye's location
            Vector3(0, 0, 1),    # view direction
            Vector3(0, 1, 0),    # up vector
            90,                  # hfov
            1000,                 # height
            1000,                 # width
            2)                   # aa level

camera = Camera(view,
                scene,
                lighting)

img = camera.take_photo()
img.save('image.bmp')    # Display image in default image-viewer application
print "Rendering time:", datetime.now() - start
