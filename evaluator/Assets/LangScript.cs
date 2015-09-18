using UnityEngine;
using System.Collections;

public class LangScript : MonoBehaviour {
	WWW www;
	// Use this for initialization
	void Start () {
		string url = "http://mhacks.azurewebsites.net/translate?q=Hi%20there&lang=de";
		www = new WWW(url);

	}
	
	// Update is called once per frame
	void Update () {

		if (Input.GetKey ("A")) {
			StartCoroutine(WaitForRequest(www));
		}
	
	}

	IEnumerator WaitForRequest(WWW www)
	{
		yield return www;
		// check for errors
		if (www.error == null)
		{
			Debug.Log("WWW Ok!: " + www.text);
		} else {
			Debug.Log("WWW Error: "+ www.error);
		}    
	}
}
