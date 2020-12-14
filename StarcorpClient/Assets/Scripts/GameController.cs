using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Newtonsoft.Json.Linq;

[RequireComponent(typeof(ObjectManager))]
public class GameController : MonoBehaviour
{
    // Start is called before the first frame update
    private PlayerController player;

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
    public HexGrid gameGrid;

    void Start()
    {
        this.mainCamera = Camera.main;

        this.socket = GetComponent<Socket>();
        this.objectManager = GetComponent<ObjectManager>();
        this.gameGrid = FindObjectOfType<HexGrid>();

        this.CityManager = GetComponent<CityManager>();
        this.ResourceManager = GetComponent<ResourceManager>();

        this.Initialize();
    }

    void Initialize()
    {
        this.objectManager.SetUp(this.socket);

        this.socket.Register("player_load", (ev) =>
        {
            this.player = this.objectManager.CreatePlayer((JObject)ev.Data[0]);


            this.mainCamera.transform.SetParent(this.player.transform, false);

            this.CityManager.Initialize(this.socket);
            this.ResourceManager.Initialize(this.socket);
        });

        this.socket.Register("player_logout", (ev) =>
        {
            Debug.Log("Processing logout event");
            string uuid = (string)ev.Data[0]["uuid"];

            Destroy(this.objectManager.Get(uuid));
        });

        this.socket.Login($"UnityTest{Random.value}", "12345");
    }

    IEnumerator MovePlayerTo(Vector3 screenPosition)
    {
        Vector3 start;
        if (this.player.moving)
        {
            yield break;
        }

        start = this.player.transform.position;

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
        if (Input.GetMouseButtonDown(0))
        {
            StartCoroutine(this.MovePlayerTo(Input.mousePosition));
        }
    }

    void OnApplicationQuit()
    {
        this.socket.Emit("logout");
        // this.socket.Close();
    }
}
