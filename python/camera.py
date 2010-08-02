from PIL import Image
from colour import Colour

BACKGROUND = Colour(0.6,0.6,0.6)  # Colour of the background

class Camera(object):
  def __init__(self, view, scene, lighting):
    self.view = view
    self.scene = scene
    self.lighting = lighting


  def colour_of_pixel(self, row, col):
    colour = Colour(0,0,0)
    rays = self.view.eye_rays(row, col)
    for ray in rays:
      hitpoint = self.scene.intersect(ray)
      if hitpoint[1] == float('Inf'):
        colour += BACKGROUND
      else:
        (obj, alpha) = hitpoint
        pos = ray.pos(alpha)
        normal = obj.normal(pos)
        colour += obj.material.lit_colour(normal, self.lighting, -ray.dir, pos)
          
    colour = colour / len(rays)
    return colour


  def take_photo(self):
    img = Image.new("RGB", (self.view.width, self.view.height))
    
    for row in range(self.view.height):
      for col in range(self.view.width):
        pixel = self.colour_of_pixel(row, col)
        img.putpixel((col, row), pixel.intColour())
        
    return img
