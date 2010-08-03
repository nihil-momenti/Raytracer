from colour import Colour
from geom3 import Ray3

def distanceLoss(distance):
  return max(0, 5 - distance) / 5

class AmbientLight(object):
  def __init__(self, value, scene=None):
    self.value = value
    if scene is not None:
      scene.addLight(self)

  def specularLighting(self, normal, view_vector, point, scene):
    return Colour(0,0,0)

  def diffuseLighting(self, normal, point, scene):
    return self.value
    
class DirectionalLight(object):
  def __init__(self, value, direction, scene=None):
    self.value = value
    self.direction = direction.unit()
    if scene is not None:
      scene.addLight(self)

  def specularLighting(self, normal, view_vector, point, scene):
    direction = self.direction
    distance = float('Inf')
    hitpoint = scene.intersect(Ray3(point + direction * 0.0001, direction))
    if (hitpoint[1] < distance and hitpoint[0].material.casts_shadow):
      return Colour(0,0,0)
    h = (self.direction + view_vector.unit()).unit()
    return self.value * max(0, h.dot(normal))

  def diffuseLighting(self, normal, point, scene):
    direction = self.direction
    distance = float('Inf')
    hitpoint = scene.intersect(Ray3(point + direction * 0.0001, direction))
    if (hitpoint[1] < distance and hitpoint[0].material.casts_shadow):
      return Colour(0,0,0)
    return self.value * max(0, self.direction.dot(normal))


class PointLight(object):
  def __init__(self, value, point, scene=None):
    self.value = value
    self.point = point
    if scene is not None:
      scene.addLight(self)

  def specularLighting(self, normal, view_vector, point, scene):
    vector = self.point - point
    direction = vector.unit()
    distance = vector.length()
    hitpoint = scene.intersect(Ray3(point + direction * 0.0001, direction))
    if (hitpoint[1] < distance and hitpoint[0].material.casts_shadow):
      return Colour(0,0,0)
    h = (direction + view_vector.unit()).unit()
    return self.value * distanceLoss(distance) * max(0, h.dot(normal))

  def diffuseLighting(self, normal, point, scene):
    vector = self.point - point
    direction = vector.unit()
    distance = vector.length()
    hitpoint = scene.intersect(Ray3(point + direction * 0.0001, direction))
    if (hitpoint[1] < distance and hitpoint[0].material.casts_shadow):
      return Colour(0,0,0)
    return self.value * distanceLoss(distance) *  max(0, direction.dot(normal))


class FocusedLight(object):
  def __init__(self, value, point, direction, spread, scene=None):
    self.value = value
    self.point = point
    self.direction = -direction.unit()
    self.spread = spread
    if scene is not None:
      scene.addLight(self)

  def specularLighting(self, normal, view_vector, point, scene):
    vector = self.point - point
    direction = vector.unit()
    distance = vector.length()
    hitpoint = scene.intersect(Ray3(point + direction * 0.0001, direction))
    if (hitpoint[1] < distance and hitpoint[0].material.casts_shadow):
      return Colour(0,0,0)
    multiplier = max(0, direction.dot(self.direction)) ** self.spread
    h = (direction + view_vector.unit()).unit()
    return self.value * multiplier * distanceLoss(distance) *  max(0, h.dot(normal))

  def diffuseLighting(self, normal, point, scene):
    vector = self.point - point
    direction = vector.unit()
    distance = vector.length()
    hitpoint = scene.intersect(Ray3(point + direction * 0.0001, direction))
    if (hitpoint[1] < distance and hitpoint[0].material.casts_shadow):
      return Colour(0,0,0)
    multiplier = max(0, direction.dot(self.direction)) ** self.spread
    return self.value * multiplier * distanceLoss(distance) *  max(0, direction.dot(normal))

