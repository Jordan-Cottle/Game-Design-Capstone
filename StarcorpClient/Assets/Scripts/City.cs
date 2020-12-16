using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using Newtonsoft.Json.Linq;

public class City : MonoBehaviour
{
    public string id;
    public int population;
    public Dictionary<string, int> resources;

    public Text label;

    void Awake()
    {
        this.resources = new Dictionary<string, int>();
    }

    public void Initialize(JObject data)
    {
        string rss = "resources";
        Debug.Log($"Initializing with {data}");
        Debug.Log($"Resources: {data[rss]}");
        this.name = (string)data["name"];
        this.id = (string)data["id"];
        this.population = (int)data["population"];
        foreach (var pair in (JObject)data["resources"])
        {
            Debug.Log($"Setting {pair.Key}: {pair.Value}");
            this.resources[pair.Key] = (int)pair.Value;
        }
    }

    public void OnClick()
    {
        int food = this.resources["food"];
        Debug.Log($"{this.name}: {food} clicked!");
    }

    public void OnGUI()
    {
        this.label.text = this.ToString();
    }

    public override string ToString()
    {
        string s = $"{this.name} ({this.population})\n";

        foreach (var resource in this.resources)
        {
            s += $"{resource.Key}: {resource.Value}\n";
        }

        // TODO: Display demand and prices

        return s;
    }
}
