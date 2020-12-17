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

    public Resource foodPrefab;
    public Resource waterPrefab;
    public Resource fuelPrefab;

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

    public Resource CreateResource(JObject data)
    {
        Debug.Log($"Creating resource from: {data}");

        string type = (string)data["type"];
        Resource resource;

        switch (type)
        {
            case "food":
                resource = this.foodPrefab;
                break;
            case "water":
                resource = this.waterPrefab;
                break;
            case "fuel":
                resource = this.fuelPrefab;
                break;
            default:
                throw new KeyNotFoundException($"Unrecognized resource type: {name}");
        }

        Position position = new Position((string)data["position"]);

        Debug.Log($"Creating {type} node at {position}");

        resource = Instantiate<Resource>(resource);
        resource.Initialize(position);

        this.resources[position] = resource;
        return resource;
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

        this.socket.Register("resource_exhausted", (ev) =>
        {
            var data = ev.Data[0];

            Position position = new Position((string)data["position"]);

            if (this.resources.ContainsKey(position))
            {
                Resource resource = this.resources[position];
                Debug.Log($"{resource} at {position} exhausted");

                Destroy(resource.gameObject);
                this.resources.Remove(position);
            }
            else
            {
                Debug.Log("WARNING: Server attempt to exhaust a non-existent resource");
            }
        });

        this.socket.Register("resource_generated", (ev) =>
        {
            this.CreateResource((JObject)ev.Data[0]);
        });
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
                Debug.Log($"Click on {resource} detected!");

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
        foreach (var resource in this.resourcesCounts)
        {
            output += $"{resource.Key} {resource.Value}\n";
        }

        this.display.text = output;
        return output;
    }
}
