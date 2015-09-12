using UnityEngine;
using System.Collections;
using Meta;
using System.Net;
using System.Text;

public class CameraScript : MonoBehaviour {


	public string fileToUpload = "C:/Users/Jake/Desktop/img_file.png";
	public string url = "http://localhost:5000/img";
	public SpriteRenderer spriteRenderer;
	public Sprite captureImage;
	public Sprite viewImage;
	public bool hasTakenPic = false;
	private float timer;

	// Use this for initialization
	void Start () {
		//renders 
		spriteRenderer = GetComponent<SpriteRenderer> ();
		Debug.Log (viewImage);
		spriteRenderer.sprite = viewImage;
	}
	
	// Update is called once per frame
	void Update () {
		timer += Time.deltaTime;
		if (Input.GetKeyDown ("space")) {
			timer = 0f;
			if (spriteRenderer.sprite == viewImage)
				spriteRenderer.sprite = captureImage;
			Application.CaptureScreenshot (fileToUpload);
			hasTakenPic = true;
			SendToServer(fileToUpload);

		}
		else if (timer >= 1.0f) {
			spriteRenderer.sprite = viewImage;
			timer = 0f;
		}
	}

	public void OnTouchHold()
	{
		spriteRenderer.material.color = Color.green;
	}

	void SendToServer(string file)
	{
		using (WebClient client = new WebClient()) {
			byte[] result = client.UploadFile (url, file);
			string responseAsString = Encoding.Default.GetString (result);
		}
	}
	
}
