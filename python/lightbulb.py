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
    self.addition = sqrt(light.value.r ** 2 + light.value.g ** 2 + light.value.b ** 2)
    
  def lit_colour(self, scene, normal, view_vector, point, n=0):
    return (view_vector.dot(normal) ** 2) * self.light.diffuseLighting(-normal, point, scene) + Colour(0.5, 0.5, 0.5)
