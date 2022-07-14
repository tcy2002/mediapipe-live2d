using System;
using UnityEngine;
using System.Net.Sockets;

public class VideoCapture : MonoBehaviour
{
    public Camera mainCam;
    private Texture2D _t2d;
    private RenderTexture _rt;

    private Socket _client;

    private const int OriWidth = 800;
    private const int OriHeight = 600;
    private const int Width = 320;
    private const int Height = 320;
    private const string Address = "127.0.0.1";
    private const int Port = 12345;

    private void Start()
    {
        Screen.SetResolution(OriWidth, OriHeight, false);
        _rt = new RenderTexture(OriWidth, OriHeight, 24);
        mainCam.targetTexture = _rt;
        RenderTexture.active = _rt;
        _t2d = new Texture2D(Width, Height, TextureFormat.RGB24, false);

        InitTcp();
    }

    private void InitTcp()
    {
        _client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        _client.SendTimeout = 1;
        var failingTime = 0;
        var port = Port;
        while (true)
        {
            try
            {
                _client.Connect(Address, port);
                break;
            }
            catch (Exception e)
            {
                failingTime++;
                port++;
                if (failingTime < 3)
                    continue;
                print(e);
                break;
            }
        }
    }

    private void Update()
    {
        try
        {
            _t2d.ReadPixels(new Rect(240, 140, Width, Height), 0, 0);
            _client.Send(_t2d.EncodeToJPG());
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