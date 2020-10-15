using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

class Node : IComparable
{
    public GameTile tile;
    public Node parent;
    public int costFromStart;
    private int estimate;
    public Node(GameTile tile, int costFromStart, GameTile goal)
    {
        this.tile = tile;
        this.costFromStart = costFromStart;
        this.estimate = (int)Vector3Int.Distance(this.tile.cellPosition, goal.cellPosition) * 10;
    }

    public int estimateToGoal
    {
        get => this.costFromStart + this.estimate;
    }

    public override bool Equals(object obj)
    {
        // If the passed object is null
        Node other = obj as Node;

        if (other is null)
        {
            return false;
        }

        return this.tile == other.tile;
    }

    public override int GetHashCode()
    {
        return this.tile.GetHashCode();
    }

    public static bool operator ==(Node a, Node b)
    {
        return a.tile == b.tile;
    }

    public static bool operator !=(Node a, Node b)
    {
        return a.tile != b.tile;
    }

    public static bool operator <(Node a, Node b)
    {
        return a.estimateToGoal < b.estimateToGoal;
    }
    public static bool operator >(Node a, Node b)
    {
        return a.estimateToGoal > b.estimateToGoal;
    }

    public int CompareTo(object o)
    {
        Node other = o as Node;

        if (other is null)
        {
            throw new ArgumentException("Cannot compare GameTile to null");
        }

        if (this < other)
        {
            return -1;
        }
        else if (this > other)
        {
            return 1;
        }

        return 0;
    }

    override public string ToString()
    {
        return $"{this.tile}: {this.costFromStart}";
    }
}
public class AStar
{
    private GameTile destination;
    private HexGrid world;


    public AStar(HexGrid world, GameTile destination)
    {
        this.world = world;
        this.destination = destination;
    }
    public List<GameTile> search(GameTile start)
    {

        List<GameTile> path = new List<GameTile>();
        Heap<Node> openList = new Heap<Node>();
        HashSet<GameTile> closed = new HashSet<GameTile>();

        // Push start onto heap for first iteration of while loop below

        Node currentNode = new Node(start, 0, this.destination);
        openList.push(currentNode);

        while (currentNode.tile != this.destination)
        {
            if (!openList.empty)
            {
                currentNode = openList.pop();
                closed.Add(currentNode.tile);
            }
            else
            {
                return path;  // No path can be created
            }

            if (currentNode.tile == this.destination)
            {
                break;
            }

            // while currentNode.contents != self.goal:
            List<GameTile> neighbors = this.world.neighbors(currentNode.tile);

            foreach (GameTile neighbor in neighbors)
            {
                // Debug.Log($"AStar looking at {neighbor}");
                if (closed.Contains(neighbor))
                {
                    continue;
                }

                int costFromStart = currentNode.costFromStart + neighbor.movementCost;
                Node n = new Node(neighbor, costFromStart, destination);

                if (openList.contains(n))
                {
                    n = openList.get(n); // Get reference to object in heap
                    if (costFromStart < n.costFromStart)
                    {
                        // Debug.Log($"Updating {n} in {openList}");
                        n.costFromStart = costFromStart;
                        n.parent = currentNode;

                        // Refresh openList to handle potentially reordered neighbor
                        openList.update(n);
                    }
                }
                else
                {
                    // Debug.Log($"Adding {n} to {openList}");
                    n.parent = currentNode;

                    openList.push(n);
                }
            }

        }

        // Generate path
        while (currentNode.tile != start)
        {
            path.Add(currentNode.tile);
            currentNode = currentNode.parent;
        }

        path.Reverse();
        return path;
    }
}
