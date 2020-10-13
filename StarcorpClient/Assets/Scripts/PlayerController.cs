using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Transform))]
public class PlayerController : MonoBehaviour
{
    public float maxSpeed = 5;

    private Transform playerTransform;
    private Camera mainCamera;
    private HexGrid gameGrid;

    public string playerName;

    bool moving = false;

    private Queue<Vector3> targets = new Queue<Vector3>();

    // Start is called before the first frame update
    void Start()
    {
        this.mainCamera = Camera.main;

        this.gameGrid = (HexGrid)FindObjectOfType(typeof(HexGrid));

        this.playerTransform = GetComponent<Transform>();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0) && !this.moving)
        {
            StartCoroutine(this.moveTo(mainCamera.ScreenToWorldPoint(Input.mousePosition)));
        }
    }

    IEnumerator moveTo(Vector3 worldPosition)
    {
        this.moving = true;
        List<Vector3> positions = new List<Vector3>();

        yield return StartCoroutine(this.gameGrid.path(this.playerTransform.position, worldPosition, positions));

        foreach (Vector3 position in positions)
        {
            this.targets.Enqueue(position);
        }
        yield return StartCoroutine(ChaseTargets());
        this.moving = false;
    }

    IEnumerator ChaseTargets()
    {
        while (this.targets.Count > 0)
        {
            Vector3 destination = this.targets.Dequeue();
            while (this.playerTransform.position != destination)
            {
                this.playerTransform.position = Vector3.MoveTowards(this.playerTransform.position, destination, this.maxSpeed * Time.deltaTime);
                yield return null;
            }
        }
    }
}
