import cStringIO as StringIO
from PIL import Image

with open('evaluate_pic1.jpg', 'rb') as f:
	d = f.read()
	d.strip()

stream = StringIO.StringIO(d)
img = Image.open(stream)
width = img.size[0]/3
height = img.size[1]/3
img = img.resize((width, height),Image.ANTIALIAS)
print img.size
img.save('image_scaled.jpg',quality=95)
