from csg import *
from view import *
from scene import *
from shapes import *
from colour import *
from camera import *
from texture import *
from material import *
from lighting import *
from lightbulb import *
from transforms import *
from geom3 import Point3, Vector3, Ray3, unit

def generateScene():
  SHINY_RED  = Material(Colour(0.7,0.3,0.2), Colour(0.4,0.4,0.4),  100)
  SHINY_BLUE = Material(Colour(0.2,0.3,0.7), Colour(0.8,0.8,0.8),  200)
  
  MATT_RED   = Material(Colour(0.7,0.3,0.2), None, None)
  MATT_BLUE  = Material(Colour(0.1,0.1,0.7), None, None)
  MATT_GREEN = Material(Colour(0.1,0.7,0.1), None, None)
  MATT_WHITE = Material(Colour(1  ,1  ,1  ), None, None)
  
  WALL_TEXTURE = Texture(Point3(0,0,0), # Top left point
    'wall_tiles.jpg', Vector3(0,4,0), Vector3(0,0,4), Vector3(4,0,0), # Texture file, x vector, y vector
    None, None, None) # Specular colour, shininess, reflectivity
  WALL_TEXTURE.casts_shadow = False

  FLOOR_TEXTURE = Texture(Point3(0,0,0), # Top left point
    'floor_tiles.jpg', Vector3(4,0,0), Vector3(0,0,4), Vector3(0,4,0),# Texture file, x vector, y vector
    None, None, None) # Specular colour, shininess, reflectivity

  REF_BLUE   = Material(Colour(0.2,0.3,0.7), Colour(0.2,0.2,0.2),  200, 0.1)
  
  REFLECTIVE = Material(Colour(0.1,0.1,0.1), None, None, 1.0)

  GOLD   = Material(Colour(0.78,0.58,0.09), None, None, 0.1)
  SILVER = Material(Colour(0.75,0.75,0.75), None, None, 0.1)
  BRONZE = Material(Colour(0.80,0.50,0.20), None, None, 0.1)


  WOOD = Texture(Point3(0,0,0), # Top left point
    'Desk_Texture.jpg', Vector3(4,0,0), Vector3(0,4,0), Vector3(0,0,4), # Texture file, x vector, y vector
    None, None, None) # Specular colour, shininess, reflectivity
  
  scene = Scene()

  FocusedLight(Colour(1,1,1), Point3(-0.1, 1, 0.2), Point3(0, -0.6, 0.3), 20, scene)
  PointLight(Colour(0.8, 0.8, 0.8), Point3(-0.5, 0, 0), scene)
  AmbientLight(Colour(0.1,0.1,0.1), scene)
  
  ##Mirror glass
#  Translation(
#    Rotation(
#      Intersection([
#        Plane(Point3( 0  , 0  , 0   ), Vector3( 0, 0,-1)),
#        Plane(Point3( 0  , 0  , 0.01), Vector3( 0, 0, 1)),
#        Plane(Point3( 0.5, 0  , 0   ), Vector3( 1, 0, 0)),
#        Plane(Point3(-0.5, 0  , 0   ), Vector3(-1, 0, 0)),
#        Plane(Point3( 0  , 0.5, 0   ), Vector3( 0, 1, 0)),
#        Plane(Point3( 0  ,-0.5, 0   ), Vector3( 0,-1, 0)),
#      ], REFLECTIVE),
#      Vector3(-0.4,1,0.1), 40
#    ),
#    Vector3(0.4,0,0.8),
#    scene
#  )
  
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
      ], WOOD),
      Vector3(-0.4,1,0.1), 40
    ),
    Vector3(0.4,0,0.8),
    scene
  )
  
  ## Pedestal Base
  Translation(
    Rotation(
      Intersection([
        Plane(Point3( 0  , 0   ,-0.1), Vector3( 0, 0,-1)),
        Plane(Point3( 0  , 0   , 0.1), Vector3( 0, 0, 1)),
        Plane(Point3( 0.3, 0   , 0  ), Vector3( 1, 0, 0)),
        Plane(Point3(-0.3, 0   , 0  ), Vector3(-1, 0, 0)),
        Plane(Point3( 0  , 0.2 , 0  ), Vector3( 0, 1, 0)),
        Plane(Point3( 0  , 0   , 0  ), Vector3( 0,-1, 0)),
      ], WOOD),
      Vector3(0,1,0), 30
    ),
    Vector3(0,-0.6,0.3),
    scene
  )
  
  ## Pedestal Top
  Translation(
    Rotation(
      Intersection([
        Plane(Point3( 0  , 0   ,-0.1), Vector3( 0, 0,-1)),
        Plane(Point3( 0  , 0   , 0.1), Vector3( 0, 0, 1)),
        Plane(Point3( 0.1, 0   , 0  ), Vector3( 1, 0, 0)),
        Plane(Point3(-0.1, 0   , 0  ), Vector3(-1, 0, 0)),
        Plane(Point3( 0  , 0.4 , 0  ), Vector3( 0, 1, 0)),
        Plane(Point3( 0  , 0.2 , 0  ), Vector3( 0,-1, 0)),
      ], WOOD),
      Vector3(0,1,0), 30
    ),
    Vector3(0,-0.6,0.3),
    scene
  )
  
  ## Gold Ball
  Sphere(Point3(0,-0.1,0.3), 0.09, GOLD, scene)
  
  ## Silver Ball
  Sphere(Point3(-0.18,-0.3,0.4), 0.09, SILVER, scene)
  
  ## Bronze Ball
  Sphere(Point3(0.18,-0.3,0.2), 0.09, BRONZE, scene)

  ## Textured Ball
  Sphere(Point3(-0.4, 0, 1), 0.2, WOOD, scene)
  
  ## Floor
  Plane(Point3(0,-0.6,0), Vector3(0,1,0), FLOOR_TEXTURE, scene)
  
  ## Walls
  Plane(Point3(-1  , 0  , 0  ), Vector3( 1, 0, 0), WALL_TEXTURE, scene)
  Plane(Point3( 1  , 0  , 0  ), Vector3(-1, 0, 0), WALL_TEXTURE, scene)
  Plane(Point3( 0  , 0  , 2  ), Vector3( 0, 0,-1), WALL_TEXTURE, scene)
  Plane(Point3( 0  , 0  ,-2  ), Vector3( 0, 0, 1), WALL_TEXTURE, scene)

  ## Roof
  Plane(Point3(0, 1, 0), Vector3(0, -1, 0), MATT_WHITE, scene)
  
  
  
  view = View(Point3(0, 1, -2), # eye's location
              Point3(0,0.2, 0),    # look at point
              Vector3(0, 1, 0),    # up vector
              45,                  # hfov
              400,                 # height
              640,                # width
              1)                   # aa level
  
  return view, scene

