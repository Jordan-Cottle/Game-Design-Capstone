using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using Newtonsoft.Json.Linq;

public class CityManager : MonoBehaviour
{
    private GameController controller;
    private CityPanelManager panelManager;

    public City cityPrefab;

    private Socket socket;

    public Dictionary<Position, City> cities;
    private int cityCount = 0;


    // Start is called before the first frame update
    void Start()
    {
        this.controller = GetComponent<GameController>();
        this.panelManager = FindObjectOfType<CityPanelManager>();

        this.cities = new Dictionary<Position, City>();
    }

    public void Initialize(Socket socket)
    {
        this.socket = socket;

        this.socket.Register("city_updated", (ev) =>
        {
            var data = ev.Data[0];
            Debug.Log($"Updating city with {data}");

            City city = this.controller.ObjectManager.Get("city", (string)data["id"]).GetComponent<City>();
            city.population = (int)data["population"];
            city.UpdateResources((JObject)data["resources"]);
        });
    }

    public City CreateCity(JObject data)
    {
        Debug.Log($"Creating city from {data}");
        Position position = new Position((string)data["position"]);
        Vector3 worldPos = controller.gameGrid.getWorldPosition(position);
        worldPos.z = -1;

        City city = Instantiate(cityPrefab, worldPos, Quaternion.identity);
        city.Initialize(data);

        this.controller.ObjectManager.Track("city", (string)data["id"], city.gameObject);
        this.cities.Add(position, city);

        return city;
    }
}
