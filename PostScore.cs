// Code sourced from the following webpages:
// https://www.youtube.com/watch?v=lnwOq0kW4ms&t=86s
// https://docs.unity3d.com/ScriptReference/Networking.UnityWebRequest.Get.html
// https://docs.unity3d.com/ScriptReference/Networking.UnityWebRequest.Post.html
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;


public class PostScore : MonoBehaviour
{
    // Initialize variables
    private InputField username;
    private InputField score;
    private InputField output;
    private string uri = "http://192.168.0.86:5000/";

    // Start is called before the first frame update
    void Start()
    {
        // Get the username, score, and output input fields
        username = GameObject.Find("UsernameField").GetComponent<InputField>();
        score = GameObject.Find("PointsField").GetComponent<InputField>();
        output = GameObject.Find("OutputField").GetComponent<InputField>();
        // Find post button and add listener
        GameObject.Find("POSTButton").GetComponent<Button>().onClick.AddListener(PostData);
    }

    void PostData() => StartCoroutine(PostRequest());

    // Post score to server
    IEnumerator PostRequest()
    {
        // Create a new form
        WWWForm form = new WWWForm();
        // Add username and score to form
        form.AddField("username", username.text);
        form.AddField("score",  int.Parse(score.text));
        // Create a new web request
        using (UnityWebRequest www = UnityWebRequest.Post(uri, form))
        {
            // Wait for the request to complete
            yield return www.SendWebRequest();
            // Check if the request was successful
            switch (www.result)
            {
                // Checks for connection errors and notifies user
                case UnityWebRequest.Result.ConnectionError:
                    output.text = "Error connecting to " + uri;
                    break;
                // If response is 200, parse the data and display it
                case UnityWebRequest.Result.Success:
                    break;
                // If response is not 200, notify user with error
                default:
                    output.text = "HTTP Error: " + www.error;
                    break;
            }
        }
    }
}