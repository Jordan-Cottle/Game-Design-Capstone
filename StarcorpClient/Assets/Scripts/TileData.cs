using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;


[CreateAssetMenu]
public class TileData : ScriptableObject
{
    public TileBase[] tiles;

    public int terrainType;

    public static readonly string[] TYPES = { "Space", "Ground", "Water", "Star" };

    public string type
    {
        get => TYPES[this.terrainType];
    }
}