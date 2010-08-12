from datetime import datetime

from csg import *
from view import *
from scene import *
from shapes import *
from colour import *
from camera import *
from material import *
from lighting import *
from lightbulb import *
from transforms import *
from geom3 import Point3, Vector3, Ray3, unit

import myScene

try:
  import psyco
  psyco.full()
  "Psyco running"
except ImportError:
  print "Psyco not available"

start = datetime.now()
view, scene = myScene.generateScene()

camera = Camera(view, scene)

img = camera.take_photo_new()
img.save('image.bmp')    # Display image in default image-viewer application
print "Rendering time:", datetime.now() - start
