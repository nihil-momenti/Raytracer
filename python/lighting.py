from colour import Colour
from geom3 import Ray3

class AmbientLight(object):
  def __init__(self, value):
    self.value = value

  def specularLighting(self, normal, view_vector, point, scene):
    return Colour(0,0,0)

  def diffuseLighting(self, normal, point, scene):
    return self.value
    
class DirectionalLight(object):
  def __init__(self, value, direction):
    self.value = value
    self.direction = direction.unit()

  def specularLighting(self, normal, view_vector, point, scene):
    if (scene.intersect(Ray3(point + self.direction * 0.0001, self.direction))[1] != float('Inf')):
      return Colour(0,0,0)
    h = (self.direction + view_vector.unit()).unit()
    return self.value * max(0, h.dot(normal))

  def diffuseLighting(self, normal, point, scene):
    if (scene.intersect(Ray3(point + self.direction * 0.0001, self.direction))[1] != float('Inf')):
      return Colour(0,0,0)
    return self.value * max(0, self.direction.dot(normal))


class PointLight(object):
  def __init__(self, value, point):
    self.value = value
    self.point = point

  def specularLighting(self, normal, view_vector, point, scene):
    direction = (self.point - point).unit()
    h = (direction + view_vector.unit()).unit()
    return self.value * max(0, h.dot(normal))

  def diffuseLighting(self, normal, point, scene):
    direction = (self.point - point).unit()
    return self.value * max(0, direction.dot(normal))


class FocusedLight(object):
  def __init__(self, value, point, direction, spread):
    self.value = value
    self.point = point
    self.direction = -direction.unit()
    self.spread = spread

  def specularLighting(self, normal, view_vector, point, scene):
    if (scene.intersect(Ray3(point + self.direction * 0.0001, self.direction))[1] != float('Inf')):
      return Colour(0,0,0)
    direction = (self.point - point).unit()
    multiplier = max(0, direction.dot(self.direction)) ** self.spread
    h = (direction + view_vector.unit()).unit()
    return self.value * multiplier * max(0, h.dot(normal))

  def diffuseLighting(self, normal, point, scene):
    if (scene.intersect(Ray3(point + self.direction * 0.0001, self.direction))[1] != float('Inf')):
      return Colour(0,0,0)
    fullDirection = self.point - point
    direction = fullDirection.unit()
    multiplier = max(0, direction.dot(self.direction)) ** self.spread
    return self.value * multiplier * max(0,5 - fullDirection.length())/5 * max(0, direction.dot(normal))

