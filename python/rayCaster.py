from datetime import datetime
from camera import Camera
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
