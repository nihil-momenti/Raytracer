require 'geom3'

module Shapes
   include Geom3 

  # An abstract base class for all shapes.
  class Shape
      attr_accessor :material
      # Set the material for the shape.
      def initialize(material)
          @material = material
      end
  
      # The ray t value of the first intersection point of the
      # ray with self, or nil if no intersection occurs
      def intersect(ray)
          # Must be overriden be subclasses
      end
  
      # The surface normal at the given point on the shape
      def normal(p)
          # Must be overriden by subclasses
      end
  end
  
  # A ray-traceable sphere
  class Sphere < Shape
      # Create a sphere with a given centre point, radius
      # and surface material
      def initialize(centre, radius, material)
          super(material)
          @centre = centre
          @radius = radius
      end
  
  
      # The surface normal at the given point on the sphere
      def normal(p)
          return (p - @centre).unit
      end
  
  
      # The ray t value of the first intersection point of the
      # ray with self, or nil if no intersection occurs
      def intersect(ray)
          t = nil
          q = @centre - ray.start
          vDotQ = ray.dir.dot(q)
          squareDiffs = q.dot(q) - @radius**2
          discrim = vDotQ * vDotQ - squareDiffs
          if discrim >= 0
              root = Math.sqrt(discrim)
              t0 = (vDotQ - root)
              t1 = (vDotQ + root)
              if t0 > 0
                  t = t0
              elsif t1 > 0
                  t = t1
              end
          end
          return t
      end
  
      def inspect()
          return "Sphere(%s, %.3f)" % [@centre, @radius]
      end
  end
  
  
  
  # A ray-traceable plane
  class Plane < Shape   
      # Create a plane through a given point with given normal
      # and surface material
      def initialize(point, normal, material)
          super(material)
          @n = normal.unit # Normalise in case caller doesn't
          @p = point
      end
  
  
      # The surface normal at the given point
      def normal(p)
          return nil   # FIX ME
      end
  
  
      # The ray t value of the first intersection point of the
      # ray with self, or nil if no intersection occurs
      def intersect(ray)
          return nil # FIX ME !!
      end
  
      def inspect()
          return "Plane(%s, %s)" % [@p, @n]
      end
  end
end
