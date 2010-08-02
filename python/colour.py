# The Colour class, a class to represent an RGB colour
# supporting addition, scaling by a scalar and modulation
# (component-wise multiplication).

# Written for COSC 363.
# @author Richard Lobb
# @version July 2010.

# Last year I provided modulation by an overloaded multiply operator
# but that seemed to cause confusion. Let's see what happens this year.

def toInt(floatVal):
  return max(0, min(255, int(256.0 * floatVal)))


class Colour(object):
  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b


  def __mul__(self, factor):
    if (isinstance(factor, float)):
      return Colour(self.r * factor, self.g * factor, self.b * factor)
    elif (isinstance(factor, int)):
      return Colour(self.r * factor, self.g * factor, self.b * factor)
    elif (isinstance(factor, Colour)):
      return Colour(self.r * factor.r, self.g * factor.g, self.b * factor.b)
    else:
      return NotImplemented()


  def __div__(self, divisor):
    div = float(divisor) 
    return Colour(self.r / div, self.g / div, self.b / div)


  def __rmul__(self, factor):
    if (isinstance(factor, float)):
      return Colour(self.r * factor, self.g * factor, self.b * factor)
    elif (isinstance(factor, int)):
      return Colour(self.r * factor, self.g * factor, self.b * factor)
    else:
      return NotImplemented()


  def __add__(self, other):
    return Colour(self.r + other.r, self.g + other.g, self.b + other.b)


  def __iadd__(self, other):
    self.r += other.r
    self.g += other.g
    self.b += other.b
    return self

  def __pow__(self, power):
    return Colour(self.r ** power, self.g ** power, self.b ** power)


  def intColour(self):
    return (toInt(self.r), toInt(self.g), toInt(self.b))
 

  def __repr__(self):
    return "Colour(%f,%f,%f)"  % (self.r, self.g, self.b)
