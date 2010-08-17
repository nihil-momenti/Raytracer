from shapes import Plane
from PIL import Image
from geom3 import Ray3, epsilon
from colour import Colour
from math import floor
from material import Material

class Texture(Material):
  def __init__(self, point, texture_file, x_direction, y_direction, specular_colour=None, shininess=None, reflectivity=None, refractivity=None):
    super(Texture,self).__init__(None, specular_colour, shininess, reflectivity, refractivity)
    self.point = point
    image = Image.open(texture_file)
    self.texture = image.load()
    self.width, self.height = image.size
    self.x_vector = x_direction.unit() / x_direction.length()
    self.y_vector = y_direction.unit() / y_direction.length()
    self.z_vector = x_direction.cross(y_direction).unit() / x_direction.cross(y_direction).length()
    self.last_colour = (None, None)


  def diffuse_colour(self, point, normal):
    if self.last_colour[0] is not None and self.last_colour[0] == point:
      return self.last_colour[1]

    if self.texture is not None:
      x_amount = (point - self.point).dot(self.x_vector)
      y_amount = (point - self.point).dot(self.y_vector)
      z_amount = (point - self.point).dot(self.z_vector)
      if abs(normal.dot(self.x_vector)) < epsilon:
        x = floor(((x_amount + z_amount) % 1.0) * self.width)
      else:
        x = floor((x_amount % 1.0) * self.width)
      if abs(normal.dot(self.y_vector)) < epsilon:
        y = floor(((y_amount + z_amount) % 1.0) * self.height)
      else:
        y = floor((y_amount % 1.0) * self.height)
      colour = self.texture[x, y]

      if isinstance(colour,int):
        colour = Colour(colour/255.0, colour/255.0, colour/255.0)
      else:
        colour = Colour(colour[0]/255.0, colour[1]/255.0, colour[2]/255.0)
        
      self.last_colour = (point, colour)
      return colour
