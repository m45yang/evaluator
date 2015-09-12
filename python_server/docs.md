Endpoints:
----------

- localhost:5000/img

	- Method `POST`
	- Expects `img_file` field in the request body. The `img_file` should be the raw image file data.

- localhost:5000/test

	- Method `GET`
	- This is just for testing. It uses an already saved image to test the API.

- localhost:5000/search

	- Method `POST`
	- This endpoint is used for searching EBay. It expects a `q` parameter in the get request. Like `http://localhost:5000/search?q=Moleskin`
	- It returns `name` & `price`