﻿using System.Collections.Generic;

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
    void Awake()
    {
        position = this.transform.position;
        Hide();
    }

    public void Hide()
    {
        this.transform.position = new Vector3(10000, 10000, 10000);
    }

    public void Show()
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
            label.Selector.maxValue = ResourceManager.resourcesCounts[resourceName];
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
        }
        else
        {
            Debug.Log("Selling goods!");
            PlayerManager.SellResources(chosen, activeCity);
        }
    }
}
