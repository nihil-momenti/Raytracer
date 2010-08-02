from geom3 import Vector3, Point3, unit, dot, cross
from math import sqrt

class Scene(object):
    def __init__(self, objs = []):
        self.objs = objs


    def addObject(self, obj):
        self.objs.append(obj)


    def intersect(self, ray):
        t = {}
        for obj in self.objs :
            intersect = obj.intersect(ray)
            if intersect < float('Inf'):
                t[intersect] = obj
        if len(t) == 0 : return (None, float('Inf'))
        first = min(t)
        return (t[first], first)

