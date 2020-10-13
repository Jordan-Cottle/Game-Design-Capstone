using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;
using UnityEngine.UI;

[RequireComponent(typeof(Tilemap))]
public class HexGrid : MonoBehaviour
{
    private Tilemap grid;
    private Dictionary<Position, GameTile> tiles;
    private Dictionary<Position, Text> labels;

    [SerializeField]
    private TileData[] tileTypes;

    public Canvas canvas;
    public Text textPrefab;
    private int foundCounter = 0;

    private Dictionary<TileBase, TileData> tileTypeData;
    void Start()
    {
        this.tiles = new Dictionary<Position, GameTile>();
        this.labels = new Dictionary<Position, Text>();

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

    void Update()
    {
        Vector3 worldPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);

        Vector3Int cellPosition = this.grid.WorldToCell(worldPosition);

        worldPosition.z = 0;

        Position pos = new Position(cellPosition);
        if (!this.labels.ContainsKey(pos))
        {
            Debug.Log($"Cell position: ({cellPosition.x}, {cellPosition.y})::{worldPosition}");
            Text label = Instantiate(textPrefab, this.grid.CellToWorld(cellPosition), Quaternion.identity, this.canvas.transform);
            label.text = $"({cellPosition.x}, {cellPosition.y})\n {pos}";
            this.labels[pos] = label;
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

    public Text getLabel(GameTile tile)
    {
        Text label;
        if (!this.labels.ContainsKey(tile.position))
        {
            label = Instantiate(textPrefab, this.getWorldPosition(tile), Quaternion.identity, this.canvas.transform);
            label.text = $"{this.foundCounter++}: {tile.position}\n{tile.cellPosition}";
            this.labels[tile.position] = label;
        }
        else
        {
            label = this.labels[tile.position];
        }

        return label;
    }

    public Vector3 getWorldPosition(GameTile tile)
    {
        return this.grid.CellToWorld(tile.cellPosition);
    }
}
