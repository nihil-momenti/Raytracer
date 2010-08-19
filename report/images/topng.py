import sys
from PIL import Image

for arg in sys.argv[1:]:
  print arg
  Image.open(arg).save(arg[0:arg.rfind('.')] + '.png')
