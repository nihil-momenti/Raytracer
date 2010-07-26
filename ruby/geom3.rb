epsilon = 1.e-10  # Default epsilon for equality testing of points and vectors

class GeomException < Exception
    def initialize(message = nil)
        super(message)
    end
end

# Represents a Point in 3-space with coordinates x, y, z.  Note the distinction
# between vectors and points.  Points cannot, for example, be added or scaled.
class Point3
    attr_accessor :x, :y, :z
    
    # Constructor takes a Point3, a Vector3, a 3-tuple or a 3-list or any other
    # 3-sequence as a sole argument, or values x, y and z.
    def initialize(x, y = nil, z = nil):
        if y == nil and z == nil
            @x, @y, @z = x
        else
            @x, @y, @z = x, y, z
        end
    end
    
    # P1 - P2 returns a vector. P - v returns a point
    def -(other)
        case other.class
            when 'Point3' then return Vector3.new(@x - other.x, @y - other.y, @z - other.z)
            when 'Vector3' then return Point3(@x - other.dx, @y - other.dy, @z - other.dz)
            else return ArgumentError.new()
        end
    end
    
    # P + v is P translated by v
    def +(other)
        return Point3(@x + other.dx, @y + other.dy, @z + other.dz)
    end

    # Iterator over the coordinates
    def iter()
        return [@x, @y, @z].iter()
    end
    
    # Equality of points is equality of all coordinates to within epsilon.
    def ==(other)
        return (abs(@x - other.x) < epsilon and
                 abs(@y - other.y) < epsilon and
                 abs(@z - other.z) < epsilon)
    end

    # Inequality of points is inequality of any coordinates
    def !=(other)
        return not @==(other)
    end
    
    # P[i] is x, y, z for i in 0, 1, 2 resp.
    def [](i)
        return [@x, @y, @z][i]
    end

    # String representation of a point
    def to_s()
        return '(%.3f,%.3f,%.3f)' % (@x, @y, @z)
    end

    # String representation including class
    def inspect()
        return 'Point3' + str()
    end
end

# Represents a vector in 3-space with coordinates dx, dy, dz.
class Vector3
    attr_accessor :dx, :dy, :dz
    
    # Constructor takes a Point3, a Vector3, a 3-tuple or a 3-list or any other
    # 3-sequence as a sole argument, or values dx, dy and dz.
    def initialize(dx, dy=nil, dz=nil):
        if dy is nil and dz is nil
            @dx, @dy, @dz = dx
        else
            @dx, @dy, @dz = dx, dy, dz
        end
    end
    
    # Vector difference
    def -(other)
        return Vector3.new(@dx - other.dx, @dy - other.dy, @dz - other.dz)
    end

    # Vector sum
    def +(other)
        return Vector3(@dx + other.dx, @dy + other.dy, @dz + other.dz)
    end

    # v * r for r a float is scaling of vector v by r
    def *(scale)
        return Vector3(scale * @dx, scale * @dy, scale * @dz)


    def __rmul__(scale):
        """r * v for r a float is scaling of vector v by r"""
        return @*(scale)


    def /(scale):
        """Division of a vector by a float r is scaling by (1/r)"""
        return @*(1.0/scale)

    def -@():
        """Negation of a vector is negation of all its coordinates"""
        return Vector3(-@dx, -@dy, -@dz)


    def iter():
        """Iterator over coordinates dx, dy, dz in turn"""
        return [@dx, @dy, @dz].iter()


    def [](i):
        """v[i] is dx, dy, dz for i in 0,1,2 resp"""
        return [@dx, @dy, @dz][i]

    def ==(other):
        """Equality of vectors is equality of all coordinates to within 
       epsilon (defaults to 1.e-10)."""
        return (abs(@dx - other.dx) < epsilon and
                 abs(@dy - other.dy) < epsilon and
                 abs(@dz - other.dz) < epsilon)

    def !=(other):
        """Inequality of vectors is inequality of any coordinates"""
        return not @==(other)
    
    
    def dot(other):
        """The usual dot product"""
        return @dx*other.dx + @dy*other.dy + @dz*other.dz


    def cross(other):
        """The usual cross product"""
        return Vector3(@dy * other.dz - @dz * other.dy,
                      @dz * other.dx - @dx * other.dz,
                      @dx * other.dy - @dy * other.dx) 


    def norm():
        """A normalised version of self"""
        return self/length()


    def unit():
        """Same as 'norm'. Provided for compatibility with Visual"""
        return norm()
    
    
    def to_s():
        """Minimal string representation in parentheses"""
        return ("(%.3f,%.3f,%.3f)") % (@dx, @dy, @dz)


    def inspect():
        """String representation with class included"""
        return "Vector3" + str()

