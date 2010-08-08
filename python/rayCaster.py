from datetime import datetime

from csg import *
from view import *
from scene import *
from shapes import *
from colour import *
from camera import *
from material import *
from lighting import *
from lightbulb import *
from transforms import *
from geom3 import Point3, Vector3, Ray3, unit

SHINY_RED = Material(Colour(0.7, 0.3, 0.2), Colour(0.4,0.4,0.4), 100)
SHINY_BLUE = Material(Colour(0.2, 0.3, 0.7), Colour(0.8,0.8,0.8), 200)
REFLECTIVE_BLUE = Material(Colour(0.2, 0.3, 0.7), Colour(0.8,0.8,0.8), 200, 0.1)
MATT_GREEN = Material(Colour(0.1, 0.7, 0.1), None, None)
MATT_BLUE = Material(Colour(0.1, 0.1, 0.7), None, None)
MATT_RED = Material(Colour(0.7, 0.1, 0.1), None, None)
REFLECTIVE = Material(None, None, None, 1.0)

try:
  import psyco
  psyco.full()
except ImportError:
  print "Psyco not available"

start = datetime.now()

scene = Scene()

DirectionalLight(Colour(0.8,0.8,0.8), Vector3(-1,-1,-1))
# LightBulb(Colour(0.8, 0.8, 0.8), Point3(1, 0, 0), 0.05, scene)
# LightBulb(Colour(0.8, 0.8, 0.8), Point3(0, 0, -0.5), 0.05, scene)
AmbientLight(Colour(0.1,0.1,0.1), scene)

##Mirror
Translation(
  Rotation(
    Union([
      Intersection([
        Plane(Point3( 0  , 0  , 0   ), Vector3( 0, 0,-1)),
        Plane(Point3( 0  , 0  , 0.01), Vector3( 0, 0, 1)),
        Plane(Point3( 0.5, 0  , 0   ), Vector3( 1, 0, 0)),
        Plane(Point3(-0.5, 0  , 0   ), Vector3(-1, 0, 0)),
        Plane(Point3( 0  , 0.5, 0   ), Vector3( 0, 1, 0)),
        Plane(Point3( 0  ,-0.5, 0   ), Vector3( 0,-1, 0)),
        ],
        REFLECTIVE
      ),
      Intersection([
        Plane(Point3( 0   , 0   , 0  ), Vector3( 0, 0,-1)),
        Plane(Point3( 0   , 0   , 0.1), Vector3( 0, 0, 1)),
        Plane(Point3( 0.53, 0   , 0  ), Vector3( 1, 0, 0)),
        Plane(Point3(-0.53, 0   , 0  ), Vector3(-1, 0, 0)),
        Plane(Point3( 0   , 0.53, 0  ), Vector3( 0, 1, 0)),
        Plane(Point3( 0   ,-0.53, 0  ), Vector3( 0,-1, 0)),
        ],
        SHINY_RED
      ),
    ]),
    Vector3(-0.8,1,0), 40
  ),
  Vector3(0.4,0,0.8),
  None,
  scene
)

## Pedestal
Translation(
  Rotation(
    Union([
      Intersection([
        Plane(Point3( 0  , 0   , 0  ), Vector3( 0, 0,-1)),
        Plane(Point3( 0  , 0   , 0.1), Vector3( 0, 0, 1)),
        Union([
          Intersection([
            Plane(Point3( 0.05, 0   , 0  ), Vector3( 1, 0, 0)),
            Plane(Point3(-0.05, 0   , 0  ), Vector3(-1, 0, 0)),
            Plane(Point3( 0  , 0.2 , 0  ), Vector3( 0, 1, 0)),
            Plane(Point3( 0  , 0.1 , 0  ), Vector3( 0,-1, 0)),
          ]),
          Intersection([
            Plane(Point3( 0.15, 0   , 0  ), Vector3( 1, 0, 0)),
            Plane(Point3(-0.15, 0   , 0  ), Vector3(-1, 0, 0)),
            Plane(Point3( 0  , 0.1 , 0  ), Vector3( 0, 1, 0)),
            Plane(Point3( 0  , 0   , 0  ), Vector3( 0,-1, 0)),
          ]),
        ]),
      ], SHINY_RED),
      # Sphere(Point3(-0.025,0.15,0), 0.02, REFLECTIVE),
      ]),
    Vector3(0,1,0), 30
  ),
  Vector3(0,-0.6,0.3),
  None,
  scene
)



Plane(Point3(0,-0.6,0), Vector3(0,1,0),REFLECTIVE_BLUE,scene)
# Plane(Point3(-0.6,0,0), Vector3(1,0,0),REFLECTIVE_BLUE,scene)
# Plane(Point3(0,0,2), Vector3(0,0,-1),REFLECTIVE_BLUE,scene)


# Rotation(
# CSG([
      # Plane(Point3( 0, 0, 1  ), Vector3( 0, 0,-1)),
      # Plane(Point3( 0, 0, 1.1), Vector3( 0, 0, 1)),
      # Plane(Point3( 0.5, 0, 0  ), Vector3( 1, 0, 0)),
      # Plane(Point3(-0.5, 0, 0  ), Vector3(-1, 0, 0)),
      # Plane(Point3( 0, 0.5, 0  ), Vector3( 0, 1, 0)),
      # Plane(Point3( 0,-0.5, 0  ), Vector3( 0,-1, 0)),
  # ],
  # SHINY_RED,
  # scene
# )

# Sphere(Point3(0,0,2), 0.1, SHINY_RED, scene)
# Sphere(Point3(1,0,2), 0.1, SHINY_RED, scene)
# Sphere(Point3(0,1,2), 0.1, SHINY_RED, scene)
# Sphere(Point3(1,1,2), 0.1, SHINY_RED, scene)
# Sphere(Point3(1,1,4), 0.1, SHINY_RED, scene)
# Sphere(Point3(0,1,4), 0.1, SHINY_RED, scene)
# Sphere(Point3(1,0,4), 0.1, SHINY_RED, scene)
# Sphere(Point3(0,0,4), 0.1, SHINY_RED, scene)

view = View(Point3(0, 0.2, -2), # eye's location
            Point3(0, 0, 0),    # look at point
            Vector3(0, 1, 0),    # up vector
            45,                  # hfov
            225,                 # height
            360,                 # width
            3)                   # aa level

camera = Camera(view, scene)

img = camera.take_photo_new()
img.save('image.bmp')    # Display image in default image-viewer application
print "Rendering time:", datetime.now() - start
