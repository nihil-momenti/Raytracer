from geom3 import Ray3
from math import tan

class View(object):
  def __init__(self, viewPoint, viewDirection, viewUp, hFov, height, width):
    self.point = viewPoint
    self.width = width
    self.height = height
    spacing = 2 * tan(hFov/2) / width
    self.yVector = -spacing * viewUp.unit()
    self.xVector = spacing * viewUp.cross(viewDirection).unit()
    self.topLeft = (viewPoint + viewDirection) - (self.yVector * height / 2 + self.xVector * width / 2)

  def eye_rays(self, row, col, multi):
    rays = []
    for irow in range(multi):
      for icol in range(multi):
        point = self.topLeft + self.yVector * (row + irow / multi) + self.xVector * (col + icol / multi)
        rays.append(Ray3(self.point, point - self.point))
    return rays

