using UnityEngine;
using System.Collections;

public class WWWFormImage : MonoBehaviour {
	
	public string screenShotURL= "http://httpbin.org/post";
	public string url = "http://localhost:5000/img";
	// Use this for initialization
	void Start () {
		StartCoroutine(UploadJPG());
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
		byte[] bytes = tex.EncodeToPNG();
		Destroy( tex );
		
		// Create a Web Form
		WWWForm form = new WWWForm();
		form.AddField("frameCount", Time.frameCount.ToString());
		form.AddBinaryData("fileUpload", bytes, @"C:\images\img_file.jpg", "image/jpg");
		
		// Upload to a cgi script
		WWW w = new WWW(url, form);
		yield return w;
		if (!string.IsNullOrEmpty(w.error)) {
			print(w.error);
		}
		else {
			print("Finished Uploading Screenshot");
		}
	}
}