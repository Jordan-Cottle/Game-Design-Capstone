using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

using Newtonsoft.Json.Linq;

[RequireComponent(typeof(ObjectManager))]
public class GameController : MonoBehaviour
{
    private Camera mainCamera;

    private Socket socket;
    private ObjectManager objectManager;

    public ObjectManager ObjectManager
    {
        get => this.objectManager;
    }

    public CityManager CityManager
    {
        get; private set;
    }

    public ResourceManager ResourceManager
    {
        get; private set;
    }

    public PlayerManager PlayerManager
    {
        get; private set;
    }
    public HexGrid gameGrid;

    void Start()
    {
        this.mainCamera = Camera.main;

        this.socket = FindObjectOfType<Socket>();
        this.objectManager = GetComponent<ObjectManager>();
        this.gameGrid = FindObjectOfType<HexGrid>();

        this.CityManager = GetComponent<CityManager>();
        this.ResourceManager = GetComponent<ResourceManager>();
        this.PlayerManager = GetComponent<PlayerManager>();

        this.Initialize();
    }

    void Initialize()
    {
        this.objectManager.SetUp(this.socket);
        this.CityManager.Initialize(this.socket);
        this.ResourceManager.Initialize(this.socket);
        PlayerManager.Initialize(this.socket);

        this.socket.Register("player_load", (ev) =>
        {
            PlayerController player = this.objectManager.CreatePlayer((JObject)ev.Data[0]);
            this.mainCamera.transform.SetParent(player.transform, false);

            PlayerManager.Player = player;
        });

        this.socket.Register("player_logout", (ev) =>
        {
            Debug.Log("Processing logout event");
            string id = (string)ev.Data[0];

            Destroy(this.objectManager.Get("player", id));
        });

        this.socket.Register("sector_load", (ev) =>
        {
            var data = ev.Data[0];
            Debug.Log($"Loading sector from {data}");

            this.gameGrid.Initialize((JArray)data["tiles"]);

            foreach (var city in data["cities"])
            {
                this.CityManager.CreateCity((JObject)city);
            }

            foreach (var resource_node in data["resource_nodes"])
            {
                this.ResourceManager.CreateResource((JObject)resource_node);
            }

        });

        this.socket.Emit("player_load");
        this.socket.Emit("load_sector");
    }

    IEnumerator MovePlayerTo(Vector3 screenPosition)
    {
        PlayerController player = PlayerManager.Player;
        Vector3 start;
        if (player.moving)
        {
            yield break;
        }

        start = player.transform.position;

        List<Position> positions = this.gameGrid.path(start, Camera.main.ScreenToWorldPoint(screenPosition));

        player.moving = true;
        foreach (Position position in positions)
        {
            JObject json = new JObject();
            json["destination"] = position.json;
            this.socket.Emit("player_move", json);

            yield return new WaitForSeconds(0.25f);

            if (!player.moving)
            {
                yield break;
            }
        }
        player.moving = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0) && !EventSystem.current.IsPointerOverGameObject())
        {
            StartCoroutine(this.MovePlayerTo(Input.mousePosition));
        }
    }

    void OnApplicationQuit()
    {
        this.socket.Emit("logout");
        this.socket.Close();
    }
}
