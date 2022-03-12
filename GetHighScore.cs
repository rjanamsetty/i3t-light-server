// Code sourced from the following webpages:
// https://www.youtube.com/watch?v=lnwOq0kW4ms&t=86s
// https://docs.unity3d.com/ScriptReference/Networking.UnityWebRequest.Get.html
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;


public class GetHighScore : MonoBehaviour
{
    // Initialize variables
    private InputField output;
    private string uri = "http://192.168.0.86:5000/highscore";

    // Start is called before the first frame update
    void Start()
    {
        // Get the input field
        output = GameObject.Find("OutputField").GetComponent<InputField>();
        // Call the function to get the high score
        StartCoroutine(GetRequest());
        // Find get button and add a listener
        GameObject.Find("GETButton").GetComponent<Button>().onClick.AddListener(GetData);

    }

    void GetData() => StartCoroutine(GetRequest());

    // Get the high score from the server
    IEnumerator GetRequest()
    {
        // Set temporary variable to fill ouput area with data
        output.text = "Loading...";
        // Create a new UnityWebRequest object to get the data from the server
        using (UnityWebRequest www = UnityWebRequest.Get(uri))
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
                    // Return data
                    string text = www.downloadHandler.text;
                    // Remove {, }, and " from the data
                    text = text.Replace("{", "");
                    text = text.Replace("}", "");
                    text = text.Replace("\"", "");
                    // Dispay the data
                    output.text = text;
                    break;
                // If response is not 200, notify user with error
                default:
                    output.text = "HTTP Error: " + www.error;
                    break;
            }
        }
    }
}