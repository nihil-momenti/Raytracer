from PIL import Image
from colour import Colour

BACKGROUND = Colour(0.6,0.6,0.6)  # Colour of the background

class Camera(object):
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
    rays = self.view.eye_rays(row, col)
    for ray in rays:
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
          
    colour = colour / len(rays)
    return colour


  def take_photo(self):
    img = Image.new("RGB", (self.view.width, self.view.height))
    
    for row in range(self.view.height):
      for col in range(self.view.width):
        pixel = self.colour_of_pixel(row, col)
        img.putpixel((col, row), pixel.intColour())
        
    return img
