using UnityEngine;

public class PlayerManager : MonoBehaviour
{
    public PlayerController Player;

    public ObjectManager ObjectManager;
    public CityManager CityManager;
    public CityPanelManager PanelManager;

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
    }
}
