﻿using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

/*
    Represent the hexagonal grid as cube coordinates
*/
public struct Position
{
    public Vector3Int cellPosition;

    public int x;
    public int y;
    public int z;

    public Position(Vector3Int gridPos)
    {
        this.x = gridPos.x - (gridPos.y - (gridPos.y & 1)) / 2;
        this.z = gridPos.y;
        this.y = -x - z;

        this.cellPosition = gridPos;
    }

    public Position cubeOffset(int x, int y, int z)
    {
        Position pos = new Position(this.cellPosition);

        pos.x += x;
        pos.y += y;
        pos.z += z;

        return pos;
    }
    public List<Position> neighbors
    {
        get => new List<Position> {
            this.cubeOffset(1, -1, 0),
            this.cubeOffset(1, 0, -1),
            this.cubeOffset(0, 1, -1),
            this.cubeOffset(-1, 1, 0),
            this.cubeOffset(-1, 0, 1),
            this.cubeOffset(0, -1, 1),
        };
    }

    public static bool operator ==(Position a, Position b)
    {
        return a.x == b.x && a.y == b.y && a.z == b.z;
    }

    public static bool operator !=(Position a, Position b)
    {
        return !(a == b);
    }

    public override string ToString()
    {
        return $"({this.x}, {this.y}, {this.z})";
    }

    public override bool Equals(object obj)
    {
        if (obj == null)
        {
            return false;
        }

        Position other = (Position)obj;

        return this == other;
    }

    public override int GetHashCode()
    {
        return this.x << 16 | this.y;
    }

}

/*
    Tiles consist of a position in the grid and their terrain type
*/
public class GameTile
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

    public static bool operator ==(GameTile a, GameTile b)
    {
        return a.position == b.position;
    }

    public static bool operator !=(GameTile a, GameTile b)
    {
        return a.position != b.position;
    }

    public override bool Equals(object obj)
    {
        GameTile other = obj as GameTile;
        if (other == null)
            return false;

        return this.position == other.position;
    }

    public override int GetHashCode()
    {
        return this.position.GetHashCode();
    }

    public int CompareTo(object obj)
    {
        GameTile other = obj as GameTile;
        if (other == null)
            throw new ArgumentException("Cannot compare GameTile to null");

        return this.movementCost.CompareTo(other.movementCost);

    }

    public static bool operator <(GameTile a, GameTile b)
    {
        return a.terrainType.movementCost() < b.terrainType.movementCost();
    }

    public static bool operator >(GameTile a, GameTile b)
    {
        return a.terrainType.movementCost() > b.terrainType.movementCost();
    }

    override public string ToString()
    {
        return $"{this.terrainType.name()} {this.position}: {this.clickedCount}";
    }
}
