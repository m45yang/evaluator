using UnityEngine;
using System.Collections;

public class MenuStartScript : MonoBehaviour {

	Vector3 pos;
    public float scale;

	// Use this for initialization
	void Start () {
		scale = transform.localScale.x;
	
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown ("escape")) {

			pos.z = -1000f;
			scale = 0f;
			transform.position = pos;
		}
		transform.localScale = new Vector3(scale,scale, 1);

	}
}
