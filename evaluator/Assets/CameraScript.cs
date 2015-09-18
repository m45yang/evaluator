using UnityEngine;
using System.Collections;
using Meta;
using System.Net;
using System.Text;
using System.IO;
using System;
using System.Collections.Generic;
using System.Linq;

public class CameraScript : MonoBehaviour {


	public string fileToUpload = @"C:\images\img_file.jpg";
	public string url = "http://localhost:5000/img";
	public SpriteRenderer spriteRenderer;
	public Sprite captureImage;
	public Sprite viewImage;
	private float timer;	
	public bool isMenu = true;
	public float scale;

	public string itemName;
	public string walmartResponse;
	public string ebayResponse;
	public bool search = false;

    public NameScript nameScript;


	// Use this for initialization
	void Start () {
		//renders
		spriteRenderer = GetComponent<SpriteRenderer> ();
		Debug.Log (viewImage);
		spriteRenderer.sprite = viewImage;
		scale = 0f;

		// nameScript = GameObject.Find ("NameText").GetComponent<NameScript> ();
	}

	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown ("escape")) {
			isMenu = false;
			scale = 1f;
		}

		if (isMenu == false) {
			timer += Time.deltaTime;
			transform.localScale = new Vector3(scale,2, scale);
			if (Input.GetKeyDown ("space")) {
				timer = 0f;
				if (spriteRenderer.sprite == viewImage) {
					spriteRenderer.sprite = captureImage;
				}
				Application.CaptureScreenshot (fileToUpload);
				StartCoroutine(UploadJPG());
			}
			else if (timer >= 1.0f) {
				spriteRenderer.sprite = viewImage;
				timer = 0f;
			}

			if (search) {
				// nameScript.name = itemName;
				timer = 0f;
				searchDatabases();
			}
		}
	}

	IEnumerator UploadJPG() {
		// We should only read the screen after all rendering is complete
		yield return new WaitForEndOfFrame();

		// Create a texture the size of the screen, RGB24 format
		int width = Screen.width;
		int height = Screen.height;
		var tex = new Texture2D( width, height, TextureFormat.RGB24, false );

		// Read screen contents into the texture
		tex.ReadPixels( new Rect(0, 0, width, height), 0, 0 );
		tex.Apply();

		// Encode texture into PNG
		byte[] bytes = tex.EncodeToJPG();
		Destroy( tex );

		// Create a Web Form
		WWWForm form = new WWWForm();
		form.AddField("frameCount", Time.frameCount.ToString());
		form.AddBinaryData("fileUpload", bytes, @"C:\images\img_file.jpg", "image/jpg");

		// Upload to a cgi script
		WWW w = new WWW(url, form);
		yield return w;
		search = true;
		itemName = w.text;
		Debug.Log (itemName);
		if (!string.IsNullOrEmpty(w.error)) {
			print(w.error);
		}
		else {
			print("Finished Uploading Screenshot");
		}
	}

	public void searchDatabases() {
		search = false;
		WebClient walmartClient = new WebClient ();
		walmartClient.QueryString.Add ("q", itemName);
		walmartResponse = walmartClient.DownloadString ("http://localhost:5000/wal_search");
		Debug.Log (walmartResponse);

		WebClient ebayClient = new WebClient ();
		ebayClient.QueryString.Add ("q", itemName);
		ebayResponse = ebayClient.DownloadString ("http://localhost:5000/ebay_search");
		Debug.Log (ebayResponse);
	}
}
