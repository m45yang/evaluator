using UnityEngine;
using System.Collections;
using Meta;

public class CameraScript : MonoBehaviour {

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
			Application.CaptureScreenshot ("C:/Users/Jake/Desktop/screenshot.png");
			hasTakenPic = true;

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
	
	
}
