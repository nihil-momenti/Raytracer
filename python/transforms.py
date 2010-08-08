from geom3 import Ray3, Point3, Vector3
from shapes import Shape
import math
from random import random

class Transform(Shape):
  def __init__(self, shape, material=None, scene=None):
    super(Transform,self).__init__(material, scene)
    self.shape = shape
  
  
  def material(self, point):
    if self.m is not None:
      return self.m
    else:
      return self.shape.material(self.transform(point))
  
  
  def point_on_surface(self, p):
    return self.shape.point_on_surface(self.transofrm(p))
  
  
  def point_inside(self, p):
    return self.shape.point_inside(self.transform(p))
  
  
  def normal(self, p):
    return self.inv_transform(self.shape.normal(self.transform(p)))
  
  
  def intersect(self, ray):
    return self.shape.intersect(Ray3(self.transform(ray.start), self.transform(ray.dir)))



class Translation(Transform):
  def __init__(self, shape, vector, material=None, scene=None):
    super(Translation,self).__init__(shape, material, scene)
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
  def __init__(self, shape, vector, angle, material=None, scene=None):
    super(Rotation,self).__init__(shape, material, scene)
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
      # old_v = t.dot(self.v)
      # old_w = t.dot(self.w)
      # old_u = t.dot(self.u)
      
      # r = math.sqrt(old_w ** 2 + old_u ** 2)
      # theta = math.atan2(old_w, old_u) + self.angle
      
      # new_w = r * math.sin(theta)
      # new_u = r * math.cos(theta)
      
      # return Point3(old_v * self.v + new_w * self.w + new_u * self.u)
    elif isinstance(t, Ray3):
      return Ray3(transform(t.start), transform(t.dir))
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
      # old_v = t.dot(self.v)
      # old_w = t.dot(self.w)
      # old_u = t.dot(self.u)
      
      # r = math.sqrt(old_w ** 2 + old_u ** 2)
      # theta = math.atan2(old_w, old_u) + self.angle
      
      # new_w = r * math.sin(theta)
      # new_u = r * math.cos(theta)
      
      # return Point3(old_v * self.v + new_w * self.w + new_u * self.u)
    elif isinstance(t, Ray3):
      return Ray3(inv_transform(t.start), inv_transform(t.dir))
    else:
      print t
      raise Exception

