using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Newtonsoft.Json.Linq;

public class ObjectManager : MonoBehaviour
{
    private Dictionary<string, GameObject> objects;

    public PlayerController playerPrefab;

    public void Start()
    {
        this.objects = new Dictionary<string, GameObject>();
    }

    public void SetUp(Socket socket)
    {
        socket.Register("object_moved", (ev) =>
        {
            var data = ev.Data[0];

            string uuid = (string)data["uuid"];

            Position position = new Position((string)data["destination"]);

            // TODO: Handle generically
            PlayerController player = this.Get(uuid).GetComponent<PlayerController>();
            player.JumpTo(position);
        });

        socket.Register("player_joined", (ev) =>
        {
            this.CreatePlayer((JObject)ev.Data[0]);
        });
    }

    public PlayerController CreatePlayer(JObject data)
    {
        string uuid = (string)data["uuid"];
        Position position = new Position((string)data["position"]);

        Debug.Log($"Setting up player with {position}");

        PlayerController player = Instantiate(this.playerPrefab, Vector3.zero, Quaternion.identity);
        player.JumpTo(position);

        this.Track(uuid, player.gameObject);

        return player;
    }

    public void Load(JArray data)
    {
        Debug.Log(data);
    }

    public void Track(string uuid, GameObject obj)
    {
        this.objects[uuid] = obj;
    }

    public GameObject Get(string uuid)
    {
        return this.objects[uuid];
    }
}
