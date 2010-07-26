'''The Ray-tracer's Scene class and associated geometric objects.

Written for COSC363.
@author Richard Lobb
@version July 2010.'''

from geom3 import Vector3, Point3, unit, dot, cross
from math import sqrt

class Scene(object):
    '''A scene is a list of ray-traceable objects. It provides an intersect
       method to intersect a ray with the scene, returning the 't'
       value (distance along the ray) at the first hit, plus
       the object hit, in a pair.'''

    def __init__(self, objs = []):
        """Constructor takes a list of scene objects, each of which
        must provide an 'intersect' method that returns the ray t
        value or None of the first intersection between the ray and
        the object"""
        self.objs = objs


    def addObject(self, obj):
        """Add a new object to the list of objects"""
        self.objs.append(obj)


    def intersect(self, ray):
        """Intersect the given ray with all objects in the scene,
        returning the pair (obj, t) of the first object hit or 
        None if there are no hits"""

        # *** FIX ME! ***
        t = self.objs[0].intersect(ray)
        return None if t is None else (objs[0], t)



class Sphere(object):
    '''A ray-traceable sphere'''
    
    def __init__(self, centre, radius, material):
        """Create a sphere with a given centre point, radius
        and surface material"""
        self.centre = centre
        self.radius = radius
        self.material = material


    def normal(self, p):
        """The surface normal at the given point on the sphere"""
        return unit(p - self.centre)


    def intersect(self, ray):
        """The ray t value of the first intersection point of the
        ray with self, or None if no intersection occurs"""
        t = None
        q = self.centre - ray.start
        vDotQ = dot(ray.dir, q)
        squareDiffs = dot(q, q) - self.radius*self.radius
        discrim = vDotQ * vDotQ - squareDiffs
        if discrim >= 0:
            root = sqrt(discrim)
            t0 = (vDotQ - root)
            t1 = (vDotQ + root)
            if t0 > 0:
                t = t0
            elif t1 > 0:
                t = t1
        return t
    

    def __repr__(self):
        return "Sphere(%s, %.3f)" % (str(self.centre), self.radius)



class Plane(object):
    '''A ray-traceable plane'''
    
    def __init__(self, point, normal, material):
        """Create a plane through a given point with given normal
        and surface material"""
        self.n = unit(normal)  # Normalise in case caller doesn't
        self.p = point
        self.material = material


    def normal(self, p):
        """The surface normal at the given point"""
        return None   # FIX ME


    def intersect(self, ray):
        """The ray t value of the first intersection point of the
        ray with self, or None if no intersection occurs"""
        
        return None # FIX ME !!
    

    def __repr__(self):
        return "Plane(%s, %s)" % (str(self.p), str(self.n))
