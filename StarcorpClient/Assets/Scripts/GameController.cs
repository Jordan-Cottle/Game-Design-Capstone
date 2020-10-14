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

    void Start()
    {
        this.mainCamera = Camera.main;

        this.socket = new Socket();
        this.objectManager = GetComponent<ObjectManager>();

        this.Initialize();
    }

    void Initialize()
    {
        this.objectManager.SetUp(this.socket);

        this.socket.Register("player_load", (ev) =>
        {
            this.player = this.objectManager.CreatePlayer((JObject)ev.Data[0]);


            this.mainCamera.transform.SetParent(this.player.transform, false);
        });

        socket.Login("UnityTest");
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            this.player.TravelTo(mainCamera.ScreenToWorldPoint(Input.mousePosition));
        }
    }
}
