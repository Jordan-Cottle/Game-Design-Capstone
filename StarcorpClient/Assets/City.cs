using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Newtonsoft.Json.Linq;

public class City : MonoBehaviour
{
    public string uuid;
    public int population;
    public Dictionary<string, int> resources;

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
        this.uuid = (string)data["uuid"];
        this.population = (int)data["population"];
        foreach (var pair in (JObject)data["resources"])
        {
            Debug.Log($"Setting {pair.Key}: {pair.Value}");
            this.resources[pair.Key] = (int)pair.Value;
        }
    }

    public void OnClick()
    {
        int food = this.resources["Food"];
        Debug.Log($"{this.name}: {food} clicked!");
    }
}
