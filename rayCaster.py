from geom3 import Point3, Vector3, Ray3, cross, dot, unit, length
from math import sqrt, tan, atan, degrees
from geom3 import Point3, Vector3, Ray3, unit
from colour import Colour
from PIL import Image
from illumination import Lighting, Material
from scene import Scene, Sphere, Plane
from datetime import datetime


# Define various scene constants

WIN_SIZE = 200                      # Screen window size (square)
LIGHT_DIR = unit(Vector3(2,5,3))    # The direction vector towards the light source
LIGHT_INTENS = 0.8                  # Intensity of the single white light source
AMBIENT = 0.1                       # Ambient light level (assumed white light)
BACKGROUND = Colour(0.6,0.6,0.6)    # Colour of the background

SHINY_RED = Material(Colour(0.7, 0.3, 0.2), Colour(0.4,0.4,0.4), 100)
SHINY_BLUE = Material(Colour(0.2, 0.3, 0.7), Colour(0.8,0.8,0.8), 200)
MATT_GREEN = Material(Colour(0.1, 0.7, 0.1), None, None)

# Warning the next three values can't be meaningfully altered until
# the View.eye_ray method has been rewritten.

EYEPOINT = Point3(0.5, 0.5, 2)  # Where the eye is
LOOKAT = Point3(0.5, 0.5, 0)    # The look at point
FOV = 45                        # Field of view (degrees).


class View(object):
    '''A View specifies a camera's position and orientation in space,
       plus its field_of_view (fov) in degrees. It also specifies the
       required image size (width x height).'''

    
    def __init__(self, eye_point, look_at, fov, width, height):
        '''Constructor sets the eye-point, look-at-point and field of view,
           plus the width and height (in pixels) of the image that will
           be computed using this view.'''
        
        self.eye_point = eye_point
        self.look_at = look_at
        self.fov = fov
        self.width = width
        self.height = height

        
    def eye_ray(self, col, row):
        '''The ray from the eye through pixel (col,row) in this view.'''

        # This version is a horrible hack that works only for the simple
        # geometry in which the image on the viewplane is the unit square
        # from (0,0,1) to (1,1,1) and the eye is located at some point
        # (0.5, 0.5, eyeZ).
        # And in fact, it's not just a horrible hack. It's an incomplete
        # horrible hack.
        
        spacing = 1.0 / self.width  # Pixel spacing

        # Compute (x, y) coordinates of pixel on the plane z = 1
        y = (self.height - row - 0.5) * spacing
        x = (col + 0.5) * spacing

        # Oops, some code seems to have gone missing here.

        return ray

    

# ======= A Ray Tracing/Ray Casting Camera class ========= 

class Camera(object):
    '''An Camera provides a 'take_photo' method that computes the ray-casting 
       image of a given scene from a given view with given lighting.'''

    def __init__(self, view, scene, lighting):
        self.view = view
        self.scene = scene
        self.lighting = lighting
        

    def colour_along_ray(self, ray):
        """Return the colour seen looking along the given ray into the
           current scene with the current lighting."""
        
        hitPoint = self.scene.intersect(ray)

        if hitPoint is None:
            colour = BACKGROUND
        else:
            (obj, alpha) = hitPoint
            colour = obj.material.diffuse_colour

        return colour


    def take_photo(self):
        img = Image.new("RGB", (self.view.width, self.view.height))
        
        for row in range(self.view.height):
            for col in range(self.view.width):
                ray = self.view.eye_ray(col, row)
                colour = self.colour_along_ray(ray)
                img.putpixel((col, row), colour.intColour())
                
        return img

        
# ====== Main body. Compute and display image ========

start = datetime.now()
lighting = Lighting(LIGHT_INTENS, LIGHT_DIR, AMBIENT)

scene = Scene([Sphere(Point3(0.35,0.6,0.5), 0.25, SHINY_BLUE),
               Sphere(Point3(0.75,0.2,0.6), 0.15, SHINY_RED),
               Plane(Point3(0,0,0), Vector3(0,1,0), MATT_GREEN)])

view = View(EYEPOINT, LOOKAT, FOV, WIN_SIZE, WIN_SIZE)
camera = Camera(view, scene, lighting)

img = camera.take_photo()
img.show()      # Display image in default image-viewer application
print "Rendering time:", datetime.now() - start
