using UnityEngine;
using Live2D.Cubism.Core;

public class HiyoriController : MonoBehaviour
{
    private CubismModel _model;
    
    public float absBodyRollThreshold = 30;
    public float absBodyYawThreshold = 30;
    public float absBodyRollYawMax = 60;

    public float earMaxThreshold = 0.38f;
    public float earMinThreshold = 0.30f;

    public float irisLeftCeiling = 0.2f;
    public float irisRightCeiling = 0.85f;
    public float irisUpCeiling = 0.8f;
    public float irisDownCeiling = 0.2f;

    public float marMaxThreshold = 0.8f;
    public float marMinThreshold;

    public bool changeMouthForm = true;
    public float mouthDistMin = 60.0f;
    public float mouthDistMax = 80.0f;

    private float _t1;       // for breath
    private float[] _params;
    private bool _blush;

    // Start is called before the first frame update
    private void Start()
    {
        _model = this.FindCubismModel();

        absBodyRollThreshold = Mathf.Abs(absBodyRollThreshold);
        absBodyYawThreshold = Mathf.Abs(absBodyYawThreshold);
        absBodyRollYawMax = Mathf.Abs(absBodyRollYawMax);
    }

    // Update is called once per frame
    private void Update()
    {
        // control the blush of the avatar
        if (!Input.GetKeyDown(KeyCode.Alpha1))
            return;
        _blush = !_blush;
    }
    
    private void LateUpdate()
    {
        _params = FaceTracker.GetParams();
        
        // yaw
        var parameter = _model.Parameters[0];
        parameter.Value = -Mathf.Clamp(_params[2], -30, 30);

        // pitch
        parameter = _model.Parameters[1];
        parameter.Value = Mathf.Clamp(_params[1], -30, 30);

        // roll
        parameter = _model.Parameters[2];
        parameter.Value = -Mathf.Clamp(_params[0], -30, 30);

        // breath
        _t1 += Time.deltaTime;
        var value = (Mathf.Sin(_t1 * 3f) + 1) * 0.5f;
        parameter = _model.Parameters[17];
        parameter.Value = value;

        parameter = _model.Parameters[19];
        parameter.Value = _blush ? 1: 0;

        EyeBlinking();

        IrisMovement();

        MouthOpening();

        if (changeMouthForm)
            MouthForm();

    }

    // whole body movement (body X/Z)
    // optional as the effect is not that pronounced
    private void BodyMovement() {
        // roll
        var parameter = _model.Parameters[16];
        if (Mathf.Abs(_params[0]) > absBodyRollThreshold) {
            parameter.Value = -(10 - 0) / (absBodyRollYawMax - absBodyRollThreshold) * ((Mathf.Abs(_params[0]) - absBodyRollThreshold) * Mathf.Sign(_params[0]));
        }
        else {
            parameter.Value = 0;
        }

        // yaw
        parameter = _model.Parameters[14];
        if (Mathf.Abs(_params[2]) > absBodyYawThreshold) {
            parameter.Value = -(10 - 0) / (absBodyRollYawMax - absBodyYawThreshold) * ((Mathf.Abs(_params[2]) - absBodyYawThreshold) * Mathf.Sign(_params[2]));
        }
        else {
            parameter.Value = 0;
        }
    }

    private void EyeBlinking() {
        // my left eye = live2d's right (mirroring)
        _params[3] = Mathf.Clamp(_params[3], earMinThreshold, earMaxThreshold);
        var eyeLValue = (_params[3] - earMinThreshold) / (earMaxThreshold - earMinThreshold) * 1;
        var parameter = _model.Parameters[6];
        parameter.Value = eyeLValue;

        // my right eye = live2d's left (mirroring)
        _params[4] = Mathf.Clamp(_params[4], earMinThreshold, earMaxThreshold);
        var eyeRValue = (_params[4] - earMinThreshold) / (earMaxThreshold - earMinThreshold) * 1;
        parameter = _model.Parameters[4];
        parameter.Value = eyeRValue;
    }

    private void IrisMovement() {
        var eyeballX = (_params[5] + _params[7]) / 2;
        var eyeballY = (_params[6] + _params[8]) / 2;

        eyeballX = Mathf.Clamp(eyeballX, irisLeftCeiling, irisRightCeiling);
        eyeballY = Mathf.Clamp(eyeballY, irisDownCeiling, irisUpCeiling);

        // range is [-1, 1]
        eyeballX = (eyeballX - irisLeftCeiling) / (irisRightCeiling - irisLeftCeiling) * 2 - 1;
        eyeballY = (eyeballY - irisDownCeiling) / (irisUpCeiling - irisDownCeiling) * 2 - 1;

        // optional
        // pass the value to an "activation function"
        // to create a smoother effect (when the iris is near center)
        eyeballX = Mathf.Pow(eyeballX, 3);
        eyeballY = Mathf.Pow(eyeballY, 3);

        var parameter = _model.Parameters[8];
        parameter.Value = eyeballX;
        parameter = _model.Parameters[9];
        parameter.Value = eyeballY;
    }

    private void MouthOpening() {
        // mouth aspect ratio -> mouth opening
        var marClamped = Mathf.Clamp(_params[9], marMinThreshold, marMaxThreshold);
        marClamped = (marClamped - marMinThreshold) / (marMaxThreshold - marMinThreshold) * 1;
        var parameter = _model.Parameters[13];
        parameter.Value = marClamped;
    }

    private void MouthForm() {
        // mouth distance -> mouth form
        var mouthDistClamped = Mathf.Clamp(_params[10], mouthDistMin, mouthDistMax);
        // range is [-1, 1]
        mouthDistClamped = (mouthDistClamped - mouthDistMin) / (mouthDistMax - mouthDistMin) * 2 - 1;
        var parameter = _model.Parameters[12];
        parameter.Value = mouthDistClamped;
    }
}
