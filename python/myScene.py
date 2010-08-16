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

def generateScene():
  SHINY_RED  = Material(Colour(0.7,0.3,0.2), Colour(0.4,0.4,0.4),  100)
  SHINY_BLUE = Material(Colour(0.2,0.3,0.7), Colour(0.8,0.8,0.8),  200)
  
  MATT_RED   = Material(Colour(0.7,0.1,0.1), None, None)
  MATT_BLUE  = Material(Colour(0.1,0.1,0.7), None, None)
  MATT_GREEN = Material(Colour(0.1,0.7,0.1), None, None)
  
  WALL_COLOUR = Material(Colour(1.0,1.0,1.0), None, None)
  WALL_COLOUR.casts_shadow = False

  REF_BLUE   = Material(Colour(0.2,0.3,0.7), Colour(0.8,0.8,0.8),  200, 0.1)
  
  REFLECTIVE = Material(None, None, None, 1.0)
  
  scene = Scene()

  FocusedLight(Colour(3,3,3), Point3(-0.4, 2, 0), Point3(0, -0.4, 0.35), 20, scene)
  PointLight(Colour(0.8, 0.8, 0.8), Point3(0, 0, 0), scene)
  AmbientLight(Colour(0.1,0.1,0.1), scene)
  
  ##Mirror glass
  Translation(
    Rotation(
      Intersection([
        Plane(Point3( 0  , 0  , 0   ), Vector3( 0, 0,-1)),
        Plane(Point3( 0  , 0  , 0.01), Vector3( 0, 0, 1)),
        Plane(Point3( 0.5, 0  , 0   ), Vector3( 1, 0, 0)),
        Plane(Point3(-0.5, 0  , 0   ), Vector3(-1, 0, 0)),
        Plane(Point3( 0  , 0.5, 0   ), Vector3( 0, 1, 0)),
        Plane(Point3( 0  ,-0.5, 0   ), Vector3( 0,-1, 0)),
      ]),
      Vector3(-0.8,1,0), 40
    ),
    Vector3(0.4,0,0.8),
    REFLECTIVE,
    scene
  )
  
  ##Mirror frame
  Translation(
    Rotation(
      Intersection([
        Plane(Point3( 0   , 0   , 0.0001  ), Vector3( 0, 0,-1)),
        Plane(Point3( 0   , 0   , 0.1), Vector3( 0, 0, 1)),
        Plane(Point3( 0.53, 0   , 0  ), Vector3( 1, 0, 0)),
        Plane(Point3(-0.53, 0   , 0  ), Vector3(-1, 0, 0)),
        Plane(Point3( 0   , 0.53, 0  ), Vector3( 0, 1, 0)),
        Plane(Point3( 0   ,-0.53, 0  ), Vector3( 0,-1, 0)),
      ]),
      Vector3(-0.8,1,0), 40
    ),
    Vector3(0.4,0,0.8),
    SHINY_RED,
    scene
  )
  
  ## Pedestal Base
  Translation(
    Rotation(
      Intersection([
        Plane(Point3( 0  , 0   , 0  ), Vector3( 0, 0,-1)),
        Plane(Point3( 0  , 0   , 0.1), Vector3( 0, 0, 1)),
        Plane(Point3( 0.15, 0   , 0  ), Vector3( 1, 0, 0)),
        Plane(Point3(-0.15, 0   , 0  ), Vector3(-1, 0, 0)),
        Plane(Point3( 0  , 0.1 , 0  ), Vector3( 0, 1, 0)),
        Plane(Point3( 0  , 0   , 0  ), Vector3( 0,-1, 0)),
      ]),
      Vector3(0,1,0), 30
    ),
    Vector3(0,-0.6,0.3),
    SHINY_RED,
    scene
  )
  
  ## Pedestal Top
  Translation(
    Rotation(
      Intersection([
        Plane(Point3( 0  , 0   , 0  ), Vector3( 0, 0,-1)),
        Plane(Point3( 0  , 0   , 0.1), Vector3( 0, 0, 1)),
        Plane(Point3( 0.05, 0   , 0  ), Vector3( 1, 0, 0)),
        Plane(Point3(-0.05, 0   , 0  ), Vector3(-1, 0, 0)),
        Plane(Point3( 0  , 0.2 , 0  ), Vector3( 0, 1, 0)),
        Plane(Point3( 0  , 0.1 , 0  ), Vector3( 0,-1, 0)),
      ]),
      Vector3(0,1,0), 30
    ),
    Vector3(0,-0.6,0.3),
    SHINY_RED,
    scene
  )
  
  ## Reflective Ball
  Sphere(Point3(0,-0.3,0.3), 0.07, REFLECTIVE, scene)
  
  
  ## Floor
  Plane(Point3(0,-0.6,0), Vector3(0,1,0),REF_BLUE,scene)
  
  ## Walls
  Plane(Point3(-1  , 0  , 0  ), Vector3( 1, 0, 0), WALL_COLOUR, scene)
  Plane(Point3( 1  , 0  , 0  ), Vector3(-1, 0, 0), WALL_COLOUR, scene)
  Plane(Point3( 0  , 0  , 2  ), Vector3( 0, 0,-1), WALL_COLOUR, scene)
  Plane(Point3( 0  , 0  ,-2  ), Vector3( 0, 0, 1), WALL_COLOUR, scene)

  ## Roof
  Plane(Point3(0, 1, 0), Vector3(0, -1, 0), WALL_COLOUR, scene)
  
  
  
  view = View(Point3(0, 1, -2), # eye's location
              Point3(0,0.2, 0),    # look at point
              Vector3(0, 1, 0),    # up vector
              45,                  # hfov
              900,                 # height
              1440,                 # width
              4)                   # aa level
  
  return view, scene

