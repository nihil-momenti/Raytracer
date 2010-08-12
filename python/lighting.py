from colour import Colour
from geom3 import Ray3
import math

class Light(object):
  def __init__(self, value, scene=None):
    self.value = value
    if scene is not None:
      scene.addLight(self)
  
  
  def distanceLoss(self, distance):
    return (max(0, 8 - distance) / 8) ** 3
  
  
  def checkShadow(self, point, direction, distance, scene):
      ray = Ray3(point + direction * 0.0001, direction)
      hitpoint = scene.intersect(ray)
      (obj, alpha) = hitpoint
      pos = ray.pos(alpha)
      return (alpha < distance and obj.material.casts_shadow)



class AmbientLight(Light):
  def __init__(self, value, scene=None):
    super(AmbientLight, self).__init__(value, scene)
  
  
  def specularLighting(self, normal, view_vector, point, scene):
    return Colour(0,0,0)
  
  
  def diffuseLighting(self, normal, point, scene):
    return self.value



class DirectionalLight(Light):
  def __init__(self, value, direction, scene=None):
    super(DirectionalLight, self).__init__(value, scene)
    self.direction = -direction.unit()
  
  
  def specularLighting(self, normal, view_vector, point, scene):
    if self.checkShadow(point, self.direction, float('Inf'), scene):
      return Colour(0,0,0)
    else:
      h = (self.direction + view_vector.unit()).unit()
      return self.value * max(0, h.dot(normal))
  
  
  def diffuseLighting(self, normal, point, scene):
    if self.checkShadow(point, self.direction, float('Inf'), scene):
      return Colour(0,0,0)
    else:
      return self.value * max(0, self.direction.dot(normal))



class PointLight(Light):
  def __init__(self, value, point, scene=None):
    super(PointLight, self).__init__(value, scene)
    self.point = point
  
  
  def specularLighting(self, normal, view_vector, point, scene):
    vector = self.point - point
    direction = vector.unit()
    distance = vector.length()
    
    if self.checkShadow(point, direction, distance, scene):
      return Colour(0,0,0)
    else:
      h = (direction + view_vector.unit()).unit()
      return self.value * self.distanceLoss(distance) * max(0, h.dot(normal))
  
  
  def diffuseLighting(self, normal, point, scene):
    vector = self.point - point
    direction = vector.unit()
    distance = vector.length()
    
    if self.checkShadow(point, direction, distance, scene):
      return Colour(0,0,0)
    else:
      return self.value * self.distanceLoss(distance) *  max(0, direction.dot(normal))



class FocusedLight(Light):
  def __init__(self, value, point, aim_point, angle, scene=None):
    super(FocusedLight, self).__init__(value, scene)
    self.point = point
    self.direction = (point - aim_point).unit()
    self.angle = math.radians(angle)
  
  
  def spread(self, direction):
    theta = math.acos(direction.dot(self.direction))
    if theta < 0:
      return 0
    else:
      return (max(0, self.angle - theta) / self.angle) ** 2
  
  
  def specularLighting(self, normal, view_vector, point, scene):
    vector = self.point - point
    direction = vector.unit()
    distance = vector.length()
    
    if self.checkShadow(point, direction, distance, scene):
      return Colour(0,0,0)
    else:
      h = (direction + view_vector.unit()).unit()
      return self.value * self.spread(direction) * self.distanceLoss(distance) *  max(0, h.dot(normal))
  
  
  def diffuseLighting(self, normal, point, scene):
    vector = self.point - point
    direction = vector.unit()
    distance = vector.length()
    
    if self.checkShadow(point, direction, distance, scene):
      return Colour(0,0,0)
    else:
      return self.value * self.spread(direction) * self.distanceLoss(distance) *  max(0, direction.dot(normal))

