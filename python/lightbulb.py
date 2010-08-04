from material import *
from lighting import PointLight
from shapes import Sphere
from math import sqrt

class LightBulb(object):
  def __init__(self, colour, point, size, scene):
    light = PointLight(colour, point, scene)
    material = LightBulbMaterial(light)
    bulb = Sphere(point, size, material, scene)


class LightBulbMaterial(Material):
  def __init__(self, light):
    super(LightBulbMaterial, self).__init__(None)
    self.casts_shadow = False
    self.light = light
  
  def lit_colour(self, scene, normal, view_vector, point):
    return ((view_vector.dot(normal) ** 2 + 0.5)) * self.light.diffuseLighting(-normal, point, scene)
