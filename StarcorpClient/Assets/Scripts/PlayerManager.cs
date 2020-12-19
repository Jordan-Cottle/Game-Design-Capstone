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
    public UpgradePanelManager UpgradePanelManager;

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
                UpgradePanelManager.Show();
            }
            else
            {
                PanelManager.Hide();
                UpgradePanelManager.Hide();
            }
        });

        Socket.Register("resources_sold", (ev) =>
        {
            var data = ev.Data[0];

            playerMoney = (float)data["new_balance"];
            var resourceType = (string)data["resource_type"];

            Debug.Log($"Sold {resourceType} to city");

            ResourceManager.Set(resourceType, (int)data["now_held"]);

            var cityData = (JObject)data["city"];

            City city = ObjectManager.Get("city", (string)cityData["id"]).GetComponent<City>();

            var resourceData = (JObject)cityData["resources"];
            city.amounts[resourceType] = (int)resourceData[resourceType]["amount"];
            city.prices[resourceType] = (float)resourceData[resourceType]["price"];
        });

        Socket.Register("resources_purchased", (ev) =>
        {
            var data = ev.Data[0];

            playerMoney = (float)data["new_balance"];
            var resourceType = (string)data["resource_type"];

            Debug.Log($"Purchased {resourceType} from city");

            ResourceManager.Set(resourceType, (int)data["now_held"]);

            var cityData = (JObject)data["city"];

            City city = ObjectManager.Get("city", (string)cityData["id"]).GetComponent<City>();

            var resourceData = (JObject)cityData["resources"];
            city.amounts[resourceType] = (int)resourceData[resourceType]["amount"];
            city.prices[resourceType] = (float)resourceData[resourceType]["price"];
        });

        Socket.Register("player_load", (ev) =>
        {
            var data = ev.Data[0];
            UpgradePanelManager.Initialize((JArray)data["systems"]);
            Position position = new Position((string)data["position"]);

            if (CityManager.cities.ContainsKey(position))
            {
                PanelManager.LoadCity(CityManager.cities[position]);
                UpgradePanelManager.Show();
            }
            else
            {
                PanelManager.Hide();
                UpgradePanelManager.Hide();
            }
        });
    }

    public void SellResources(Dictionary<string, int> resources, City city)
    {
        JObject data = new JObject();

        data["city_id"] = city.id;
        data["resources"] = JConstructor.FromObject(resources);
        Socket.Emit("sell_resources", data);
    }

    public void BuyResources(Dictionary<string, int> resources, City city)
    {
        JObject data = new JObject();

        data["city_id"] = city.id;
        data["resources"] = JConstructor.FromObject(resources);
        Socket.Emit("buy_resources", data);
    }
    void OnGUI()
    {
        this.playerMoneyLabel.text = $"$ {this.playerMoney}";
    }
}
