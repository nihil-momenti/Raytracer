from geom3 import Vector3, Point3
from math import sqrt

class Sphere(object):
  def __init__(self, centre, radius, material, scene=None):
    """Create a sphere with a given centre point, radius
    and surface material"""
    self.centre = centre
    self.radius = radius
    self.material = material
    if scene is not None:
      scene.addObject(self)


  def normal(self, p):
    return (p - self.centre).unit()


  def intersect(self, ray):
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
  def __init__(self, point, normal, material, scene=None):
    self.n = normal.unit()
    self.p = point
    self.material = material
    if scene is not None:
      scene.addObject(self)


  def normal(self, p):
    return self.n


  def intersect(self, ray):
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

class CSG(object):
  def __init__(self, planes, material, scene=None):
    self.planes = planes
    self.material = material
    if scene is not None:
      scene.addObject(self)

  def normal(self, point):
    for plane in self.planes:
      if ((plane.p - point).dot(plane.n) == 0):
        return plane.n
    
    
  def intersect(self, ray):
    intersections = [plane.intersect(ray) for plane in self.planes]
    return min(intersections)
