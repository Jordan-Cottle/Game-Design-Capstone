using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using Newtonsoft.Json.Linq;

public class City : MonoBehaviour
{
    public string id;
    public int population;
    public Dictionary<string, int> amounts;
    public Dictionary<string, float> prices;

    void Awake()
    {
        this.amounts = new Dictionary<string, int>();
        this.prices = new Dictionary<string, float>();
    }

    public void Initialize(JObject data)
    {
        Debug.Log($"Initializing with {data}");
        this.name = (string)data["name"];
        this.id = (string)data["id"];
        this.population = (int)data["population"];
        UpdateResources((JObject)data["resources"]);
    }

    public void UpdateResources(JObject resources)
    {
        foreach (var resource in resources)
        {
            string resource_name = (string)resource.Key;

            JObject resource_data = (JObject)resource.Value;
            int amount = (int)resource_data["amount"];
            float price = (float)resource_data["price"];
            Debug.Log($"Setting {resource_name} in {this}: Amount->{amount}, Price->{price}");
            this.amounts[resource_name] = amount;
            this.prices[resource_name] = price;
        }
    }
}
