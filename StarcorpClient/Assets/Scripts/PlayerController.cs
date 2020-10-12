using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    private Camera mainCamera;
    private HexGrid gameGrid;

    public string name;

    // Start is called before the first frame update
    void Start()
    {
        this.mainCamera = Camera.main;

        gameGrid = (HexGrid)FindObjectOfType(typeof(HexGrid));
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
