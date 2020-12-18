using UnityEngine;
using UnityEngine.UI;

public class TransactionLabel : MonoBehaviour
{

    public Text PriceLabel;
    public Text CountLabel;
    public Slider Selector;

    public Text SelectedCountLabel;
    public Text SelectedTotalLabel;

    private float _price;
    public float Price
    {
        get => _price;
        set
        {
            _price = value;
            PriceLabel.text = $"${_price:F3}";
            TotalPrice = _price * _selectedCount;
        }
    }

    private int _count;
    public int Count
    {
        get => _count;
        set
        {
            _count = value;
            CountLabel.text = $"{_count}";
        }
    }

    private int _selectedCount;
    public int SelectedCount
    {
        get => _selectedCount;
        set
        {
            _selectedCount = value;
            SelectedCountLabel.text = $"{_selectedCount}";
            TotalPrice = _price * _selectedCount;
        }
    }

    private float _totalPrice;
    public float TotalPrice
    {
        get => _totalPrice;
        set
        {
            _totalPrice = value;
            SelectedTotalLabel.text = $"${_totalPrice:F3}";
        }
    }

    void Start()
    {
        SelectedCount = 0;
    }
}
