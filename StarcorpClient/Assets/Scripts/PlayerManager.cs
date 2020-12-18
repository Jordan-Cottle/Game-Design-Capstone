using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using Newtonsoft.Json.Linq;

public class PlayerManager : MonoBehaviour
{
    public PlayerController Player;

    public ResourceManager ResourceManager;
    public ObjectManager ObjectManager;
    public CityManager CityManager;
    public CityPanelManager PanelManager;

    private Socket Socket;
    private float playerMoney;
    public Text playerMoneyLabel;

    public void Initialize(Socket socket)
    {
        Socket = socket;
        Socket.Register("object_moved", (ev) =>
        {
            var data = ev.Data[0];

            string id = (string)data["id"];

            Position position = new Position((string)data["position"]);

            PlayerController player = ObjectManager.Get("player", id).GetComponent<PlayerController>();

            if (player != Player)
            {
                return;
            }

            if (CityManager.cities.ContainsKey(position))
            {
                PanelManager.LoadCity(CityManager.cities[position]);
            }
            else
            {
                PanelManager.Hide();
            }
        });

        Socket.Register("resources_sold", (ev) =>
        {
            var data = ev.Data[0];

            playerMoney = (float)data["new_balance"];
            var resourceType = (string)data["resource_type"];

            Debug.Log($"Sold {resourceType} to city");

            ResourceManager.Set(resourceType, (int)data["now_held"]);

            City city = ObjectManager.Get("city", (string)data["city_id"]).GetComponent<City>();
            city.amounts[resourceType] = (int)data["city_held"];
        });
    }

    public void SellResources(Dictionary<string, int> resources, City city)
    {
        JObject data = new JObject();

        data["city_id"] = city.id;
        foreach (var resource in resources)
        {
            Debug.Log($"Selling {resource.Value} {resource.Key} to {city}");
            data[resource.Key] = resource.Value;
        }

        Socket.Emit("sell_resources", data);
    }

    void OnGUI()
    {
        this.playerMoneyLabel.text = $"$ {this.playerMoney}";
    }
}
