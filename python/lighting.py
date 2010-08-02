from colour import Colour

class AmbientLight(object):
  def __init__(self, value):
    self.value = value

  def specularLighting(self, normal, view_vector, point):
    return Colour(0,0,0)

  def diffuseLighting(self, normal, point):
    return self.value
    
class DirectionalLight(object):
  def __init__(self, value, direction):
    self.value = value
    self.direction = direction.unit()

  def specularLighting(self, normal, view_vector, point):
    h = (self.direction + view_vector.unit()).unit()
    return self.value * max(0, h.dot(normal))

  def diffuseLighting(self, normal, point):
    return self.value * max(0, self.direction.dot(normal))


class PointLight(object):
  def __init__(self, value, point):
    self.value = value
    self.point = point

  def specularLighting(self, normal, view_vector, point):
    direction = self.point - point
    direction = direction / abs(direction.length())
    h = (direction + view_vector.unit()).unit()
    return self.value * max(0, h.dot(normal))

  def diffuseLighting(self, normal, point):
    direction = self.point - point
    direction = direction / abs(direction.length())
    return self.value * max(0, direction.dot(normal))


class FocusedLight(object):
  def __init__(self, value, point, direction, spread):
    self.value = value
    self.point = point
    self.direction = -direction.unit()
    self.spread = spread

  def specularLighting(self, normal, view_vector, point):
    direction = (self.point - point)
    direction = direction / abs(direction.length())
    multiplier = max(0, direction.dot(self.direction)) ** self.spread
    h = (direction + view_vector.unit()).unit()
    return self.value * multiplier * max(0, h.dot(normal))

  def diffuseLighting(self, normal, point):
    direction = (self.point - point)
    direction = direction / abs(direction.length())
    multiplier = max(0, direction.dot(self.direction)) ** self.spread
    return self.value * multiplier * max(0, direction.dot(normal))

