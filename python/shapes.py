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
  def __init__(self, point, normal, material=None, scene=None):
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



class CSGPlane(object):
  def __init__(self, point, normal):
    self.n = normal.unit()
    self.p = point


  def intersect(self, ray):
    t1 = ray.dir.dot(self.n) # positive if ray is heading in the same direction as the plane normal
    t2 = (self.n.dot(self.p - ray.start)) # negative if initial point on norm side of plane
    # print self.n, ray.dir, t1, t2
    
    if t1 < 0 and t2 < 0:
      return ('outwards', t2 / t1)
    elif t1 > 0 and t2 > 0:
      return ('inwards', t2 / t1)
    elif t1 < 0 and t2 >= 0:
      return ('outside', float('Inf'))
    elif t1 > 0 and t2 <= 0:
      return ('inside', float('Inf'))
    else:
      print self.p, self.n, ray, t1, t2
      raise Exception



class CSG(object):
  def __init__(self, planes, material, scene=None):
    self.planes = planes
    self.material = material
    if scene is not None:
      scene.addObject(self)

  def normal(self, point):
    for plane in self.planes:
      if ((plane.p - point).dot(plane.n) < 0.00001):
        return -plane.n
    
    
  def intersect(self, ray):
    inters = [plane.intersect(ray) for plane in self.planes]
    #print inters

    inters.sort(key=lambda intersection:intersection[1])
    
    if reduce(lambda a,b: a or b[0] == 'outside', inters, False):
      return float('Inf')
    
    inters = filter(lambda inter: inter[1] != float('Inf'), inters)
    inters.append(None) # Sentinel
    inters.reverse()
    
    #print inters
    
    if inters[-1] is None or inters[-1][0] == 'outwards':
      return float('Inf')
    
    while inters[-2] is not None and inters[-2][0] == 'inwards':
      inters.pop()

    if inters[-1] is None:
      return float('Inf')

    inter = inters.pop()

    while inters[-1] is not None and inters[-1][0] == 'outwards':
      inters.pop()

    if inters[-1] is not None and inters[-1][0] == 'inwards':
      return float('Inf')

    return inter[1]
