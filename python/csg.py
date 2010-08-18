from shapes import Shape

class CSG(Shape):
  def __init__(self, material=None, scene=None):
    super(CSG,self).__init__(material, scene)
  
  
  def normal(self, p):
    for object in self.objects:
      if object.point_on_surface(p):
        return object.normal(p)
    print self, self.objects, p
    raise Exception


class Intersection(CSG):
  def __init__(self, objects, material=None, scene=None):
    super(Intersection,self).__init__(material, scene)
    self.objects = objects
  
  
  def point_on_surface(self, p):
    value = False
    for object in self.objects:
      if object.point_on_surface(p):
        value = True
      elif object.point_inside(p) is False:
        return False
    
    return value
  
  
  def point_inside(self, p):
    for object in self.objects:
      if object.point_inside(p) is False:
        return False
    
    return True
  
  
  def intersect(self, ray):
    inters = [object.intersect(ray) for object in self.objects]
    
    intersection = reduce(lambda a,b: (max(a[0], b[0]), min(a[1], b[1])), inters)
    
    if (intersection[0] > intersection[1]):
      return (float('Inf'), -float('Inf'))
    else:
      return intersection
