using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Dpoch.SocketIO;

public class NetworkController : MonoBehaviour
{
    // Start is called before the first frame update

    private SocketIO socket;

    public
    void Start()
    {
        socket = new SocketIO("ws://lanparty.mynetgear.com:1234/socket.io/?EIO=4&transport=websocket");

        socket.OnOpen += () => Debug.Log("Socket open!");
        socket.OnConnectFailed += () => Debug.Log("Socket failed to connect!");
        socket.OnClose += () => Debug.Log("Socket closed!");
        socket.OnError += (err) => Debug.Log("Socket Error: " + err);

        socket.On("login_accepted", (ev) =>
        {
            var data = ev.Data;
            Debug.Log(data);
        });

        socket.Connect();
        socket.Emit("loginRequest", "{\"name\": \"Unity\"}");
    }

    void OnDestroy()
    {
        socket.Close();
    }
}
