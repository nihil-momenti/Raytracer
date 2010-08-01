from geom3 import Ray3
from math import tan, pi

class View(object):
  def __init__(self, viewPoint, viewDirection, viewUp, hFov, height, width, multi):
    self.point = viewPoint
    self.width = width
    self.height = height
    self.multi = multi
    spacing = 2 * tan(hFov * pi / 360) / width
    self.yVector = -spacing * viewUp.unit()
    self.xVector = spacing * viewUp.cross(viewDirection).unit()
    self.topLeft = (viewPoint + viewDirection) - (self.yVector * height / 2 + self.xVector * width / 2)
    print viewPoint + viewDirection
    print height
    print width
    print self.topLeft
    print self.xVector
    print self.yVector

  def eye_rays(self, row, col):
    rays = []
    for irow in range(self.multi):
      for icol in range(self.multi):
        point = self.topLeft + self.yVector * (row + irow / self.multi) + self.xVector * (col + icol / self.multi)
        rays.append(Ray3(self.point, point - self.point))
    return rays

