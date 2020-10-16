using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

using Dpoch.SocketIO;
using Newtonsoft.Json.Linq;

public class Socket : MonoBehaviour
{
    private const string API_URL = "http://lanparty.mynetgear.com:1234";
    private const string SOCKET_URL = "ws://lanparty.mynetgear.com:1234/socket.io/?EIO=4&transport=websocket";

    private SocketIO socket;
    private string userID;
    private Dictionary<string, string> cookies;

    public bool ready = false;

    public void Awake()
    {
        this.socket = new SocketIO(SOCKET_URL);
        this.cookies = new Dictionary<string, string>();

        this.socket.OnOpen += () => Debug.Log("Socket open!");
        this.socket.OnConnectFailed += () => Debug.Log("Socket failed to connect!");
        this.socket.OnClose += () => Debug.Log("Socket closed!");
        this.socket.OnError += (err) => Debug.Log("Socket Error: " + err);
    }

    IEnumerator KeepAlive() // TODO: Remove this when proper auto logout event from server is implemented
    {
        while (true)
        {
            this.Emit("check_in");
            yield return new WaitForSeconds(20);
        }
    }

    public void Login(string playerName)
    {
        Debug.Log("Logging in");

        this.Register("login_accepted", (ev) =>
        {
            var data = ev.Data[0];

            Debug.Log(data);
            this.userID = (string)data["id"];

            this.AddCookie("id", this.userID);

            Debug.Log($"Logged in successfully with {this.userID}");

            this.Emit("player_load");

            StartCoroutine(this.KeepAlive());
        });

        this.socket.Connect();
        this.Emit("login", JObject.Parse($"{{'name': '{playerName}'}}"));
    }

    private void AddCookie(string key, string value)
    {
        if (this.cookies.ContainsKey(key) && this.cookies[key] == value)
        {
            return;
        }

        this.cookies[key] = value;
    }

    public void Emit(string ev, JObject data)
    {
        foreach (var pair in this.cookies)
        {
            data[pair.Key] = pair.Value;
        }

        this.socket.Emit(ev, data);
    }
    public void Emit(string ev)
    {
        JObject data = new JObject();
        foreach (var pair in this.cookies)
        {
            data[pair.Key] = pair.Value;
        }

        this.socket.Emit(ev, data);
    }

    public void Post(string url, WWWForm form, Action<JObject> callBack)
    {
        UnityWebRequest post = UnityWebRequest.Post($"{API_URL}/{url}", form);

        StartCoroutine(this.execute(post, callBack));
    }

    public void Get(string url, Action<JObject> callBack)
    {
        UnityWebRequest get = UnityWebRequest.Get($"{API_URL}/{url}");

        StartCoroutine(this.execute(get, callBack));

    }

    private IEnumerator execute(UnityWebRequest request, Action<JObject> callBack)
    {
        foreach (var pair in this.cookies)
        {
            request.SetRequestHeader(pair.Key, pair.Value);
        }

        yield return request.SendWebRequest();

        string results = request.downloadHandler.text;
        Debug.Log(results);

        callBack(JObject.Parse(results));
    }

    public void Register(string ev, Action<SocketIOEvent> handler)
    {
        this.socket.On(ev, handler);
    }

    public void Close()
    {
        this.socket.Close();
    }
}
