using System;
using UnityEngine;

using Dpoch.SocketIO;
using Newtonsoft.Json.Linq;

public class Socket
{
    private const string URL = "ws://lanparty.mynetgear.com:1234/socket.io/?EIO=4&transport=websocket";

    private SocketIO socket;
    private string sessionID;


    public Socket()
    {
        this.socket = new SocketIO(URL);

        this.socket.OnOpen += () => Debug.Log("Socket open!");
        this.socket.OnConnectFailed += () => Debug.Log("Socket failed to connect!");
        this.socket.OnClose += () => Debug.Log("Socket closed!");
        this.socket.OnError += (err) => Debug.Log("Socket Error: " + err);
    }

    public void Login(PlayerController player)
    {
        Debug.Log("Logging in");
        this.socket.On("login_accepted", (ev) =>
        {
            var data = ev.Data[0];

            Debug.Log(data);
            this.sessionID = (string)data["session_id"];

            Debug.Log($"Logged in successfully with {sessionID}");
            string position = (string)data["player"]["position"];

            string[] args = position.Split(',');
            Vector3Int pos = new Vector3Int(0, 0, 0);
            pos.x = int.Parse(args[0]);
            pos.y = int.Parse(args[1]);
            pos.z = int.Parse(args[2]);

            Debug.Log($"Setting up player with {pos}");
            player.SetUp(pos);
        });

        this.socket.Connect();
        this.socket.Emit("login_request", $"{{\"name\": \"{player.playerName}\"}}");
    }

    public void Register(string ev, Action<SocketIOEvent> handler)
    {
        this.socket.On(ev, handler);
    }

    void Close()
    {
        socket.Close();
    }
}
