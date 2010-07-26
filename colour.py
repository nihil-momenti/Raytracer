# The Colour class, a class to represent an RGB colour
# supporting addition, scaling by a scalar and modulation
# (component-wise multiplication).

# Written for COSC 363.
# @author Richard Lobb
# @version July 2010.

# Last year I provided modulation by an overloaded multiply operator
# but that seemed to cause confusion. Let's see what happens this year.

def toInt(floatVal):
    """Support function: convert a colour component in the range 0 - 1
    to the range 0 .. 255."""
    return max(0, min(255, int(256.0 * floatVal)))


class Colour(object):
    """Represents a colour as an RGB triple of floats, usually in the range 0 - 1.
    Can be multiplied by a scalar or modulated by another colour (which
    is componentwise multiplication)."""

    def __init__(self, r, g, b):
        """Initialiser, given either a single parameter that's a sequence of red,
        green and blue components or three scalar R, G and B values"""
        self.r = r
        self.g = g
        self.b = b


    def modulate(self, other):
        """Modulate this colour by another, i.e., return a new colour
           obtained by component-wise multiplication of self by other"""
        return Colour(self.r * other.r, self.g * other.g, self.b * other.b)


    def __mul__(self, factor):
        """Multiplication operator: colour * scalar"""
        f = float(factor)   # Make sure the other operand is a float (or convertible to one)
        return Colour(self.r * f, self.g * f, self.b * f)


    def __div__(self, divisor):
        """Division by a scale factor"""
        div = float(divisor) 
        return Colour(self.r / div, self.g / div, self.b / div)


    def __rmul__(self, factor):
        """Reverse multiplication operator: scalar * colour"""
        return Colour(self.r * factor, self.g * factor, self.b * factor)


    def __add__(self, other):
        """Plus operator for two colours"""
        return Colour(self.r + other.r, self.g + other.g, self.b + other.b)


    def __iadd__(self, other):
        """+= operator for two colours. Componentwise addition to self."""
        self.r += other.r
        self.g += other.g
        self.b += other.b
        return self


    def intColour(self):
        """Return an RGB triple of self's RGB components, each multiplied
        by 256 and clamped to the range 0..255"""
        return (toInt(self.r), toInt(self.g), toInt(self.b))
 

    def __repr__(self):
        """The string representation of self"""
        return "Colour(%f,%f,%f)"  % (self.r, self.g, self.b)


# Demo code to run if this file is run directly rather than just being imported.

if __name__ == "__main__":
    colourA = Colour(0.5, 0.2, 0.5)
    print "colourA:", str(colourA)
    colourB = 0.5 * colourA
    print "colourB:", str(colourB)
    print "colourC:", str(colourA * 0.5)
    print "colourD:", str(colourA / 2)
    reflectance = Colour(1, 0.5, 0.2)
    print "reflectance:", str(reflectance)
    print "colourB * reflectance", colourB.modulate(reflectance)
    colourA += colourB
    print "After adding in colourB, colourA is: ", str(colourA)
    print "In (0..255) ints, colour A is:", colourA.intColour()
