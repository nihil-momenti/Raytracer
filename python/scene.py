'''The Ray-tracer's Scene class.

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
        t = {}
        for obj in self.objs :
            intersect = obj.intersect(ray)
            if intersect < float('Inf'):
                t[intersect] = obj
        if len(t) == 0 : return (None, float('Inf'))
        first = min(t)
        return (t[first], first)

