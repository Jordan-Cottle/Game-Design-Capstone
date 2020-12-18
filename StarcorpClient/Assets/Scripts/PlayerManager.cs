using UnityEngine;
using UnityEngine.UI;

public class PlayerManager : MonoBehaviour
{
    public PlayerController Player;

    public ResourceManager ResourceManager;
    public ObjectManager ObjectManager;
    public CityManager CityManager;
    public CityPanelManager PanelManager;

    private float playerMoney;
    public Text playerMoneyLabel;

    public void Initialize(Socket socket)
    {
        socket.Register("object_moved", (ev) =>
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

        socket.Register("resources_sold", (ev) =>
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

    void OnGUI()
    {
        this.playerMoneyLabel.text = $"$ {this.playerMoney}";
    }
}
