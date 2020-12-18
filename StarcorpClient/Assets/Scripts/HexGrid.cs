using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;
using UnityEngine.UI;

using Newtonsoft.Json.Linq;

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
    private Dictionary<string, TileBase> tileNames;

    public TileBase space;
    public TileBase lush;
    public TileBase aquatic;
    public TileBase arid;
    public TileBase solar;

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

        this.tileNames = new Dictionary<string, TileBase>();
        this.tileNames["SPACE"] = space;
        this.tileNames["LUSH"] = lush;
        this.tileNames["AQUATIC"] = aquatic;
        this.tileNames["ARID"] = arid;
        this.tileNames["SOLAR"] = solar;
    }

    public void Initialize(JArray data)
    {
        Debug.Log($"Initializing tilemap with {data}");

        this.grid.ClearAllTiles();

        foreach (JObject tile in data)
        {
            Position position = new Position((string)tile["position"]);
            TileBase tileType = this.tileNames[(string)tile["type"]];
            this.grid.SetTile(position.cellPosition, tileType);
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
            Text label = Instantiate(textPrefab, this.grid.CellToWorld(cellPosition), Quaternion.identity, this.canvas.transform);
            label.text = $"({cellPosition.x}, {cellPosition.y})\n {pos}";
            this.labels[pos] = label;
        }
    }

    public TerrainType terrainType(GameTile tile)
    {
        TileBase tileBase = this.grid.GetTile(tile.cellPosition);

        if (tileBase is null)
        {
            return TerrainType.Space;
        }

        TileData data = this.tileTypeData[tileBase];

        return data.terrainType;
    }

    public GameTile getTile(Vector3 worldPosition)
    {
        Vector3Int coordinate = this.grid.WorldToCell(worldPosition);

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

    public Vector3 getWorldPosition(Position position)
    {
        return this.grid.CellToWorld(this.getTile(position).cellPosition);
    }

    public Vector3 getWorldPosition(GameTile tile)
    {
        return this.grid.CellToWorld(tile.cellPosition);
    }

    public Vector3 getWorldPosition(Vector3Int position)
    {
        return this.grid.CellToWorld(position);
    }
    public Vector3 getWorldPosition(Vector3 screenPosition)
    {
        Vector3 worldPosition = Camera.main.ScreenToWorldPoint(screenPosition);

        // Snap worldPosition to grid
        Vector3Int cellPosition = this.grid.WorldToCell(worldPosition);
        return this.grid.CellToWorld(cellPosition);
    }

    public List<GameTile> neighbors(GameTile tile)
    {
        List<Position> neighbors = tile.position.neighbors;

        List<GameTile> tiles = new List<GameTile>();
        foreach (Position neighbor in neighbors)
        {
            tiles.Add(this.getTile(neighbor));
        }

        return tiles;
    }

    public List<Position> path(Vector3 start, Vector3 end)
    {
        List<Position> path = new List<Position>();
        AStar aStar = new AStar(this, this.getTile(end));

        List<GameTile> tilePath = aStar.search(this.getTile(start));

        foreach (GameTile tile in tilePath)
        {
            path.Add(tile.position);
        }

        return path;
    }
}
