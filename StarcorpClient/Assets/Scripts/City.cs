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

        this.prices["food"] = 5;
        this.prices["water"] = 3;
        this.prices["fuel"] = 25;
    }

    public void Initialize(JObject data)
    {
        Debug.Log($"Initializing with {data}");
        this.name = (string)data["name"];
        this.id = (string)data["id"];
        this.population = (int)data["population"];

        var resources = (JObject)data["resources"];
        foreach (var pair in resources)
        {
            Debug.Log($"Setting {pair.Key}: {pair.Value}");
            this.amounts[pair.Key] = (int)pair.Value;
        }
    }
}
