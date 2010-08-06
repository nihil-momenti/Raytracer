from geom3 import Ray3
from math import tan, pi
from random import random

class View(object):
  def __init__(self, viewPoint, lookAtPoint, viewUp, hFov, height, width, multi):
    viewDirection = (lookAtPoint - viewPoint).unit()
    self.point = viewPoint
    self.width = width
    self.height = height
    self.multi = multi
    spacing = 2 * tan(hFov * pi / 360) / width
    self.yVector = -spacing * viewUp.unit()
    self.xVector = spacing * viewUp.unit().cross(viewDirection.unit()).unit()
    self.topLeft = (viewPoint + viewDirection) - (self.yVector * height / 2 + self.xVector * width / 2)


  def eye_ray(self, row, col):
    dy = self.yVector * (row + 0.5)
    dx = self.xVector * (col + 0.5)
    point = self.topLeft + dy + dx
    ray = Ray3(self.point, point - self.point)
    return ray

    
  def eye_rays(self, row, col):
    rays = []
    for irow in range(self.multi):
      for icol in range(self.multi):
        dy = self.yVector * (row + (irow + random()/2) / self.multi)
        dx = self.xVector * (col + (icol + random()/2) / self.multi)
        point = self.topLeft + dy + dx
        rays.append(Ray3(self.point, point - self.point))
    return rays
