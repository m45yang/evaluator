from flask import Flask, request, jsonify
import requests
import uuid
from ebaysdk.finding import Connection
from ebaysdk.exception import ConnectionError

app = Flask(__name__)

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
img = 'test_pic.jpg'
postData = {
	#'image_request[remote_image_url]' : imageUrl,
	'image_request[locale]': 'en',
	'image_request[language]': 'en',
}

@app.route('/img', methods=['POST'])
def img_search():
	img_data = request.files['img_file']
	parse_resp = requests.post('https://api.parse.com/1/files/'+str(uuid.uuid4())+'.jpg', headers=parse_header, data=img_data)
	img_file_url = parse_resp.json()['url']
	
	req_data["image_request[remote_image_url]"] = img_file_url
	resp = requests.post(IMG_REQUEST, headers=req_headers, data=req_data)
	token = resp.json()['token']

	resp = requests.get(IMG_RESPONSE+token,headers=cloud_headers)
	while resp.json()['status'] != 'completed':
		resp = requests.get(IMG_RESPONSE+token,headers=cloud_headers)
#	print resp.json()["name"]
	return jsonify({"name": resp.json()["name"]})

@app.route('/search', methods=['GET'])
def search_ebay():
	searchword = request.args.get('q', '')
	try:
		api = Connection(appid=EBAY_APPID, config_file=None)
		response = api.execute('findItemsAdvanced', {'keywords': searchword})
#		print int(response.dict()['searchResult']['_count']) == 0
		if int(response.dict()['searchResult']['_count']) == 0:
			return jsonify({"error":"No results found"})
		item = response.reply.searchResult.item[0]
#		print dir(item)
		return jsonify({"name":item.title, "price": item.sellingStatus.currentPrice.value+' '+item.sellingStatus.currentPrice._currencyId})
	except ConnectionError as e:
		print e 
		return jsonify(e.response.dict())

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
	print resp.json()["name"]
	return jsonify({"name": resp.json()["name"]})

if __name__ == "__main__":
	app.run(debug=True)