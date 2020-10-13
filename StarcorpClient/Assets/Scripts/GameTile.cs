using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

/*
    Represent the hexagonal grid as axial coordinates

    Rows are indexed by the X coordinate

    Columns are indexed by the Y coordinate

    When needed, the third axial coordinate Z is calculated by
        Z = -X - Y
*/
public struct Position
{
    public int x;
    public int y;

    public int z
    {
        get => -1 * (this.x + this.y);
    }

    public int row
    {
        get => x;
    }

    public int col
    {
        get => y;
    }

    public Position(int x, int y)
    {
        this.x = x;
        this.y = y;
    }

    public Position(Vector3Int gridPos)
    {
        this.x = gridPos.y;
        this.y = gridPos.x;
    }

    public Vector3Int cellPosition
    {
        get => new Vector3Int(this.y, this.x, 0);
    }

    public List<Position> neighbors
    {
        get => new List<Position> {
            new Position(this.x, this.y - 1),
            new Position(this.x+1, this.y - 1),
            new Position(this.x+1, this.y),
            new Position(this.x, this.y + 1),
            new Position(this.x-1, this.y + 1),
            new Position(this.x-1, this.y),
        };
    }

    public override string ToString()
    {
        return $"({this.x}, {this.y})";
    }
}

/*
    Tiles consist of a position in the grid and their terrain type
*/
public class GameTile : IComparable
{
    public Position position;

    public int clickedCount;

    public HexGrid map;

    public GameTile(Position position, HexGrid parent)
    {
        this.position = position;
        this.clickedCount = 0;

        this.map = parent;
    }
    public TerrainType terrainType
    {
        get => this.map.terrainType(this);
    }

    public int movementCost
    {
        get => this.terrainType.movementCost();
    }

    public Vector3Int cellPosition
    {
        get => this.position.cellPosition;
    }

    public int CompareTo(object obj)
    {
        if (obj == null)
        {
            throw new ArgumentException("Cannot compare GameTile to null");
        }

        GameTile other = obj as GameTile;
        if (other == null)
        {
            throw new ArgumentException($"{obj} is not a GameTile");
        }


        return this.movementCost.CompareTo(other.movementCost);
    }

    override public string ToString()
    {
        return $"{this.terrainType.name()} {this.position}: {this.clickedCount}";
    }
}
