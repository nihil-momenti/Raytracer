from geom3 import Vector3, Point3, epsilon
from math import sqrt

class Shape(object):
  def __init__(self, material=None, scene=None):
    self.m = material
    if scene is not None:
      scene.addObject(self)
  
  
  def material(self, point):
    return self.m



class Sphere(Shape):
  def __init__(self, centre, radius, material=None, scene=None):
    super(Sphere,self).__init__(material, scene)
    self.centre = centre
    self.radius = radius
  
  
  def normal(self, p):
    return (p - self.centre).unit()
  
  
  def point_on_surface(self, p):
    return (abs((p - self.centre).length() - self.radius) < epsilon)
  
  
  def point_inside(self, p):
    return ((p - self.centre).length() < self.radius + epsilon)
  
  
  def intersect(self, ray):
    q = self.centre - ray.start
    vDotQ = ray.dir.dot(q)
    squareDiffs = q.dot(q) - self.radius ** 2
    discrim = vDotQ ** 2 - squareDiffs
    if discrim >= 0:
      root = sqrt(discrim)
      t0 = (vDotQ - root)
      t1 = (vDotQ + root)
      return (t0, t1)
    else:
      return (float('Inf'), -float('Inf'))
  
  
  def __repr__(self):
    return "Sphere(%s, %.3f)" % (str(self.centre), self.radius)



class Plane(Shape):
  def __init__(self, point, normal, material=None, scene=None):
    super(Plane,self).__init__(material, scene)
    self.n = normal.unit()
    self.p = point
  
  
  def normal(self, p):
    return self.n
  
  
  def point_on_surface(self, p):
    return (abs((self.p - p).dot(self.n)) < epsilon)
  
  
  def point_inside(self, p):
    return ((self.p - p).dot(self.n) > epsilon)
  
  
  def intersect(self, ray):
    t1 = ray.dir.dot(self.n)
    t2 = (self.n.dot(self.p - ray.start))
    
    if abs(t1) < epsilon:
      if t2 >= 0:
        return (float('Inf'), -float('Inf'))
      else:
        return (-float('Inf'), float('Inf'))
    elif t1 > 0:
      return (-float('Inf'), t2 / t1)
    elif t1 < 0:
      return (t2 / t1, float('Inf'))
    else:
      print self.p, self.n, ray, t1, t2
      raise Exception
    
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
