using UnityEngine;
using UnityEngine.UI;

public class CityPanelManager : MonoBehaviour
{
    // Start is called before the first frame update

    public Text CityNameLabel;
    public Text PopulationLabel;
    public TransactionLabel FoodLabel;
    public TransactionLabel WaterLabel;
    public TransactionLabel FuelLabel;

    public Text TotalLabel;
    public Text TotalPriceLabel;

    public ResourceManager resourceManager;

    private bool _buy = false;
    public bool Buy
    {
        get => _buy; set
        {
            _buy = value;
            if (_buy)
            {
                TotalLabel.color = Color.red;
                TotalPriceLabel.color = Color.red;
            }
            else
            {
                TotalLabel.color = Color.green;
                TotalPriceLabel.color = Color.green;
            }

            SetUpSlider(FoodLabel, "food");
            SetUpSlider(WaterLabel, "water");
            SetUpSlider(FuelLabel, "fuel");
        }
    }

    private float totalPrice;

    private Vector3 position;
    void Awake()
    {
        position = this.transform.position;
        Hide();
    }

    void Hide()
    {
        this.transform.position = new Vector3(10000, 10000, 10000);
    }

    void Show()
    {
        this.transform.position = position;
    }

    void SetUpSlider(TransactionLabel label, string resourceName)
    {
        if (Buy)
        {
            label.Selector.maxValue = label.Count;
        }
        else
        {
            label.Selector.maxValue = resourceManager.resourcesCounts[resourceName];
        }
    }

    void SetUpLabel(City city, TransactionLabel label, string resourceName)
    {
        int count = city.amounts[resourceName];
        float price = city.prices[resourceName];

        label.Count = count;
        label.Price = price;

        SetUpSlider(label, resourceName);
    }

    void UpdateTotal()
    {
        totalPrice = 0;
        totalPrice += FoodLabel.TotalPrice;
        totalPrice += WaterLabel.TotalPrice;
        totalPrice += FuelLabel.TotalPrice;

        TotalPriceLabel.text = $"${totalPrice:F3}";
    }

    public void LoadCity(City city)
    {
        CityNameLabel.text = city.name;
        PopulationLabel.text = $"Population: {city.population}";

        SetUpLabel(city, FoodLabel, "food");
        SetUpLabel(city, WaterLabel, "water");
        SetUpLabel(city, FuelLabel, "fuel");

        UpdateTotal();
        Show();
    }

    public void SelectFood(int amount)
    {
        FoodLabel.SelectedCount = (int)FoodLabel.Selector.value;
        UpdateTotal();
    }
    public void SelectWater(int amount)
    {
        WaterLabel.SelectedCount = (int)WaterLabel.Selector.value;
        UpdateTotal();
    }
    public void SelectFuel(int amount)
    {
        FuelLabel.SelectedCount = (int)FuelLabel.Selector.value;
        UpdateTotal();
    }
}
