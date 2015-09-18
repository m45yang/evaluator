using UnityEngine;
using System.Collections;

public class textScript : MonoBehaviour {
		

	public bool isMenu = true;
	public float scale;

	// Use this for initialization
	void Start () {
		scale = 0;
	
	}
	
	// Update is called once per frame
	void Update () {

		if (Input.GetKey("escape")) {
			isMenu = false;
		}

		if (isMenu == false)
		{
			scale = 0.25f;

		}
		transform.localScale = new Vector3(scale,scale, 1);
	
	}
}
