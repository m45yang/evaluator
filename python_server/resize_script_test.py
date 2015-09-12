import cStringIO as StringIO
from PIL import Image

with open('test_crop.jpg', 'rb') as f:
	d = f.read()
	d.strip()

stream = StringIO.StringIO(d)
img = Image.open(stream)
#width = img.size[0]/3
#height = img.size[1]/3
#img = img.resize((width, height),Image.ANTIALIAS)

width, height = img.size 
width /= 2
left = (width-326)/2
print left
print img.size
img = img.crop((left,30,left+326,height-35))
print img.size


file_data = StringIO.StringIO()
img.save(file_data,quality=95, format="JPEG")
contents = file_data.getvalue()
print len(contents)
file_data.close()
#img.save('tested.jpg',quality=95)
#return file_data.getvalue()
