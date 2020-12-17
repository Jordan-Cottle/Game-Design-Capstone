using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Transform))]
public class PlayerController : MonoBehaviour
{
    public float maxSpeed = 5;

    private HexGrid gameGrid;

    public string playerName;

    public bool moving = false;

    private Queue<Vector3> targets = new Queue<Vector3>();
    private Vector3 destination;

    void Awake()
    {
        this.gameGrid = FindObjectOfType<HexGrid>();
    }

    public void JumpTo(Position position)
    {
        Vector3 worldPos = this.gameGrid.getWorldPosition(position);
        worldPos.z = -1;
        this.transform.position = worldPos;
    }


    public void JumpTo(Vector3 destination)
    {
        this.transform.position = destination;
    }

    public void MoveTowards(Vector3 destination)
    {
        this.transform.position = Vector3.MoveTowards(this.transform.position, destination, this.maxSpeed * Time.deltaTime);
    }
}
