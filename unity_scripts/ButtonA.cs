using System;
using System.Collections.Generic;
using UnityEngine;

public class ButtonA : MonoBehaviour
{
    public List<Material> skyMats;
    private int _len;
    private int _num;

    private void Start()
    {
        _len = skyMats.Count;
    }

    public void OnClick()
    {
        _num = (_num + 1) % _len;
        RenderSettings.skybox = skyMats[_num];
    }
}
