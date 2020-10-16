using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Newtonsoft.Json.Linq;

public class CityManager : MonoBehaviour
{
    private GameController controller;

    public City cityPrefab;

    private Dictionary<Position, City> cities;

    // Start is called before the first frame update
    void Start()
    {
        this.controller = GetComponent<GameController>();

        this.cities = new Dictionary<Position, City>();
    }

    public void Initialize(Socket socket)
    {
        socket.Register("load_city", (ev) =>
        {
            var data = ev.Data[0];

            this.CreateCity((JObject)data);
        });

        socket.Emit("get_cities");
    }

    void CreateCity(JObject data)
    {
        Position position = new Position((string)data["position"]);


        Vector3 worldPos = controller.gameGrid.getWorldPosition(position);

        City city = Instantiate(cityPrefab, worldPos, Quaternion.identity);

        city.Initialize(data);

        this.controller.ObjectManager.Track((string)data["uuid"], city.gameObject);
        this.cities.Add(position, city);
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(1))
        {
            Debug.Log($"Processing click at {Input.mousePosition}");
            Position pos = this.controller.gameGrid.getTile(Camera.main.ScreenToWorldPoint(Input.mousePosition)).position;
            Debug.Log($"Processing click at cube pos {pos}");

            City city;
            if (this.cities.ContainsKey(pos))
            {
                city = this.cities[pos];

                city.OnClick();
            }
        }
    }
}
