# The Colour class, a class to represent an RGB colour
# supporting addition, scaling by a scalar and modulation
# (component-wise multiplication).

# Written for COSC 363.
# @author Richard Lobb
# @version July 2010.

# Last year I provided modulation by an overloaded multiply operator
# but that seemed to cause confusion. Let's see what happens this year.

# Represents a colour as an RGB triple of floats, usually in the range 0 - 1.
# Can be multiplied by a scalar or modulated by another colour (which is
# componentwise multiplication).
class Colour
    attr_accessor :r, :g, :b

    # Initialiser, given either a single parameter that's a sequence of red,
    # green and blue components or three scalar R, G and B values
    def initialize(r, g, b)
        @r = r
        @g = g
        @b = b
    end

    # Modulate this colour by another, i.e., return a new colour obtained by
    # component-wise multiplication of self by other
    def modulate(other)
        return Colour.new(@r * other.r, @g * other.g, @b * other.b)
    end

    # Multiplication operator: colour * scalar, colour * otherColour
    def *(factor)
        if factor.kind_of? Float then return Colour.new(@r * factor, @g * factor, @b * factor)
        elsif factor.kind_of? Fixnum then return Colour.new(@r * factor, @g * factor, @b * factor)
        elsif factor.kind_of? Colour then return self.modulate(factor)
        else raise ArgumentError
        end
    end

    # Division by a scale factor
    def /(divisor)
        div = Float(divisor) 
        return Colour.new(@r / div, @g / div, @b / div)
    end

    # Plus operator for two colours
    def +(other)
        return Colour.new(@r + other.r, @g + other.g, @b + other.b)
    end

    # Return an RGB triple of self's RGB components, each multiplied by 256
    # and clamped to the range 0..255
    def intColour()
        return [Colour.toInt(@r), Colour.toInt(@g), Colour.toInt(@b)]
    end
 
    # The string representation of self
    def inspect()
        return "Colour(%f,%f,%f)"  % [@r, @g, @b]
    end

    # Support function: convert a colour component in the range 0 - 1 to the range
    # 0 .. 255.
    def self.toInt(floatVal)
        return [0, [255, (256.0 * floatVal).to_i].min].max
    end
end

class Fixnum
    # Multiplication operator: scalar * colour
    alias_method :old_colour_times, :'*'
    def *(factor)
        if (factor.kind_of?(Colour))
            return factor * self
        else
            return self.old_colour_times(factor)
        end
    end
end

class Float
    # Multiplication operator: scalar * colour
    alias_method :old_colour_times, :'*'
    def *(factor)
        if (factor.kind_of?(Colour))
            return factor * self
        else
            return self.old_colour_times(factor)
        end
    end
end

# Demo code to run if this file is run directly rather than just being imported.

if __FILE__ == $0
    colourA = Colour.new(0.5, 0.2, 0.5)
    p "colourA:", colourA
    colourB = 0.5 * colourA
    p "colourB = 0.5 * colourA:", colourB
    p "colourA * 0.5", (colourA * 0.5)
    p "colourA / 2:", (colourA / 2)
    reflectance = Colour.new(1, 0.5, 0.2)
    p "reflectance:", reflectance
    p "colourB * reflectance", colourB * reflectance
    p "colourB.modulate(reflectance)", colourB.modulate(reflectance)
    colourA += colourB
    p "After adding in colourB, colourA is: ", colourA
    p "In (0..255) ints, colour A is:", colourA.intColour()
end
