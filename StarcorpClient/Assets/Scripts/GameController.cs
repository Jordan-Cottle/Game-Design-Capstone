using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameController : MonoBehaviour
{
    // Start is called before the first frame update
    public PlayerController player;

    private Camera mainCamera;

    private Socket socket;
    private ObjectManager objectManager;

    void Start()
    {
        this.mainCamera = Camera.main;

        this.socket = new Socket();
        this.objectManager = new ObjectManager();

        this.Initialize();
    }

    void Initialize()
    {
        socket.Login(this.player);
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            this.player.MoveTo(mainCamera.ScreenToWorldPoint(Input.mousePosition));
        }
    }
}
