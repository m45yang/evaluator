Endpoints:
----------

- localhost:5000/img

	- Method `POST`
	- Expects `img_file` field in the request body. The `img_file` should be the raw image file data.

- localhost:5000/test

	- Method `GET`
	- This is just for testing. It uses an already saved image to test the API.

- localhost:5000/ebay_search

	- Method `GET`
	- This endpoint is used for searching EBay. It expects a `q` parameter in the get request. Like `http://localhost:5000/search?q=Moleskin`
	- It returns `name` & `price`

- localhost:5000/wal_search

	- It expects a `q` parameter which is the name of the product. It returns the product name and price in JSON format. It is similar to the ebay endpoint.

- localhost:5000/list_languages

	- It doesn't expect any parameter. It returns the list of all the languages which we can translate text into

- localhost:5000/translate
	
	- It expects two parameters in a `get` request. The first one is `q` which is the text which was to be translated and the second one is `lang` which is the language the text should be translated to. For example: `http://localhost:5000/translate?q=A water bottle&lang=de`

- localhost:5000/tts

	- It expects two parameters in a `get` request. The first one is `q` which is the text which is to be spoken and the second one is `lang` which is the dialect in which the text would be spoken in. For example: `http://localhost:5000/tts?q=A water bottle&lang=en`. It redirects you to a `.mp3` url so you can pass this url directly to an MP3 player which can play audio from MP3 url.
