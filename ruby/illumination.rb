# A simplified version of the material class from lab 3 in which
# the illumination is defined by an associated lighting class, which has
# just a directional white light source and a white ambient component'''

require 'geom3'

# In this simple model of scene lighting there is a single directional white
# light source and white ambient light.
class Lighting
    attr_accessor :light_intens, :light_dir, :ambient

    # Parameters are the scalar light intensity, the unit vector direction to
    # the light source and the scalar ambient light level
    def initialize(light_intens, light_dir, ambient)
        @light_intens = light_intens
        @light_dir = light_dir
        @ambient = ambient
    end
end

        
# A Material is something that can be illuminated by lighting to yield a colour.
# It is assumed that the ambient colour of the material is the same as its
# diffuse colour and there is no self-emission.
class Material
    attr_accessor :diffuse_colour, :specular_colour, :shininess

    # Initialise the diffuse and specular reflectances plus the specular
    # highlight exponent.  specular_colour and shininess are both None for a
    # purely diffuse surface
    def initalize(diffuse_colour, specular_colour = nil, shininess = nil)
        @diffuse_colour = diffuse_colour
        @specular_colour = specular_colour
        @shininess = shininess
    end

    # The RGB colour of this material with the given surface normal under the
    # given lighting when viewed from an eyepoint in the view_vector direction.
    def lit_colour(normal, lighting, view_vector, shadowed=False)
        return self.diffuse_colour  # **** IMPLEMENT ME PROPERLY PLEASE ****
    end
end
