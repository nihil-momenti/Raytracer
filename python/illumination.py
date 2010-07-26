'''A simplified version of the material class from lab 3 in which
   the illumination is defined by an associated lighting class, which has
   just a directional white light source and a white ambient component'''

from geom3 import dot, unit


class Lighting(object):
    '''In this simple model of scene lighting there is a single directional
       white light source and white ambient light.'''

    def __init__(self, light_intens, light_dir, ambient):
        '''Parameters are the scalar light intensity, the unit vector direction
           to the light source and the scalar ambient light level'''
        self.light_intens = light_intens
        self.light_dir = light_dir
        self.ambient = ambient

        

class Material(object):
    '''A Material is something that can be illuminated by lighting
       to yield a colour. It is assumed that the ambient colour of the
       material is the same as its diffuse colour and there is no
       self-emission.'''
    
    def __init__(self, diffuse_colour, specular_colour = None, shininess = None):
        '''Initialise the diffuse and specular reflectances plus the
        specular highlight exponent.  specular_colour and shininess are
        both None for a purely diffuse surface'''
        self.diffuse_colour = diffuse_colour
        self.specular_colour = specular_colour
        self.shininess = shininess


    def lit_colour(self, normal, lighting, view_vector, shadowed=False):
        '''The RGB colour of this material with the given surface
        normal under the given lighting when viewed from an
        eyepoint in the view_vector direction.'''
        return self.diffuse_colour  # **** IMPLEMENT ME PROPERLY PLEASE ****
