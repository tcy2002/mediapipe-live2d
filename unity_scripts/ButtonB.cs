using System.Collections.Generic;
using UnityEngine;

public class ButtonB : MonoBehaviour
{
    public List<GameObject> objects;
    private int _len;
    private int _num;
    private int _old;
    private float _speedOut;
    private float _speedIn;
    private readonly float[] _yOffset = { -1.2f, 0.16f, -1.14f, -1.53f };

    public void OnClick()
    {
        if (_num != _old)
            return;
        _num = (_num + 1) % _len;
        objects[_num].transform.position = -8.0f * Vector3.right + _yOffset[_num] * Vector3.up;
    }

    private void Start()
    {
        _len = objects.Count;
        for (var i = 1; i < _len; i++)
        {
            objects[i].SetActive(false);
        }
    }

    private void Update()
    {
        if (_num == _old || objects[_num].transform.position.x >= 0)
            return;
        
        _speedOut = 4.0f * objects[_old].transform.position.x + 2.0f;
        objects[_old].transform.Translate(Vector3.right * (_speedOut * Time.deltaTime));
        
        if (objects[_old].transform.position.x < 5.0f)
            return;
        
        objects[_old].SetActive(false);
        objects[_num].SetActive(true);
        
        _speedIn = 4.0f * (-objects[_num].transform.position.x) + 1.0f;
        objects[_num].transform.Translate(Vector3.right * (_speedIn * Time.deltaTime));
        
        if (objects[_num].transform.position.x < 0)
            return;
        
        _old = _num;
    }
}
