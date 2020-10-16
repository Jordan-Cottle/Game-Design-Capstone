using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Resource : MonoBehaviour
{
    public string type;

    public Position position;
    public string pos; // TODO: Remove when Resources are loaded from server
    void Start()
    {
        this.position = new Position(pos);
        Debug.Log($"{this.type} at {this.position}");

    }

    public void Initialize()
    {
        HexGrid hexGrid = FindObjectOfType<HexGrid>();
        Vector3 worldPos = hexGrid.getWorldPosition(this.position);
        this.transform.position = worldPos;
    }
}
