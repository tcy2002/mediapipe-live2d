using TMPro;
using UnityEngine;

public class ButtonC : MonoBehaviour
{
    // Start is called before the first frame update
    private GameObject _inputFields;
    public TMP_InputField inputWidth;
    public TMP_InputField inputHeight;
    private int _width = 640;
    private int _height = 480;
    
    private void Start()
    {
        _inputFields = GameObject.Find("Canvas/Panel");
        _inputFields.SetActive(false);
        inputWidth.text = _width.ToString();
        inputHeight.text = _height.ToString();
        inputWidth.onEndEdit.AddListener(result =>
        {
            int.TryParse(result, out var width);
            if (width < 80 || width > 3840)
                return;
            _width = width;
        });
        inputHeight.onEndEdit.AddListener(result =>
        {
            int.TryParse(result, out var height);
            if (height < 80 || height > 2160)
                return;
            _height = height;
        });
    }

    public void OnClick()
    {
        _inputFields.SetActive(true);
    }

    public void OnCancel()
    {
        _inputFields.SetActive(false);
    }

    public void OnConfirm()
    {
        CaptureTexture.SetPixel(_width, _height);
        _inputFields.SetActive(false);
    }
}
