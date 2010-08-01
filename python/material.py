'''A simplified version of the material class from lab 3 in which
   the illumination is defined by an associated lighting class, which has
   just a directional white light source and a white ambient component'''

from colour import Colour

class Material(object):
  def __init__(self, diffuse_colour, specular_colour = None, shininess = None):
    self.diffuse_colour = diffuse_colour
    self.specular_colour = specular_colour
    self.shininess = shininess


  def lit_colour(self, normal, lighting, view_vector):
    reflection = Colour(0,0,0)
    for light in lighting:
      reflection += self.diffuse_colour * light.diffuseLighting(normal)
    
      if self.shininess is not None:
        reflection += self.specular_colour * (light.specularLighting(normal, view_vector) ** self.shininess)

    return reflection
