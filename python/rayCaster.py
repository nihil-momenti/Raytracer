from geom3 import Point3, Vector3, Ray3, cross, dot, unit, length, GeomException
from math import sqrt, tan, atan, degrees
from geom3 import Point3, Vector3, Ray3, unit
from colour import Colour
from PIL import Image
from material import Material
from lighting import *
from scene import Scene
from shapes import Sphere, Plane
from datetime import datetime
from view import View


# Define various scene constants

MULTI = 1 # Level of linear AA

WIN_SIZE = 100            # Screen window size (square)
LIGHT_DIR = unit(Vector3(0.5,0.5,2))  # The direction vector towards the light source
LIGHT_INTENS = 0.8          # Intensity of the single white light source
AMBIENT = 0.1             # Ambient light level (assumed white light)
BACKGROUND = Colour(0.6,0.6,0.6)  # Colour of the background

SHINY_RED = Material(Colour(0.7, 0.3, 0.2), Colour(0.4,0.4,0.4), 100)
SHINY_BLUE = Material(Colour(0.2, 0.3, 0.7), Colour(0.8,0.8,0.8), 200)
MATT_GREEN = Material(Colour(0.1, 0.7, 0.1), Colour(1,1,1), 100)

# Warning the next three values can't be meaningfully altered until
# the View.eye_ray method has been rewritten.

EYEPOINT = Point3(0.5, 0.5, 4)  # Where the eye is
VIEWDIRECTION = Vector3(0, 0, -1)  # The look at point
VIEWUP = Vector3(0,1,0)
FOV = 45            # Field of view (degrees).


# ======= A Ray Tracing/Ray Casting Camera class ========= 

class Camera(object):
  '''An Camera provides a 'take_photo' method that computes the ray-casting 
     image of a given scene from a given view with given lighting.'''

  def __init__(self, view, scene, lighting):
    self.view = view
    self.scene = scene
    self.lighting = lighting

  def colours_along_rays(self, rays):
    colours = []
    hitpoints = self.scene.intersectMultiple(rays)
    for index in range(len(hitpoints)):
      if hitpoints[index][1] == float('Inf'):
        colours.append(BACKGROUND)
      else:
        (obj, alpha) = hitpoints[index]
        try:colours.append(obj.material.lit_colour(obj.normal(rays[index].pos(alpha)), self.lighting, -rays[index].dir))
        except GeomException:
          print obj
          print alpha
          print rays[index]
          
    return colours
  
  
  def colour_of_pixel(self, row, col):
    colour = Colour(0,0,0)
    for ray in self.view.eye_rays(row, col, MULTI):
      print ray
      hitpoint = self.scene.intersect(ray)
      if hitpoint[1] == float('Inf'):
        colour += BACKGROUND
      else:
        (obj, alpha) = hitpoint
        try:colour += obj.material.lit_colour(obj.normal(ray.pos(alpha)), self.lighting, -ray.dir)
        except GeomException:
          print obj
          print alpha
          print ray
          
    colour = colour / MULTI ** 2
    return colour

  def take_photo(self):
    img = Image.new("RGB", (self.view.width, self.view.height))
    
    for row in range(self.view.height):
      for col in range(self.view.width):
        pixel = self.colour_of_pixel(row, col)
        img.putpixel((col, row), pixel.intColour())
        
    return img

    
# ====== Main body. Compute and display image ========

start = datetime.now()
light = DirectionalLight(LIGHT_INTENS, LIGHT_DIR)
ambientLight = AmbientLight(AMBIENT)

scene = Scene([Sphere(Point3(0.35,0.6,0.5), 0.25, SHINY_BLUE),
         Sphere(Point3(0.75,0.2,0.6), 0.15, SHINY_RED),
         Plane(Point3(0.5,0.5,0), Vector3(0,0,1), MATT_GREEN)])

view = View(EYEPOINT, VIEWDIRECTION, VIEWUP, FOV, WIN_SIZE, WIN_SIZE)
camera = Camera(view, scene, [light, ambientLight])

img = camera.take_photo()
img.save('image.bmp')    # Display image in default image-viewer application
print "Rendering time:", datetime.now() - start
