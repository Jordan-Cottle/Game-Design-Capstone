using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

public enum TerrainType : int
{
    Space,
    Ground,
    Water,
    Star
}

public static class TerrtainTypeExtensions
{
    public static int movementCost(this TerrainType t)
    {
        switch (t)
        {
            case TerrainType.Space:
                return 2;
            case TerrainType.Ground:
                return 5;
            case TerrainType.Water:
                return 12;
            case TerrainType.Star:
                return 45;
            default:
                throw new System.ArgumentException($"Invalid TerrainType {t}");
        }
    }
    public static string name(this TerrainType t)
    {
        switch (t)
        {
            case TerrainType.Space:
                return "Space";
            case TerrainType.Ground:
                return "Ground";
            case TerrainType.Water:
                return "Water";
            case TerrainType.Star:
                return "Star";
            default:
                throw new System.ArgumentException($"Invalid TerrainType {t}");
        }
    }
}
[CreateAssetMenu]
public class TileData : ScriptableObject
{
    public TileBase[] tiles;

    public TerrainType terrainType;
    public string terrainName
    {
        get => terrainType.name();
    }
}