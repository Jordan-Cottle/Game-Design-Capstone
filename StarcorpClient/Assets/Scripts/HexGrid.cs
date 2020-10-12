using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

[RequireComponent(typeof(Tilemap))]
public class HexGrid : MonoBehaviour
{
    private Tilemap grid;
    private Dictionary<Position, GameTile> tiles;

    [SerializeField]
    private TileData[] tileTypes;

    private Dictionary<TileBase, TileData> tileTypeData;
    void Start()
    {
        this.tiles = new Dictionary<Position, GameTile>();

        this.grid = this.GetComponent<Tilemap>();
    }

    void Awake()
    {
        this.tileTypeData = new Dictionary<TileBase, TileData>();
        foreach (var tileData in this.tileTypes)
        {
            foreach (var tile in tileData.tiles)
            {
                tileTypeData[tile] = tileData;
            }
        }
    }

    public GameTile getTile(Vector3 worldPosition)
    {
        Vector3Int coordinate = grid.WorldToCell(worldPosition);
        int row = coordinate.y;
        int col = coordinate.x;

        TileBase tile = grid.GetTile(coordinate);
        TileData data = this.tileTypeData[tile];


        Position pos = new Position(row, col);
        print($"{tile} at {pos} is a {data.type}");

        GameTile found;
        if (!this.tiles.ContainsKey(pos))
        {
            Debug.Log($"No tile currently tracked at: ({row}, {col})");
            found = new GameTile(new Position(row, col), 0);
            this.tiles[pos] = found;
        }
        else
        {
            found = this.tiles[pos];
            Debug.Log($"Found {found} at ({row}, {col})");
        }

        found.clickedCount += 1;

        Debug.Log($"{found} clicked {found.clickedCount} times!");

        return found;
    }
}
