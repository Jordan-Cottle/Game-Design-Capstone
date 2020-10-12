using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Transform))]
public class PlayerController : MonoBehaviour
{
    private Transform playerTransform;
    private Camera mainCamera;
    private HexGrid gameGrid;

    public string name;

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
        if (Input.GetMouseButtonDown(0))
        {
            Vector3 worldPosition = mainCamera.ScreenToWorldPoint(Input.mousePosition);

            GameTile t = gameGrid.getTile(worldPosition);

            Debug.Log($"{this.name} clicked on {t}!");
        }
    }
}
