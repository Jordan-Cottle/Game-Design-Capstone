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

            string position = (string)data["position"];

            string[] args = position.Split(',');
            Vector3Int pos = new Vector3Int(0, 0, 0);
            pos.x = int.Parse(args[0]);
            pos.y = int.Parse(args[1]);
            pos.z = int.Parse(args[2]);

            // TODO: Handle generically
            PlayerController player = this.Get(uuid).GetComponent<PlayerController>();
            player.MoveTo(pos);
        });

        socket.Register("player_joined", (ev) =>
        {
            this.CreatePlayer((JObject)ev.Data[0]);
        });
    }

    public PlayerController CreatePlayer(JObject data)
    {
        string uuid = (string)data["uuid"];
        string position = (string)data["position"];

        string[] args = position.Split(',');
        Vector3Int pos = new Vector3Int(0, 0, 0);
        pos.x = int.Parse(args[0]);
        pos.y = int.Parse(args[1]);
        pos.z = int.Parse(args[2]);

        Debug.Log($"Setting up player with {pos}");

        PlayerController player = Instantiate(this.playerPrefab, Vector3.zero, Quaternion.identity);
        player.MoveTo(pos);

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
