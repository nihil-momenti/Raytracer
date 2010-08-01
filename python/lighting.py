from colour import Colour

class AmbientLight(object):
  def __init__(self, value):
    self.value = value

  def specularLighting(self, normal, view_vector):
    return 0.0

  def diffuseLighting(self, normal):
    return self.value
    
class DirectionalLight(object):
  def __init__(self, value, direction):
    self.value = value
    self.direction = direction.unit()

  def specularLighting(self, normal, view_vector):
    h = (self.direction + view_vector).unit()
    return max(0, h.dot(normal))

  def diffuseLighting(self, normal):
    return self.value * max(0, self.direction.dot(normal))


class PointLight(object):
  def __init__(self, value, point):
    self.value = value
    self.point = point

  def specularLighting(self, normal, view_vector):
    return Colour(0,0,0)

  def diffuseLighting(self, normal):
    return Colour(0,0,0)


class FocusedLight(object):
  def __init__(self, value, point, direction, spread):
    self.value = value
    self.point = point
    self.direction = direction.unit()
    self.spread = spread

  def specularLighting(self, normal):
    return Colour(0,0,0)

  def diffuseLighting(self, normal):
    return Colour(0,0,0)

