using System.Collections.Generic;

using UnityEngine;
using UnityEngine.UI;

public class CityPanelManager : MonoBehaviour
{
    private City activeCity;
    public Text CityNameLabel;
    public Text PopulationLabel;
    public TransactionLabel FoodLabel;
    public TransactionLabel WaterLabel;
    public TransactionLabel FuelLabel;

    public Text TotalLabel;
    public Text TotalPriceLabel;

    public ResourceManager ResourceManager;
    public PlayerManager PlayerManager;

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
    bool active;
    void Awake()
    {
        position = this.transform.position;
        Hide();
    }

    void OnGUI()
    {
        if (active)
        {
            LoadCity(activeCity);
        }
    }

    public void Hide()
    {
        this.transform.position = new Vector3(10000, 10000, 10000);
        active = false;
    }

    public void Show()
    {
        this.transform.position = position;
        active = true;
    }

    void SetUpSlider(TransactionLabel label, string resourceName)
    {
        if (Buy)
        {
            label.Selector.maxValue = label.Count;
        }
        else
        {
            int player_held = ResourceManager.resourcesCounts[resourceName];
            label.Selector.maxValue = player_held;
            label.Selector.value = player_held;
        }
    }

    void SetUpLabel(City city, TransactionLabel label, string resourceName)
    {
        int count = city.amounts[resourceName];
        float price = city.prices[resourceName];

        if (Buy)
        {
            price *= 2;
        }

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
        activeCity = city;
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

    public void Checkout(bool purchase)
    {
        Dictionary<string, int> chosen = new Dictionary<string, int>();
        chosen["food"] = FoodLabel.SelectedCount;
        chosen["water"] = WaterLabel.SelectedCount;
        chosen["fuel"] = FuelLabel.SelectedCount;

        if (purchase != Buy)
        {
            Buy = purchase;
            return;
        }

        if (purchase)
        {
            Debug.Log("Making purchase");
            PlayerManager.BuyResources(chosen, activeCity);
        }
        else
        {
            Debug.Log("Selling goods!");
            PlayerManager.SellResources(chosen, activeCity);
        }
    }
}
