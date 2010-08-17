from geom3 import Vector3, Point3, epsilon
import math
from math import sqrt

class Shape(object):
  def __init__(self, material=None, scene=None):
    self.material = material
    if scene is not None:
      scene.addObject(self)



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



class Cone(Shape):
  def __init__(self, axis, angle, height, material=None, scene=None):
    super(Cone,self).__init__(material, scene)
    self.axis = axis.unit()
    self.angle = math.radians(angle)
    self.cos_angle = math.cos(self.angle)
    self.height = height
    self.cos_2 = self.cos_angle ** 2
    self.tan_angle = math.tan(self.angle)
  
  
  def normal(self, p):
    return ((Vector3(p) - self.axis * (self.axis.dot(Vector3(p)))).unit() + self.tan_angle * self.axis).unit()
  
  
  def point_on_surface(self, p):
    pu_dot_a = Vector3(p).unit().dot(self.axis)
    p_dot_a = Vector3(p).dot(self.axis)
    return abs(pu_dot_a - cos_angle) < epsilon and p_dot_a < self.height
    
  
  
  def point_inside(self, p):
    pu_dot_a = Vector3(p).unit().dot(self.axis)
    p_dot_a = Vector3(p).dot(self.axis)
    return pu_dot_a > 0 and pu_dot_a < cos_angle + epsilon and p_dot_a < self.height
  
  
  def intersect(self, ray):
    v_dot_a = ray.dir.dot(self.axis)
    v_dot_v = ray.dir.dot(ray.dir)
    p_dot_v = Vector3(ray.start).dot(ray.dir)
    p_dot_a = Vector3(ray.start).dot(self.axis)
    p_dot_p = Vector3(ray.start).dot(Vector3(ray.start))

    a = v_dot_a ** 2 - v_dot_v * self.cos_2
    b = 2 * v_dot_a * p_dot_a - 2 * p_dot_v * self.cos_2
    c = p_dot_a ** 2 - p_dot_p * self.cos_2

    

    discrim = b ** 2 - 4* a * c
    if discrim >= 0:
      root = sqrt(discrim)
      t0 = (-b - root) / (2 * a)
      t1 = (-b + root) / (2 * a)
      if Vector3(ray.pos(t0)).dot(self.axis) > self.height:
        return (t0, t0)
      elif Vector3(ray.pos(t1)).dot(self.axis) > self.height:
        return (t1, t1)
      else:
        return (t0, t1)
    else:
      return (float('Inf'), -float('Inf'))


  def __repr__(self):
    return "Cone(%s, %s, %s)" % (str(self.axis), str(math.degrees(self.angle)), str(self.height))
