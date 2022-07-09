using System;
using UnityEngine;
using System.Net.Sockets;

public class VideoCapture : MonoBehaviour
{
    public Camera mainCam;
    private Texture2D _t2d;
    private RenderTexture _rt;

    private Socket _client;

    private const int Width = 640;
    private const int Height = 480;
    private const string Address = "127.0.0.1";
    private const int Port = 12345;

    private void Start()
    {
        _t2d = new Texture2D(Width, Height, TextureFormat.RGB24, false);
        _rt = new RenderTexture(Width, Height, 24);
        mainCam.targetTexture = _rt;

        _client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        _client.Connect(Address, Port);
    }

    private void Update()
    {
        try
        {
            RenderTexture.active = _rt;
            _t2d.ReadPixels(new Rect(0, 0, _rt.width, _rt.height), 0, 0);
            _t2d.Apply();
            RenderTexture.active = null;
            var bytes = _t2d.EncodeToJPG();

            _client.Send(bytes);
        }
        catch (Exception e)
        {
            _client.Close();
            print(e);
        }
    }

    private void OnApplicationQuit()
    {
        _client.Close();
    }
}