import requests
a = requests.post('http://localhost:5000/img', files={'fileUpload': open('img_file.jpg', 'rb')})
print a.text
b = requests.get('http://localhost:5000/ebay_search?q='+a.text)
print b.text
c = requests.get('http://localhost:5000/wal_search?q='+a.text)
print c.text
