from PIL import Image
import colour

class Camera(object):
  def __init__(self, view, scene, lighting):
    self.view = view
    self.scene = scene
    self.lighting = lighting


  def colour_of_pixel(self, row, col):
    color = colour.Colour(0,0,0)
    rays = self.view.eye_rays(row, col)
    for ray in rays:
      hitpoint = self.scene.intersect(ray)
      if hitpoint[1] == float('Inf'):
        color += colour.Colour(0.6,0.6,0.6)
      else:
        (obj, alpha) = hitpoint
        pos = ray.pos(alpha)
        normal = obj.normal(pos)
        color += obj.material.lit_colour(self.scene, normal, self.lighting, -ray.dir, pos)
          
    color = color / len(rays)
    return color


  def take_photo(self):
    img = Image.new("RGB", (self.view.width, self.view.height))
    
    perPercent = self.view.height / 100
    
    print "  0 %",
    for row in range(self.view.height):
      if row % perPercent == 0:
        print "\b\b\b\b\b\b", "%2d" % (row / perPercent), "%",
      for col in range(self.view.width):
        img.putpixel((col, row), self.colour_of_pixel(row, col).intColour())
    
    print "\b\b\b\b\b\b100 % "
    
    return img
