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

    public void Login(string playerName)
    {
        Debug.Log("Logging in");

        this.Register("login_accepted", (ev) =>
        {
            var data = ev.Data[0];

            Debug.Log(data);
            this.sessionID = (string)data["session_id"];

            Debug.Log($"Logged in successfully with {sessionID}");

            this.Emit("player_load", new JObject());
        });

        this.socket.Connect();
        this.socket.Emit("login_request", JObject.Parse($"{{'name': '{playerName}'}}"));
    }

    public void Emit(string ev, JObject data)
    {
        data["session_id"] = this.sessionID;

        this.socket.Emit(ev, data);
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
