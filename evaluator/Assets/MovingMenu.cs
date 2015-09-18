using UnityEngine;
using System.Collections;

public class MovingMenu : MonoBehaviour {

	public Vector3 pos;
	public float speed = 2.8f;
	int num = 1;
	// Use this for initialization
	void Start () {
		pos = transform.position;
	}
	
	// Update is called once per frame
	void Update () {

		if (Input.GetKeyDown ("escape")) {
			speed = 0f;
			pos.z = -1000f;
		}
		if (transform.position.x >= 21f) {
			num = -1;
		}
	    else if (transform.position.x <= -21f) {
			num = 1;
		}
		pos.x += num * speed * Time.deltaTime;
		transform.position = pos;

	
	}
}
