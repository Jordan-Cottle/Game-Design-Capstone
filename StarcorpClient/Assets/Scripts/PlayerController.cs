using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Transform))]
public class PlayerController : MonoBehaviour
{
    public float maxSpeed = 5;

    private HexGrid gameGrid;

    public string playerName;

    bool moving = false;

    private Queue<Vector3> targets = new Queue<Vector3>();
    private Vector3 destination;

    void Awake()
    {
        this.gameGrid = FindObjectOfType<HexGrid>();
    }

    public void MoveTo(Vector3Int position)
    {
        Position p = new Position(position);
        this.transform.position = this.gameGrid.getWorldPosition(p);
    }

    public void TravelTo(Vector3 worldPosition)
    {
        Vector3 start;
        if (this.moving)
        {
            start = this.destination;
        }
        else
        {
            start = this.transform.position;
        }

        List<Vector3> positions = this.gameGrid.path(start, worldPosition);

        foreach (Vector3 position in positions)
        {
            this.targets.Enqueue(position);
            this.destination = position;
        }

        if (!this.moving)
        {
            StartCoroutine(ChaseTargets());
        }
    }

    IEnumerator ChaseTargets()
    {
        this.moving = true;
        while (this.targets.Count > 0)
        {
            Vector3 destination = this.targets.Dequeue();
            while (this.transform.position != destination)
            {
                this.transform.position = Vector3.MoveTowards(this.transform.position, destination, this.maxSpeed * Time.deltaTime);
                yield return null;
            }
        }
        this.moving = false;
    }
}
