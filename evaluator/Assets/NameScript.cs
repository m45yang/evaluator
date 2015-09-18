using UnityEngine;
using System.Collections;

public class NameScript : MonoBehaviour {

	public string name;

	// Use this for initialization
	void Start () {

	
	}
	
	// Update is called once per frame
	void Update () {
		GetComponent<TextMesh>().text = "Name: " + name;

	
	}
}
