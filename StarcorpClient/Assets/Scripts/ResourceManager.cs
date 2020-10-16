using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using Newtonsoft.Json.Linq;

public class ResourceManager : MonoBehaviour
{
    private Dictionary<Position, Resource> resources;
    private GameController controller;

    public Text display;

    Socket socket;
    // Start is called before the first frame update
    void Start()
    {
        this.resources = new Dictionary<Position, Resource>();

        this.controller = GetComponent<GameController>();
    }

    // Update is called once per frame
    public void Initialize(Socket socket)
    {
        this.socket = socket;

        this.socket.Register("resource_gathered", (ev) =>
        {
            Debug.Log($"Resources gathered: {ev.Data[0]}");
            JObject resources = (JObject)ev.Data[0]["resources"];

            string output = "~~Resources~~\n";
            foreach (var resource in resources)
            {
                output += $"{resource.Value} {resource.Key}\n";
            }

            this.display.text = output;
        });

        foreach (var resource in FindObjectsOfType<Resource>())
        {
            resource.Initialize();
            this.resources[resource.position] = resource;
        }
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(1))
        {
            Debug.Log($"Processing click at {Input.mousePosition}");
            Position pos = this.controller.gameGrid.getTile(Camera.main.ScreenToWorldPoint(Input.mousePosition)).position;
            Debug.Log($"Processing click at cube pos {pos}");

            Resource resource;
            if (this.resources.ContainsKey(pos))
            {
                resource = this.resources[pos];

                JObject obj = new JObject();

                obj["target"] = resource.position.json;
                this.socket.Emit("gather_resource", obj);
            }
        }
    }
}
