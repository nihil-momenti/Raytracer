from colour import Colour
from geom3 import Ray3

class Material(object):
  def __init__(self, diffuse_colour, specular_colour = None, shininess = None, reflectivity = None, refractivity = None):
    self.diffuse_colour = diffuse_colour
    self.specular_colour = specular_colour
    self.shininess = shininess
    self.casts_shadow = True
    self.reflectivity = reflectivity
    self.refractivity = refractivity


  def lit_colour(self, scene, normal, view_vector, point, n=0):
    reflection = Colour(0,0,0)
    if self.reflectivity is not None and n < 5:
      reflection_vector = 2 * view_vector.dot(normal) * normal - view_vector
      ray = Ray3(point + 0.00001 * reflection_vector, reflection_vector)
      hitpoint = scene.intersect(ray)
      if hitpoint[1] == float('Inf'):
        reflection += self.reflectivity * Colour(0.6,0.6,0.6)
      else:
        (obj, alpha) = hitpoint
        pos = ray.pos(alpha)
        norm = obj.normal(pos)
        reflection += self.reflectivity * obj.material.lit_colour(scene, norm, -ray.dir, pos, n+1)

    if self.refractivity is not None:
      reflection += Colour(0,0,0)

    for light in scene.lighting:
      if self.diffuse_colour is not None:
        reflection += self.diffuse_colour * light.diffuseLighting(normal, point, scene)
    
      if self.shininess is not None:
        reflection += self.specular_colour * (light.specularLighting(normal, view_vector, point, scene) ** self.shininess)

    return reflection
