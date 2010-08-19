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
  FLOOR_TEXTURE = Texture(Point3(-1,-0.6,2), # Top left point
    'floor_tiles.jpg', Vector3(1,0,0), Vector3(0,0,1), Vector3(0,1,0),# Texture file, x vector, y vector
    None, None, None) # Specular colour, shininess, reflectivity

  REFLECTIVE = Material(Colour(0.1,0.1,0.1), None, None, 1.0)
  GOLD   = Material(Colour(0.78,0.58,0.09), None, None, 0.2)

  STONE = Texture(Point3(0,0,0), # Top left point
    'stone.jpg', Vector3(0.5,0,0), Vector3(0,0.5,0), Vector3(0,0,0.5), # Texture file, x vector, y vector
    None, None, None) # Specular colour, shininess, reflectivity
  
  WOOD = Texture(Point3(0,0,0), # Top left point
    'Desk_Texture.jpg', Vector3(2,0,0), Vector3(0,2,0), Vector3(0,0,2), # Texture file, x vector, y vector
    None, None, None) # Specular colour, shininess, reflectivity
  
  scene = Scene()

  FocusedLight(Colour(1,1,1), Point3(0, 1, 0.3), Point3(0, 0, 0.3), 20, scene)
  PointLight(Colour(1, 1, 1), Point3(1, 0.5, 0), scene)
  PointLight(Colour(1, 1, 1), Point3(-1, 0.5, 0), scene)
  AmbientLight(Colour(0.05,0.05,0.05), scene)
  
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
      ], REFLECTIVE),
      Vector3(-0.4,1,0.1), 40
    ),
    Vector3(0.4,0,0.8),
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
      ], WOOD),
      Vector3(-0.4,1,0.1), 40
    ),
    Vector3(0.4,0,0.8),
    scene
  )
  
  ## Pedestal Top
  Translation(
    Rotation(
      Intersection([
        Plane(Point3( 0  , 0   ,-0.2), Vector3( 0, 0,-1)),
        Plane(Point3( 0  , 0   , 0.2), Vector3( 0, 0, 1)),
        Plane(Point3( 0.2, 0   , 0  ), Vector3( 1, 0, 0)),
        Plane(Point3(-0.2, 0   , 0  ), Vector3(-1, 0, 0)),
        Plane(Point3( 0  , 0.4 , 0  ), Vector3( 0, 1, 0)),
        Plane(Point3( 0  , 0   , 0  ), Vector3( 0,-1, 0)),
      ], STONE),
      Vector3(0,1,0), 30
    ),
    Vector3(0,-0.6,0.3),
    scene
  )
  
  ## Reflective Ball
  Sphere(Point3(0,0, 0.3), 0.2, GOLD, scene)
  
  ## Floor
  Plane(Point3(0,-0.6,0), Vector3(0,1,0), FLOOR_TEXTURE, scene)
  
  
  view = View(Point3(0,0.5, -2), # eye's location
              Point3(0,0, 0),    # look at point
              Vector3(0, 1, 0),    # up vector
              45,                  # hfov
              200,                 # height
              320,                # width
              2)                   # aa level
  
  return view, scene

