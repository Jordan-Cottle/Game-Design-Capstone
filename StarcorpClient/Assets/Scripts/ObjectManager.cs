using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Newtonsoft.Json.Linq;

public class ObjectManager : MonoBehaviour
{
    private Dictionary<string, Dictionary<string, GameObject>> objects;

    public PlayerController playerPrefab;

    public void Start()
    {
        this.objects = new Dictionary<string, Dictionary<string, GameObject>>();

        this.objects["player"] = new Dictionary<string, GameObject>();
        this.objects["city"] = new Dictionary<string, GameObject>();
    }

    public void SetUp(Socket socket)
    {
        socket.Register("object_moved", (ev) =>
        {
            var data = ev.Data[0];

            string id = (string)data["id"];

            Position position = new Position((string)data["position"]);

            // TODO: Handle generically
            PlayerController player = this.Get("player", id).GetComponent<PlayerController>();
            player.JumpTo(position);
        });

        socket.Register("player_joined", (ev) =>
        {
            this.CreatePlayer((JObject)ev.Data[0]);
        });
    }

    public PlayerController CreatePlayer(JObject data)
    {
        string id = (string)data["id"];
        Position position = new Position((string)data["position"]);

        Debug.Log($"Setting up player {id} with {position}");

        PlayerController player = Instantiate(this.playerPrefab, Vector3.zero, Quaternion.identity);
        player.JumpTo(position);

        this.Track("player", id, player.gameObject);

        return player;
    }

    public void Load(JArray data)
    {
        Debug.Log(data);
    }

    public void Track(string type, string id, GameObject obj)
    {
        this.objects[type][id] = obj;
    }

    public GameObject Get(string type, string id)
    {
        return this.objects[type][id];
    }
}
