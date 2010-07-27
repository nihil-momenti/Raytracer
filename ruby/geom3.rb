module Geom3
    Epsilon = 1.0e-10  # Default epsilon for equality testing of points and vectors
    
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
        def initialize(x, y = nil, z = nil)
            if y == nil and z == nil
                @x, @y, @z = x[0], x[1], x[2]
            else
                @x, @y, @z = x, y, z
            end
        end
        
        # P1 - P2 returns a vector. P - v returns a point
        def -(other)
            if other.kind_of? Point3 then return Vector3.new(@x - other.x, @y - other.y, @z - other.z)
            elsif other.kind_of? Vector3 then return Point3.new(@x - other.dx, @y - other.dy, @z - other.dz)
            else raise ArgumentError
            end
        end
        
        # P + v is P translated by v
        def +(other)
            return Point3.new(@x + other.dx, @y + other.dy, @z + other.dz)
        end
    
        # Iterator over the coordinates
        def iter()
            return [@x, @y, @z].iter()
        end
        
        # Equality of points is equality of all coordinates to within epsilon.
        def ==(other)
            return ((@x - other.x).abs() < Epsilon and
                    (@y - other.y).abs() < Epsilon and
                    (@z - other.z).abs() < Epsilon)
        end
    
        # Inequality of points is inequality of any coordinates
        def !=(other)
            return (not (self == other))
        end
        
        # P[i] is x, y, z for i in 0, 1, 2 resp.
        def [](i)
            return [@x, @y, @z][i]
        end
    
        # String representation of a point
        def to_s()
            return ("(%.3f,%.3f,%.3f)" % [@x, @y, @z])
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
        def initialize(dx, dy=nil, dz=nil)
            if dy == nil and dz == nil
                @dx, @dy, @dz = dx[0], dx[1], dx[2]
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
            return Vector3.new(@dx + other.dx, @dy + other.dy, @dz + other.dz)
        end
    
        # v * r for r a float is scaling of vector v by r
        def *(scale)
            return Vector3.new(scale * @dx, scale * @dy, scale * @dz)
        end
    
        # Division of a vector by a float r is scaling by (1/r)
        def /(scale)
            return self * (1.0/scale)
        end
    
        # Negation of a vector is negation of all its coordinates
        def -@()
            return Vector3.new(-@dx, -@dy, -@dz)
        end
    
        # Iterator over coordinates dx, dy, dz in turn
        def iter()
            return [@dx, @dy, @dz].iter()
        end
    
        # v[i] is dx, dy, dz for i in 0,1,2 resp
        def [](i)
            return [@dx, @dy, @dz][i]
        end
    
        # Equality of vectors is equality of all coordinates to within epsilon.
        def ==(other)
            return ((@dx - other.dx).abs < Epsilon and
                    (@dy - other.dy).abs < Epsilon and
                    (@dz - other.dz).abs < Epsilon)
        end
    
        # Inequality of vectors is inequality of any coordinates
        def !=(other)
            return (not (self == other))
        end
        
        # The usual dot product
        def dot(other)
            return @dx*other.dx + @dy*other.dy + @dz*other.dz
        end
    
        # The usual cross product
        def cross(other)
            return Vector3.new(@dy * other.dz - @dz * other.dy,
                          @dz * other.dx - @dx * other.dz,
                          @dx * other.dy - @dy * other.dx) 
        end
    
        # A normalised version of self
        def norm()
            return self/self.length
        end
    
        # Same as 'norm'. Provided for compatibility with Visual
        def unit()
            return norm()
        end
        
        # Minimal string representation in parentheses
        def to_s()
            return '(%.3f,%.3f,%.3f)' % [@dx, @dy, @dz]
        end
    
        # String representation with class included
        def inspect()
            return "Vector3" + self.to_s()
        end
    
        # Length of vector
        def length
            return Math.sqrt(self.dot(self))
        end
        
    end
    
    class ::Fixnum
        # r * v for r an integer is scaling of vector v by r
        alias_method :'old_vector3_times', :'*'
        def *(vector)
            if vector.kind_of? Vector3
                return vector * self
            else
                return self.old_vector3_times(vector)
            end
        end
    end
    
    class ::Float
        # r * v for r a float is scaling of vector v by r
        alias_method :'old_vector3_times', :'*'
        def *(vector)
            if vector.kind_of? Vector3
                return vector * self
            else
                return self.old_vector3_times(vector)
            end
        end
    end
    
    # A Line3 is defined by two points in space
    class Line3
        # Constructor takes two points (or anything convertible to Point3)
        def initialize(p1, p2)
            @p1 = Point3.new(p1)
            @p2 = Point3.new(p2)
        end
            
        # The position p1 + alpha*(p2-p1) on the Line3
        def pos(alpha)
            return @p1 + alpha * (@p2-@p1)
        end
        
        # String representation of a Line3
        def to_s()
            return 'Line3(%.3g, %.3g)' % [p1, p2]
        end
    end
    
    # A Ray3 is a directed Line3, defined by a start point and a direction
    class Ray3
        # Constructor takes a start point (or something convertible to point) and a
        # direction vector.
        def initialize(start, dir)
            @start = Point3.new(start)
            @dir = unit(Vector3.new(dir))
        end
    
        # A point on a Ray3 is start + alpha*dir for alpha positive.
        def pos(alpha)
            if alpha >= 0
                return @start + alpha * @dir
            else
                raise GeomException("Attempt to obtain point not on Ray3")
            end
        end
    
        def inspect()
            return "Ray3(%s,%s)" % [@start, @dir]
        end
    end
    
    #================================================================
    #
    # Simple unit tests if module is run as main
    #
    #================================================================
    if __FILE__ == $0
        def Geom3::assert
            raise "Assertion Failed!" unless yield
        end
        # Simple tests of all basic vector operations
        
        v1 = Vector3.new(1,2,3)
        v2 = Vector3.new(3,2,1)
    #    assert {Vector3.new((1,2,3)) == v1}
        assert {Vector3.new([1,2,3]) == v1}
        assert {Vector3.new(Point3.new(1,2,3)) == v1}
        assert {v1 + v2 == Vector3.new(4,4,4)}
        assert {v1 - v2 == Vector3.new(-2,0,2)}
        assert {v1 * 3 == Vector3.new(3,6,9)}
        assert {3 * v1 == Vector3.new(3,6,9)}
        assert {v1/2.0 == Vector3.new(0.5,1,1.5)}
        assert {-v1 == Vector3.new(-1,-2,-3)}
        assert {v1[0] == 1 and v1[1] == 2 and v1[2] == 3}
    #    assert {list(v1) == [1,2,3]}
        assert {v1.to_s == "(1.000,2.000,3.000)"}
    #    assert {eval(repr(v1)) == v1}
        assert {v1.dot(v2) == 10}
        assert {v1.cross(v2) == Vector3.new(-4,8,-4)}
        assert {Vector3.new(2,3,4).unit.length == 1.0}
        assert {Vector3.new(2,3,4).norm.length == 1.0}
        
        # Tests on points
        
        p1 = Point3.new(2,4,6)
        p2 = Point3.new(4,7,3)
    #    assert {Point3.new((2,4,6)) == p1}
        assert {Point3.new([2,4,6]) == p1}
        assert {Point3.new(Vector3.new(2,4,6)) == p1}
        assert {(0..2).each {|i| p1[i] == [2,4,6][i]}}
        assert {p1-p2 == Vector3.new(-2,-3,3)}
        assert {p1+v1 == Point3.new(3,6,9)}
        assert {p1.to_s == "(2.000,4.000,6.000)"}
    #    assert {eval(repr(p1)) == p1}
    #    try:
    #        p1 + p2
    #        assert {False}
    #    except TypeError: pass
    #    try:
    #        3 * p1
    #        assert {False}
    #    except TypeError: pass
    
        p "Passed all tests"
    end
end
