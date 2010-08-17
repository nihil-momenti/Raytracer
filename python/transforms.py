from geom3 import Ray3, Point3, Vector3
from shapes import Shape
import math
from random import random
from material import Material
from colour import Colour

class MaterialTransform(Material):
  def __init__(self, material, transform):
    self.base = material
    self.transform = transform
    self.casts_shadow = material.casts_shadow
    self.shininess = material.shininess
    self.reflectivity = material.reflectivity
    self.refractivity = material.refractivity


  def diffuse_colour(self, point, normal):
    return self.base.diffuse_colour(self.transform.transform(point), self.transform.transform(normal))


  def specular_colour(self, point, normal):
      return self.base.specular_colour(self.transform.tranform(point), self.transform.transform(normal))



class Transform(Shape):
  def __init__(self, shape, scene=None):
    super(Transform,self).__init__(MaterialTransform(shape.material, self), scene)
    self.shape = shape
  
  
  def point_on_surface(self, p):
    return self.shape.point_on_surface(self.transform(p))
  
  
  def point_inside(self, p):
    return self.shape.point_inside(self.tranform(p))
  
  
  def normal(self, p):
    return self.inv_transform(self.shape.normal(self.transform(p)))
  
  
  def intersect(self, ray):
    return self.shape.intersect(self.transform(ray))



class Translation(Transform):
  def __init__(self, shape, vector, scene=None):
    super(Translation,self).__init__(shape, scene)
    self.vector = vector
  
  
  def transform(self, t):
    if isinstance(t, Vector3):
      return t
    elif isinstance(t, Ray3):
      return Ray3(t.start - self.vector, t.dir)
    elif isinstance(t, Point3):
      return t - self.vector
    else:
      print t
      raise Exception
  
  
  def inv_transform(self, t):
    if isinstance(t, Vector3):
      return t
    elif isinstance(t, Ray3):
      return Ray3(t.start + self.vector, t.dir)
    elif isinstance(t, Point3):
      return t + self.vector
    else:
      print t
      raise Exception



class Rotation(Transform):
  def __init__(self, shape, vector, angle, scene=None):
    super(Rotation,self).__init__(shape, scene)
    self.angle = math.radians(angle)
    self.v = vector.unit()
    self.w = Vector3(0,0,0)
    while self.w == Vector3(0,0,0):
      self.w = Vector3(random(), random(), random())
      self.w = (self.w - self.v * self.w.dot(self.v)).unit()
    self.u = self.v.cross(self.w).unit()
  
  
  def transform(self, t):
    if isinstance(t, Vector3):
      old_v = t.dot(self.v)
      old_w = t.dot(self.w)
      old_u = t.dot(self.u)
      
      r = math.sqrt(old_w ** 2 + old_u ** 2)
      theta = math.atan2(old_w, old_u) + self.angle
      
      new_w = r * math.sin(theta)
      new_u = r * math.cos(theta)
      
      return old_v * self.v + new_w * self.w + new_u * self.u
    elif isinstance(t, Point3):
      return Point3(self.transform(Vector3(t)))
    elif isinstance(t, Ray3):
      return Ray3(self.transform(t.start), self.transform(t.dir))
    else:
      print t
      raise Exception
  
  
  def inv_transform(self, t):
    if isinstance(t, Vector3):
      old_v = t.dot(self.v)
      old_w = t.dot(self.w)
      old_u = t.dot(self.u)
      
      r = math.sqrt(old_w ** 2 + old_u ** 2)
      theta = math.atan2(old_w, old_u) - self.angle
      
      new_w = r * math.sin(theta)
      new_u = r * math.cos(theta)
      
      return old_v * self.v + new_w * self.w + new_u * self.u
    elif isinstance(t, Point3):
      return Point3(self.inv_transform(Vector3(t)))
    elif isinstance(t, Ray3):
      return Ray3(inv_transform(t.start), inv_transform(t.dir))
    else:
      print t
      raise Exception

