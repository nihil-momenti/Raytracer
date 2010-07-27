require 'geom3'
require 'colour'
require 'illumination'
require 'scene'
require 'shapes'
#from PIL import Image

module RayCaster
    include Geom3, Shapes
    # Define various scene constants
    
    WIN_SIZE = 200                      # Screen window size (square)
    LIGHT_DIR = Vector3.new(2,5,3).unit # The direction vector towards the light source
    LIGHT_INTENS = 0.8                  # Intensity of the single white light source
    AMBIENT = 0.1                       # Ambient light level (assumed white light)
    BACKGROUND = Colour.new(0.6,0.6,0.6)    # Colour of the background
    
    SHINY_RED = Material.new(Colour.new(0.7, 0.3, 0.2), Colour.new(0.4,0.4,0.4), 100)
    SHINY_BLUE = Material.new(Colour.new(0.2, 0.3, 0.7), Colour.new(0.8,0.8,0.8), 200)
    MATT_GREEN = Material.new(Colour.new(0.1, 0.7, 0.1), nil, nil)
    
    # Warning the next three values can't be meaningfully altered until
    # the View.eye_ray method has been rewritten.
    
    EYEPOINT = Point3.new(0.5, 0.5, 2)  # Where the eye is
    LOOKAT = Point3.new(0.5, 0.5, 0)    # The look at point
    FOV = 45                        # Field of view (degrees).
    
    # A View specifies a camera's position and orientation in space, plus its
    # field_of_view (fov) in degrees. It also specifies the required image size
    # (width x height).
    class View
        attr_accessor :eye_point, :look_at, :fov, :width, :height
        # Constructor sets the eye-point, look-at-point and field of view, plus the
        # width and height (in pixels) of the image that will be computed using
        # this view.
        def initialize(eye_point, look_at, fov, width, height)
            @eye_point = eye_point
            @look_at = look_at
            @fov = fov
            @width = width
            @height = height
        end
    
        # The ray from the eye through pixel (col,row) in this view.
        def eye_ray(col, row)
            # This version is a horrible hack that works only for the simple
            # geometry in which the image on the viewplane is the unit square
            # from (0,0,1) to (1,1,1) and the eye is located at some point
            # (0.5, 0.5, eyeZ).
            # And in fact, it's not just a horrible hack. It's an incomplete
            # horrible hack.
            
            spacing = 1.0 / @width  # Pixel spacing
    
            # Compute (x, y) coordinates of pixel on the plane z = 1
            y = (@height - row - 0.5) * spacing
            x = (col + 0.5) * spacing
            
            ray = nil
            # Oops, some code seems to have gone missing here.
    
            return ray
       end
    end
    
    # ======= A Ray Tracing/Ray Casting Camera class ========= 
    # An Camera provides a 'take_photo' method that computes the ray-casting image
    # of a given scene from a given view with given lighting.
    class Camera
        def initialize(view, scene, lighting)
            @view = view
            @scene = scene
            @lighting = lighting
        end
            
        # Return the colour seen looking along the given ray into the current scene
        # with the current lighting.
        def colour_along_ray(ray)
            hitPoint = @scene.intersect(ray)
    
            if hitPoint == nil
                colour = BACKGROUND
            else
                obj, alpha = hitPoint
                colour = obj.material.diffuse_colour
            end
    
            return colour
        end
    
    
        def take_photo()
            #img = Image.new("RGB", (@view.width, @view.height))
            img = []
            (0..@view.height).each do |row|
              img[row] = []
              (0..@view.width).each do |col|
                ray = @view.eye_ray(col, row)
                colour = self.colour_along_ray(ray)
                img[row][col] = colour.intColour()
              end
            end
                    
            return img
        end
    end    
            
    # ====== Main body. Compute and display image ========

    start = Time.now
    lighting = Lighting.new(LIGHT_INTENS, LIGHT_DIR, AMBIENT)
    
    scene = Scene.new([Sphere.new(Point3.new(0.35,0.6,0.5), 0.25, SHINY_BLUE),
                   Sphere.new(Point3.new(0.75,0.2,0.6), 0.15, SHINY_RED),
                   Plane.new(Point3.new(0,0,0), Vector3.new(0,1,0), MATT_GREEN)])
    
    view = View.new(EYEPOINT, LOOKAT, FOV, WIN_SIZE, WIN_SIZE)
    camera = Camera.new(view, scene, lighting)
    
    img = camera.take_photo()
#    img.show()      # Display image in default image-viewer application
    print "Rendering time:", Time.now - start
end
