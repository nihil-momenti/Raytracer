from PIL import Image
import colour
import math

def diff(colour1, colour2):
  dr = abs(colour1.r - colour2.r)
  dg = abs(colour1.g - colour2.g)
  db = abs(colour1.b - colour2.b)
  return (dr + dg + db)

class Camera(object):
  def __init__(self, view, scene):
    self.view = view
    self.scene = scene

  def single_colour_of_pixel(self, row, col):
    ray = self.view.eye_ray(row, col)
    hitpoint = self.scene.intersect(ray)
    if hitpoint[1] == float('Inf'):
      return colour.Colour(0.6,0.6,0.6)
    else:
      (obj, alpha) = hitpoint
      pos = ray.pos(alpha)
      normal = obj.normal(pos)
      return obj.material.lit_colour(self.scene, normal, -ray.dir, pos)

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
        color += obj.material.lit_colour(self.scene, normal, -ray.dir, pos)
          
    color = color / len(rays)
    return color


  def check_pixel(self, pixels, row, col):
    color = pixels[row * self.view.width + col]
    icol_min = -1 if col > 1 else 0
    icol_max = 2 if col < self.view.width - 3 else 1
    irow_min = -1 if row > 1 else 0
    irow_max = 2 if row < self.view.height - 3 else 1
    for icol in range(icol_min, icol_max):
      for irow in range(irow_min, irow_max):
        if diff(pixels[(row + irow) * self.view.width + (col + icol)], color) > 0.01:
          return self.colour_of_pixel(row, col)
    return color


  def take_photo_new(self):
    img = Image.new("RGB", (self.view.width, self.view.height))
    img_pixels = img.load()
    
    print "Starting first pass..."
    pixels = [self.single_colour_of_pixel(row, col)
      for row in range(self.view.height)
      for col in range(self.view.width)]
    
#    print "Starting anti-aliasing..."
#    pixels = [self.check_pixel(pixels, row, col)
#      for row in range(self.view.height)
#      for col in range(self.view.width)]
    
    img.putdata([pixel.intColour() for pixel in pixels])
    
    return img


  def take_photo(self):
    img = Image.new("RGB", (self.view.width, self.view.height))
    
    perPercent = math.ceil(self.view.height / 100.0)
    
    for row in range(self.view.height):
      if row % perPercent == 0:
        print ("%3d" % (row / perPercent)) + "%"
      for col in range(self.view.width):
        img.putpixel((col, row), self.colour_of_pixel(row, col).intColour())
    
    print "100%"
    
    return img
