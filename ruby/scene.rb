# The Ray-tracer's Scene class and associated geometric objects.
#
# Written for COSC363.
# @author Richard Lobb
# @version July 2010.

require 'geom3'

from geom3 import Vector3, Point3, unit, dot, cross
from math import sqrt

# A scene is a list of ray-traceable objects. It provides an intersect
# method to intersect a ray with the scene, returning the 't'
# value (distance along the ray) at the first hit, plus
# the object hit, in a pair.
class Scene
    # Constructor takes a list of scene objects, each of which
    # must provide an 'intersect' method that returns the ray t
    # value or None of the first intersection between the ray and
    # the object
    def initialize(objs = [])
        @objs = objs
    end


    # Add a new object to the list of objects
    def addObject(obj)
        @objs.append(obj)
    end


    # Intersect the given ray with all objects in the scene,
    # returning the pair (obj, t) of the first object hit or 
    # None if there are no hits
    def intersect(ray)
        # *** FIX ME! ***
        t = @objs[0].intersect(ray)
        return None if t is None else (objs[0], t)
    end
end
