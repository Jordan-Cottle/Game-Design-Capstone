using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using Newtonsoft.Json.Linq;

public class ResourceManager : MonoBehaviour
{
    private Dictionary<Position, Resource> resources;
    private Dictionary<string, int> resourcesCounts;
    private GameController controller;

    public Text display;

    Socket socket;
    // Start is called before the first frame update
    void Start()
    {
        this.resources = new Dictionary<Position, Resource>();
        this.resourcesCounts = new Dictionary<string, int>();

        // TODO make this better
        this.resourcesCounts["water"] = 0;
        this.resourcesCounts["food"] = 0;
        this.resourcesCounts["fuel"] = 0;

        this.controller = GetComponent<GameController>();
    }

    // Update is called once per frame
    public void Initialize(Socket socket)
    {
        this.socket = socket;

        this.socket.Register("resource_gathered", (ev) =>
        {
            var data = ev.Data[0];

            string resource_type = (string)data["resource_type"];
            int amount = (int)data["now_held"];
            Debug.Log($"Gathered {amount} {resource_type}");

            this.resourcesCounts[resource_type] = amount;
        });

        foreach (var resource in FindObjectsOfType<Resource>())
        {
            resource.Initialize();
            this.resources[resource.position] = resource;
        }
    }

    public void Set(string resourceType, int value)
    {
        this.resourcesCounts[resourceType] = value;
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

    void OnGUI()
    {
        this.display.text = this.ToString();
    }

    public override string ToString()
    {
        string output = "~~Resources~~\n";
        HashSet<string> displayed = new HashSet<string>();
        foreach (var resource in this.resources)
        {
            if (displayed.Contains(resource.Value.type))
            {
                continue;
            }
            output += $"{resource.Value.type} {this.resourcesCounts[resource.Value.type]}\n";
            displayed.Add(resource.Value.type);
        }

        this.display.text = output;
        return output;
    }
}
