from geom3 import Vector3, Point3
from math import sqrt

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
        return (p - self.centre).unit()


    def intersect(self, ray):
        """The rays t value of the first intersection point of the
        rays with self, or inf if no intersection occurs.  For each ray."""
        t = float('Inf')

        q = self.centre - ray.start
        vDotQ = ray.dir.dot(q)
        squareDiffs = q.dot(q) - self.radius ** 2
        discrim = vDotQ ** 2 - squareDiffs
        if discrim >= 0:
            root = sqrt(discrim)
            t0 = (vDotQ - root)
            t1 = (vDotQ + root)
            if t0 > 0:
                t = t0
            elif t1 > 0:
                t = t1
            
        return t

    def intersectMultiple(self, rays):
        t = []
        for ray in rays:
            q = self.centre - ray.start
            vDotQ = ray.dir.dot(q)
            squareDiffs = q.dot(q) - self.radius ** 2
            discrim = vDotQ ** 2 - squareDiffs
            if discrim >= 0:
                root = sqrt(discrim)
                t0 = (vDotQ - root)
                t1 = (vDotQ + root)
                if t0 > 0:
                    t.append(t0)
                elif t1 > 0:
                    t.append(t1)
                else:
                    t.append(float('Inf'))
            else:
                t.append(float('Inf'))
        return t
    

    def __repr__(self):
        return "Sphere(%s, %.3f)" % (str(self.centre), self.radius)



class Plane(object):
    '''A ray-traceable plane'''
    
    def __init__(self, point, normal, material):
        """Create a plane through a given point with given normal
        and surface material"""
        self.n = normal.unit()  # Normalise in case caller doesn't
        self.p = point
        self.material = material


    def normal(self, p):
        """The surface normal at the given point"""
        return None   # FIX ME


    def intersect(self, ray):
        """The ray t value of the first intersection point of the
        ray with self, or None if no intersection occurs"""
        
        return float('Inf') # FIX ME !!

    def intersectMultiple(self, rays):
        return map(self.intersect, rays)
    

    def __repr__(self):
        return "Plane(%s, %s)" % (str(self.p), str(self.n))
