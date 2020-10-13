using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

class Node
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
                return new List<GameTile>();  // No path can be created
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
        List<GameTile> path = new List<GameTile>();
        while (currentNode.tile != start)
        {
            path.Add(currentNode.tile);
            currentNode = currentNode.parent;
        }

        path.Reverse();

        // Debug.Log($"Path generated: {path}");
        return path;
    }
    public IEnumerator drawSearch(GameTile start, List<GameTile> path)
    {

        Heap<Node> openList = new Heap<Node>();
        HashSet<GameTile> closed = new HashSet<GameTile>();

        Canvas canvas = this.world.canvas;
        Text label = this.world.textPrefab;

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
                yield break;  // No path can be created
            }

            // label = this.world.getLabel(currentNode.tile);
            // string previous = label.text;
            // label.text = "Current Node";
            // yield return new WaitForSeconds(0.1f);
            // label.text = previous;


            if (currentNode.tile == this.destination)
            {
                break;
            }

            // while currentNode.contents != self.goal:
            List<GameTile> neighbors = this.world.neighbors(currentNode.tile);

            foreach (GameTile neighbor in neighbors)
            {
                // label = this.world.getLabel(neighbor);
                // previous = label.text;
                // label.text = "Neighbor found";
                // yield return new WaitForSeconds(0.1f);
                // label.text = previous;

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
    }
}
