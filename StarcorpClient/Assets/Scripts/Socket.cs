using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.SceneManagement;

using Dpoch.SocketIO;
using Newtonsoft.Json.Linq;

public class Socket : MonoBehaviour
{
    private const string API_URL = "http://lanparty.mynetgear.com:1234";
    private const string SOCKET_URL = "ws://lanparty.mynetgear.com:1234/socket.io/?EIO=4&transport=websocket";

    private SocketIO _socket;
    private string userID;
    private Dictionary<string, string> cookies;

    private Dictionary<string, Action<SocketIOEvent>> handlers;

    public bool ready = false;

    public SocketIO socket
    {
        get
        {
            if (this._socket is null)
            {
                this._socket = this.createSocket();
            }

            return this._socket;
        }
    }

    private SocketIO createSocket()
    {
        SocketIO socket = new SocketIO(SOCKET_URL);
        socket.OnOpen += () => Debug.Log("Socket open!");
        socket.OnConnectFailed += () => Debug.Log("Socket failed to connect!");
        socket.OnClose += () => Debug.Log("Socket closed!");
        socket.OnError += (err) => Debug.Log("Socket Error: " + err);

        this.cookies = new Dictionary<string, string>();
        this.handlers = new Dictionary<string, Action<SocketIOEvent>>();

        socket.Connect();
        return socket;
    }

    public void Awake()
    {
        DontDestroyOnLoad(this.gameObject);
    }

    public void Login(string email, string password)
    {
        Debug.Log("Logging in");

        this.Register("login_accepted", (ev) =>
        {
            var data = ev.Data[0];

            this.userID = (string)data["id"];

            this.AddCookie("id", this.userID);

            Debug.Log($"Logged in successfully with ID: {this.userID}");

            this.ready = true;
            this.UnRegister("login_accepted", this.handlers["login_accepted"]);

            this.Register("player_logout", (eve) =>
            {
                Debug.Log("Checking for client being logged out due to inactivity");
                string userID = (string)eve.Data[0]
            ["user_id"];

                Debug.Log($"This: {this.userID}, Other: {userID}");
                if (userID == this.userID)
                {
                    Debug.Log("Client inactive, shutting down socket.");
                    this.Close();

                    SceneManager.LoadScene("MainMenu");
                }
            });

            SceneManager.LoadScene("MainScene");
        });

        this.Emit("login", JObject.Parse($"{{'email': '{email}', 'password': '{password}'}}"));
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

        callBack(JObject.Parse(request.downloadHandler.text));
    }

    public void Register(string ev, Action<SocketIOEvent> handler)
    {
        this.socket.On(ev, handler);
        this.handlers[ev] = handler;
    }

    public void UnRegister(string ev, Action<SocketIOEvent> handler = null)
    {
        if (handler is null)
        {
            handler = this.handlers[ev];
        }
        this.socket.Off(ev, handler);
        this.handlers.Remove(ev);
    }

    public void Close()
    {
        Debug.Log("Closing socket!");
        this.socket.Close();
        this._socket = null;

    }
}