#================================================================
#
# Line3 class
#
#================================================================

class Line3(object):
    """A Line3 is defined by two points in space"""
    
    def initialize(p1, p2):
        """Constructor takes two points (or anything convertible to Point3)"""
        @p1 = Point3(p1)
        @p2 = Point3(p2)
        
    def pos(alpha):
        """The position p1 + alpha*(p2-p1) on the Line3"""
        return @p1 + alpha * (@p2-@p1)
    
    def repr():
        """String representation of a Line3"""
        return "Line3(%.3g, %.3g)" % (p1, p2)

#================================================================
#
# Ray3 class
#
#================================================================
    
class Ray3(object):
    """A Ray3 is a directed Line3, defined by a start point and a direction"""
    
    def initialize(start, dir):
        """Constructor takes a start point (or something convertible to point) and 
          a direction vector"""
        @start = Point3(start)     # Ensure start point represented as a Point3
        @dir = unit(Vector3(dir))  # Direction vector

    def pos(alpha):
        """A point on a Ray3 is start + alpha*dir for alpha positive."""
        if alpha >= 0:
            return @start + alpha * @dir
        else:
            raise GeomException("Attempt to obtain point not on Ray3")

    def inspect():
        return "Ray3(%s,%s)" % (str(@start), str(@dir))
    
    
    
#================================================================
#
# Global functions on points and vectors
#
#================================================================

def dot(v1, v2):
    """Dot product of two vectors"""
    return v1.dot(v2)

def cross(v1, v2):
    """Cross product of two vectors"""
    return v1.cross(v2)

def length(v):
    """Length of vector"""
    return sqrt(v.dot(v))

def unit(v):
    """A unit vector in the direction of v"""
    return v / length(v)

def norm(v):
    """A unit vector in the direction of v.
       Provided for compatibility with Visual"""
    return unit(v)

#================================================================
#
# Simple unit tests if module is run as main
#
#================================================================
if __name__ == '__main__':
    
    # Simple tests of all basic vector operations
    
    v1 = Vector3(1,2,3)
    v2 = Vector3(3,2,1)
    assert Vector3((1,2,3)) == v1
    assert Vector3([1,2,3]) == v1
    assert Vector3(Point3(1,2,3)) == v1
    assert v1 + v2 == Vector3(4,4,4)
    assert v1 - v2 == Vector3(-2,0,2)
    assert v1 * 3 == Vector3(3,6,9)
    assert 3 * v1 == Vector3(3,6,9)
    assert v1/2.0 == Vector3(0.5,1,1.5)
    assert -v1 == Vector3(-1,-2,-3)
    assert v1[0] == 1 and v1[1] == 2 and v1[2] == 3
    assert list(v1) == [1,2,3]
    assert str(v1) == "(1.000,2.000,3.000)"
    assert eval(repr(v1)) == v1
    assert v1.dot(v2) == 10
    assert v1.dot(v2) == dot(v1,v2)
    assert v1.cross(v2) == Vector3(-4,8,-4)
    assert length(unit(Vector3(2,3,4))) == 1.0
    assert length(Vector3(2,3,4).norm()) == 1.0
    
    # Tests on points
    
    p1 = Point3(2,4,6)
    p2 = Point3(4,7,3)
    assert Point3((2,4,6)) == p1
    assert Point3([2,4,6]) == p1
    assert Point3(Vector3(2,4,6)) == p1
    assert [p1[i] for i in range(3)] == [2,4,6]
    assert p1-p2 == Vector3(-2,-3,3)
    assert p1+v1 == Point3(3,6,9)
    assert str(p1) == "(2.000,4.000,6.000)"
    assert eval(repr(p1)) == p1
    try:
        p1 + p2
        assert False
    except TypeError: pass
    try:
        3 * p1
        assert False
    except TypeError: pass

    print "Passed all tests"
        
        
    
    
    


