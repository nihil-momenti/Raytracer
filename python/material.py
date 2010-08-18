from colour import Colour
from geom3 import Ray3

class Material(object):
  def __init__(self, diffuse_colour, specular_colour = None, shininess = None, reflectivity = None, refractivity = None):
    self.d_colour = diffuse_colour
    self.s_colour = specular_colour
    self.shininess = shininess
    self.casts_shadow = True
    self.reflectivity = reflectivity
    self.refractivity = refractivity


  def diffuse_colour(self, point, normal):
    if self.d_colour is not None:
      return self.d_colour
    else:
      return Colour(0,0,0)


  def specular_colour(self, point, normal):
    if self.s_colour is not None:
      return self.s_colour
    else:
      return Colour(0,0,0)


  def reflection(self, scene,  normal, view_vector, point, n):
    if self.reflectivity is not None and n < 5:
      reflection_vector = 2 * view_vector.dot(normal) * normal - view_vector
      ray = Ray3(point, reflection_vector)
      hitpoint = scene.intersect(ray)
      if hitpoint[1] == float('Inf'):
        return self.reflectivity * Colour(0.6,0.6,0.6)
      else:
        (obj, alpha) = hitpoint
        pos = ray.pos(alpha)
        norm = obj.normal(pos)
        return self.reflectivity * obj.material.lit_colour(scene, norm, -ray.dir, pos, n+1)
    else:
      return Colour(0,0,0)


  def refraction(self):
    if self.refractivity is not None:
      return Colour(0,0,0)
    else:
      return Colour(0,0,0)


  def diffuse(self, point, normal, scene, light):
    return self.diffuse_colour(point, normal) * light.diffuseLighting(normal, point, scene)


  def specular(self, point, normal, scene, view_vector, light):
    if self.shininess is not None:
      return self.specular_colour(point, normal) * (light.specularLighting(normal, view_vector, point, scene) ** self.shininess)
    else:
      return Colour(0,0,0)


  def lit_colour(self, scene, normal, view_vector, point, n=0):
    reflection = Colour(0,0,0)

    reflection += self.reflection(scene, normal, view_vector, point, n)
    reflection += self.refraction()
    for light in scene.lighting:
      reflection += self.diffuse(point, normal, scene, light)
      reflection += self.specular(point, normal, scene, view_vector, light)

    return reflection
