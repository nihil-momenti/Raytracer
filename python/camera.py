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
      return obj.material(pos).lit_colour(self.scene, normal, -ray.dir, pos)

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
        color += obj.material(pos).lit_colour(self.scene, normal, -ray.dir, pos)
          
    color = color / len(rays)
    return color


  def check_pixel(self, pixels, row, col):
    color = pixels[row][col]
    for icol in range(-1, 2):
      for irow in range(-1, 2):
        if diff(pixels[min(self.view.height - 1, max(0, row + irow))][min(self.view.width - 1, max(0, col + icol))], color) > 0.01:
          return self.colour_of_pixel(row, col)
    return color
    #if (diff(pixels[min(self.view.height, max(0, row))][min(self.view.height, max(0, col))], color) > 0.1):
    # if (diff(pixels[max(0, row - 1)][max(0, col - 1)], color) > 0.1):
      # self.changed[row - 1][col - 1] = True
      # self.changed[row][col] = True
    # if (diff(pixels[max(0, row)][max(0, col - 1)], color) > 0.1):
      # self.changed[row][col - 1] = True
      # self.changed[row][col] = True
    # if (diff(pixels[max(0, row - 1)][max(0, col)], color) > 0.1):
      # self.changed[row - 1][col] = True
      # self.changed[row][col] = True
    # if (diff(pixels[min(0, row + 1)][min(0, col - 1)], color) > 0.1):
      # self.changed[row - 1][col - 1] = True
      # self.changed[row][col] = True
    # if (diff(pixels[min(0, row)][min(0, col - 1)], color) > 0.1):
      # self.changed[row][col - 1] = True
      # self.changed[row][col] = True
    # if (diff(pixels[min(0, row - 1)][min(0, col)], color) > 0.1):
      # self.changed[row - 1][col] = True
      # self.changed[row][col] = True


  def take_photo_new(self):
    img = Image.new("RGB", (self.view.width, self.view.height))
    
    print "Starting first pass..."
    pixels = [[self.single_colour_of_pixel(row, col)
      for col in range(self.view.width)]
      for row in range(self.view.height)]
    
    print "Starting anti-aliasing..."
    pixels = [[self.check_pixel(pixels, row, col)
      for col in range(self.view.width)]
      for row in range(self.view.height)]
    
    [[img.putpixel((col, row), pixels[row][col].intColour())
      for col in range(self.view.width)]
      for row in range(self.view.height)]
    
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
