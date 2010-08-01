from geom3 import Vector3, Point3
from math import sqrt

class Sphere(object):
  '''A ray-traceable sphere'''
  
  def __init__(self, centre, radius, material):
    """Create a sphere with a given centre point, radius
    and surface material"""
    self.centre = centre
    self.radius = radius
    self.material = material


  def normal(self, p):
    """The surface normal at the given point on the sphere"""
    return (p - self.centre).unit()


  def intersect(self, ray):
    """The rays t value of the first intersection point of the
    rays with self, or inf if no intersection occurs.  For each ray."""
    t = float('Inf')

    q = self.centre - ray.start
    vDotQ = ray.dir.dot(q)
    squareDiffs = q.dot(q) - self.radius ** 2
    discrim = vDotQ ** 2 - squareDiffs
    if discrim >= 0:
      root = sqrt(discrim)
      t0 = (vDotQ - root)
      t1 = (vDotQ + root)
      if t0 > 0:
        t = t0
      elif t1 > 0:
        t = t1
      
    return t


  def __repr__(self):
    return "Sphere(%s, %.3f)" % (str(self.centre), self.radius)



class Plane(object):
  '''A ray-traceable plane'''
  
  def __init__(self, point, normal, material):
    """Create a plane through a given point with given normal
    and surface material"""
    self.n = normal.unit()  # Normalise in case caller doesn't
    self.p = point
    self.material = material


  def normal(self, p):
    """The surface normal at the given point"""
    return self.n


  def intersect(self, ray):
    """The ray t value of the first intersection point of the
    ray with self, or None if no intersection occurs"""
    try:
      t = (self.n.dot(self.p - ray.start)) / ray.dir.dot(self.n)
    except ZeroDivisionError:
      t = float('Inf')
    if t > 0:
      return t
    else:
      return float('Inf')


  def __repr__(self):
    return "Plane(%s, %s)" % (str(self.p), str(self.n))
