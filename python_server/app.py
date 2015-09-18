from flask import Flask, request, jsonify, redirect
from ebaysdk.finding import Connection
from ebaysdk.exception import ConnectionError
import requests
import uuid
import json
import re
import urllib2
import goslate
import StringIO
from PIL import Image
import logging

log = logging.getLogger
app = Flask(__name__)
gs = goslate.Goslate()

IMG_REQUEST = 'https://api.cloudsightapi.com/image_requests/' # get token
IMG_RESPONSE = 'https://api.cloudsightapi.com/image_responses/' # get the final recognition result with token
EBAY_APPID = 'FuckYeah-3aa5-41ba-bd61-05ccd011d237'
#--------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------#
cloud_headers= {
	"Origin": "http://cloudsightapi.com",
	"Accept-Encoding": "gzip, deflate, sdch",
	"Accept-Language": "en-US,en;q=0.8",
	"Authorization": "CloudSight amZd_zG32VK-AoSz05JLIA",
	"Accept": "*/*",
	"Referer": "http://cloudsightapi.com/api",
	"User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2507.0 Safari/537.36",
	"Connection": "keep-alive"
}
req_headers = {
	"Authorization": "CloudSight amZd_zG32VK-AoSz05JLIA",  
	"Origin": "http://cloudsightapi.com",  
	"Accept-Encoding": "gzip, deflate",  
	"Accept-Language": "en-US,en;q=0.8",  
	"User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2507.0 Safari/537.36",  
	"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",  
	"Accept": "*/*",
	"Referer": "http://cloudsightapi.com/api",  
	"Connection": "keep-alive"
}

req_data = {
	"image_request[remote_image_url]": "http://blogs.tribune.com.pk/wp-content/uploads/2013/08/18588-aitchisoncollege-1377159399-429-640x480.jpg",
	"image_request[locale]": "en-US",
	"image_request[language]": "en-US"
}
#--------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------#

parse_header = {
	'X-Parse-Application-Id': 'vt08VNPo307ZN50qD9jPPKkyIqoVPDgHNDyXd5gL',
	'X-Parse-Master-Key': 'hiLRpbZeAmb15SSgvmkdfXvFg0mTlkmPfycMLKiw',
	'Content-Type': 'image/jpeg'
}
#files={'image': open(img, 'rb')}, 
img = 'tested.jpg'
postData = {
	#'image_request[remote_image_url]' : imageUrl,
	'image_request[locale]': 'en',
	'image_request[language]': 'en',
}
colours = ['red', 'orange', 'yellow', 'grey', 'green', 'blue', 'brown', 'grass', 'black', 'white', 'pink', 'golden']

@app.route('/img', methods=['POST'])
def img_search():
	img_data = request.files['fileUpload']
	stream = StringIO.StringIO(img_data)
	img = Image.open(img_data)

	width, height = img.size 
	width /= 2
	left = (width-326)/2
	img = img.crop((left,30,left+326,height-35))

	file_data = StringIO.StringIO()
	img.save(file_data,quality=95, format="JPEG")
	contents = file_data.getvalue()
	file_data.close()

	parse_resp = requests.post('https://api.parse.com/1/files/'+str(uuid.uuid4())+'.jpg', headers=parse_header, data=contents)
	img_file_url = parse_resp.json()['url']

	req_data["image_request[remote_image_url]"] = img_file_url
	resp = requests.post(IMG_REQUEST, headers=req_headers, data=req_data)
	token = resp.json()['token']

	resp = requests.get(IMG_RESPONSE+token,headers=cloud_headers)
	while resp.json()['status'] != 'completed':
		resp = requests.get(IMG_RESPONSE+token,headers=cloud_headers)
	name = resp.json()["name"]
	#text = nltk.word_tokenize(name)
	#text = ' '.join([i[0] for i in nltk.pos_tag(text) if i[1] == 'NN'])
	print name
	write_to_file(name)
	return name;

@app.route('/ebay_search', methods=['GET'])
def search_ebay():
	searchword = request.args.get('q', '')
	for i in colours:
		searchword = searchword.replace(i, '')
	try:
		api = Connection(appid=EBAY_APPID, config_file=None)
		response = api.execute('findItemsAdvanced', {'keywords': searchword})
#		print int(response.dict()['searchResult']['_count']) == 0
		if int(response.dict()['searchResult']['_count']) == 0:
			return jsonify({"error":"No results found"})
		item = response.reply.searchResult.item[0]
#		print dir(item)
		pro = "\n\n\n---------------------------------\n"
		pro += "Ebay item name:" + item.title +"\n"
		pro += "Price: " + item.sellingStatus.currentPrice.value + item.sellingStatus.currentPrice._currencyId
		pro += "\n---------------------------------\n"
		write_to_file(pro)
		print pro
		return jsonify({"name":item.title, "price": item.sellingStatus.currentPrice.value+' '+item.sellingStatus.currentPrice._currencyId})
	except ConnectionError as e:
		print e 
		return jsonify(e.response.dict())

@app.route('/wal_search', methods=['GET'])
def search_walmart():
	searchword = request.args.get('q', '')
	query = searchword.replace("%20", "+")
	for i in colours:
		searchword = searchword.replace(i, '')
	apiKey = "3qukdf87ghrr2mf55rx9j2k8"
	try:
		resp = requests.get("http://api.walmartlabs.com/v1/search", params={'apiKey': apiKey, 'query': query})
		print resp.json()["items"][1]['name']
		# names = [i['name'] for i in resp.json()["items"]]
		pro = "\n\n\n---------------------------------\n"
		pro += "Walmart item name: " + resp.json()["items"][1]['name']+"\n"
		pro += "Price: "+ str(resp.json()["items"][1]['salePrice'])+" USD"
		pro += "\n---------------------------------\n"
		write_to_file(pro)
		print pro
		return jsonify({"name": resp.json()["items"][1]['name'], "price": str(resp.json()["items"][1]['salePrice'])+" USD"})
	except Exception as e:
		print('Search Failed: '+str(e))
		input()

@app.route('/translate', methods=['GET'])
def translate():
	transwords = request.args.get('q', 'Please Type in Text!')
	lang = request.args.get('lang', 'en')
	translated = gs.translate(transwords, lang)
	return jsonify({'text':translated})

@app.route('/list_languages', methods=['GET'])
def list_lang():
	return jsonify(gs.get_languages())

@app.route('/tts', methods=['GET'])
def tts():
	transwords = request.args.get('q', 'Please Type in Text!')
	lang = request.args.get('lang', 'en')
	url = "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl={}&total=1&idx=0&textlen={}"
	url = url.format(transwords, lang, len(transwords))
	return redirect(url, code=302)

# test route
@app.route('/test', methods=['GET'])
def test_img_name():
	parse_resp = requests.post('https://api.parse.com/1/files/'+img, headers=parse_header, data=open(img, 'rb'))
	img_file_url = parse_resp.json()['url']

	req_data["image_request[remote_image_url]"] = img_file_url
	resp = requests.post(IMG_REQUEST, headers=req_headers, data=req_data)
	token = resp.json()['token']

	resp = requests.get(IMG_RESPONSE+token,headers=cloud_headers)
	while resp.json()['status'] != 'completed':
		resp = requests.get(IMG_RESPONSE+token,headers=cloud_headers)
	# print(resp.json()["name"])
	write_to_file(resp.json()["name"])
	return jsonify({"name": resp.json()["name"]})


def write_to_file(data):
	with open('log.txt', 'a+') as f:
		f.write(data)

if __name__ == "__main__":
	app.run(debug=True)
