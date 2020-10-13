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

    public TerrainType terrainType(GameTile tile)
    {
        TileBase tileBase = this.grid.GetTile(tile.cellPosition);
        TileData data = this.tileTypeData[tileBase];

        return data.terrainType;
    }

    public GameTile getTile(Vector3 worldPosition)
    {
        Vector3Int coordinate = grid.WorldToCell(worldPosition);
        int row = coordinate.y;
        int col = coordinate.x;

        Position pos = new Position(coordinate);

        return this.getTile(pos);
    }

    public GameTile getTile(Position pos)
    {
        GameTile found;
        if (!this.tiles.ContainsKey(pos))
        {
            found = new GameTile(pos, this);
            this.tiles[pos] = found;
        }
        else
        {
            found = this.tiles[pos];
        }

        found.clickedCount += 1;

        return found;
    }

    public Vector3 getWorldPosition(GameTile tile)
    {
        return this.grid.CellToWorld(tile.cellPosition);
    }
}
