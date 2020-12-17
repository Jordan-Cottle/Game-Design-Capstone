using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Resource : MonoBehaviour
{
    public string type;

    public Position position;

    public void Initialize(Position position)
    {
        this.position = position;
        HexGrid hexGrid = FindObjectOfType<HexGrid>();
        Vector3 worldPos = hexGrid.getWorldPosition(this.position);
        worldPos.z = -0.25f;
        this.transform.position = worldPos;
    }
}
