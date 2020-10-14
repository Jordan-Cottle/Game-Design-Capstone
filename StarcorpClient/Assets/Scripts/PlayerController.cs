﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Transform))]
public class PlayerController : MonoBehaviour
{
    public float maxSpeed = 5;

    private Transform playerTransform;
    private HexGrid gameGrid;

    public string playerName;

    bool moving = false;

    private Queue<Vector3> targets = new Queue<Vector3>();
    private Vector3 destination;

    // Start is called before the first frame update
    void Start()
    {
        this.gameGrid = (HexGrid)FindObjectOfType(typeof(HexGrid));

        this.playerTransform = GetComponent<Transform>();
    }

    public void SetUp(Vector3Int position)
    {
        this.gameGrid.getWorldPosition(position);
        this.playerTransform.position = position;
    }

    public void MoveTo(Vector3 worldPosition)
    {
        Vector3 start;
        if (this.moving)
        {
            start = this.destination;
        }
        else
        {
            start = this.playerTransform.position;
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
            while (this.playerTransform.position != destination)
            {
                this.playerTransform.position = Vector3.MoveTowards(this.playerTransform.position, destination, this.maxSpeed * Time.deltaTime);
                yield return null;
            }
        }
        this.moving = false;
    }
}
