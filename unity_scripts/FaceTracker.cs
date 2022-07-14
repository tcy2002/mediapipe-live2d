using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class FaceTracker : MonoBehaviour
{
    private Thread _receiveThread;
    private static Socket _listener;
    private static Socket _client;

    private const string Address = "127.0.0.1";
    private const int Port = 54321;

    private static float _roll;
    private static float _pitch;
    private static float _yaw;
    private static float _earLeft;
    private static float _earRight;
    private static float _xRatioLeft;
    private static float _yRatioLeft;
    private static float _xRatioRight;
    private static float _yRatioRight;
    private static float _mar;
    private static float _mouthDist;
    
    private void Start()
    {
        Screen.SetResolution(800, 600, false);
        InitTcp();
        _receiveThread = new Thread(ReceiveData);
        _receiveThread.IsBackground = true;
        _receiveThread.Start();
    }

    private void InitTcp()
    {
        _listener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        _listener.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, 1);
        var port = Port;
        try
        {
            _listener.Bind(new IPEndPoint(IPAddress.Parse(Address), port));
            _listener.Listen(1);
        }
        catch (Exception e)
        {
            print(e);
        }            
    }

    private void OnApplicationQuit()
    {
        _receiveThread.Abort();
    }

    private static void ReceiveData()
    {
        try
        {
            var bytes = new byte[1024];
            while (true)
            {
                using(_client = _listener.Accept()) {
                    int length;
                    while ((length = _client.Receive(bytes)) != 0) {
                        var data = new byte[length];
                        Array.Copy(bytes, 0, data, 0, length);
                        var clientMessage = Encoding.ASCII.GetString(data);
                        var res = clientMessage.Split(' ');

                        _roll = float.Parse(res[0]);
                        _pitch = float.Parse(res[1]);
                        _yaw = float.Parse(res[2]);
                        _earLeft = float.Parse(res[3]);
                        _earRight = float.Parse(res[4]);
                        _xRatioLeft = float.Parse(res[5]);
                        _yRatioLeft = float.Parse(res[6]);
                        _xRatioRight = float.Parse(res[7]);
                        _yRatioRight = float.Parse(res[8]);
                        _mar = float.Parse(res[9]); 
                        _mouthDist = float.Parse(res[10]);
                    }
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
        }
    }

    private void OnDestroy()
    {
        _listener.Close();
    }

    public static float[] GetParams()
    {
        return new []
        {
            _roll, _pitch, _yaw, _earLeft, _earRight,
            _xRatioLeft, _yRatioLeft, _xRatioRight, _yRatioRight,
            _mar, _mouthDist
        };
    }
}
