using UnityEngine;
using UnityEngine.UI;

public class NumericLabel : MonoBehaviour
{

    [SerializeField]
    private string _name = "NullAttribute";
    [SerializeField]
    private string _valuePrefix = "";
    [SerializeField]
    private bool _integerFormat;
    private float _value = 0;

    public Text NameLabel;
    public Text ValueLabel;

    public string Name
    {
        get => _name; set
        {
            _name = value;
            UpdateLabel();
        }
    }
    public string ValuePrefix
    {
        get => _valuePrefix; set
        {
            _valuePrefix = value;
            UpdateLabel();
        }
    }

    public int IntValue
    {
        get => (int)_value; set
        {
            _value = value;
            _integerFormat = true;
            UpdateLabel();
        }
    }

    public float Value
    {
        get => _value; set
        {
            _value = value;
            UpdateLabel();
        }
    }

    public bool IntegerFormat
    {
        get => _integerFormat; set
        {
            _integerFormat = value;
            UpdateLabel();
        }
    }


    void Start()
    {
        UpdateLabel();
    }

    void UpdateLabel()
    {
        NameLabel.text = Name;

        if (IntegerFormat)
        {
            ValueLabel.text = $"{ValuePrefix}{IntValue}";
        }
        else
        {
            ValueLabel.text = $"{ValuePrefix}{Value:F3}";
        }
    }
}
