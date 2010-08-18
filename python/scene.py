from geom3 import Vector3, Point3, unit, dot, cross
from math import sqrt

class Scene(object):
  def __init__(self, objs = [], lighting = []):
    self.objs = objs
    self.lighting = lighting


  def addObject(self, obj):
    self.objs.append(obj)

  def addLight(self, light):
    self.lighting.append(light)


  def intersect(self, ray):
    intersections = [(obj, obj.intersect(ray)[0]) for obj in self.objs]
    
    min = (None, float('Inf'))
    for intersection in intersections:
      if intersection[1] > 0 and intersection[1] < min[1]:
        min = intersection
    
    return min

