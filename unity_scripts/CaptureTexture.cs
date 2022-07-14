using Unity.VisualScripting;
using UnityEngine;

public class CaptureTexture : MonoBehaviour
{
    public int width = 640;
    public int height = 480;
    
    private static Camera _mainCam;
    private static RenderTexture _rt;
    
    private UnityCapture.Interface _captureInterface;

    private void Start()
    {
        // Create texture and capture interface
        _mainCam = GameObject.Find("OutputCamera").GetComponent<Camera>();
        SetPixel(width, height);
        _captureInterface = new UnityCapture.Interface(UnityCapture.ECaptureDevice.CaptureDevice1);
    }

    private void OnDestroy()
    {
        //Cleanup capture interface
        _captureInterface.Close();
    }

    private void Update()
    {
        // Update the capture texture
        var result = _captureInterface.SendTexture(_rt);
        //if (result != UnityCapture.ECaptureSendResult.SUCCESS)
            //print("SendTexture failed: " + result);
    }

    public static void SetPixel(int width, int height)
    {
        _rt = new RenderTexture(width, height, 24);
        _mainCam.targetTexture = _rt;
        RenderTexture.active = _rt;
    }
}
