using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Heap<T> where T : IComparable
{
    List<T> items;
    private Dictionary<T, int> locations;

    private int left_child(int parent)
    {
        return (parent * 2) + 1;
    }

    private int right_child(int parent)
    {
        return this.left_child(parent) + 1;
    }

    private int parent(int index)
    {
        return (index - 1) / 2;
    }

    private bool has_left_child(int parent)
    {
        return this.left_child(parent) < this.items.Count;
    }

    private bool has_right_child(int parent)
    {
        return this.right_child(parent) < this.items.Count;
    }

    private void swap(int a, int b)
    {
        T itemA = this.items[a];
        T itemB = this.items[b];

        this.locations[itemA] = b;
        this.locations[itemB] = a;

        this.items[a] = itemB;
        this.items[b] = itemA;
    }

    private void update(int index)
    {
        this.updateDown(index);
        this.updateUp(index);
    }

    private void updateUp(int index)
    {
        T current;
        T parent;
        int current_index = index;
        int parent_index;
        bool swapping = true;
        while (current_index > 0 && swapping)
        {
            swapping = false;
            parent_index = this.parent(current_index);
            current = this.items[current_index];
            parent = this.items[parent_index];

            if (current.CompareTo(parent) < 0)
            {
                swapping = true;
                this.swap(current_index, parent_index);
                current_index = parent_index;
            }
        }
    }

    private void updateDown(int index)
    {
        T current;
        T left_child;
        T right_child;
        T lesser_child;

        int current_index = index;
        int child_index;
        bool swapping = true;
        while (this.has_left_child(current_index) && swapping)
        {
            swapping = false;
            current = this.items[current_index];
            child_index = this.left_child(current_index);
            left_child = this.items[child_index];

            if (!this.has_right_child(current_index))
            {
                lesser_child = left_child;
                child_index = this.left_child(current_index);
            }
            else
            {
                child_index = this.right_child(current_index);
                right_child = this.items[child_index];

                if (left_child.CompareTo(right_child) < 0)
                {
                    lesser_child = left_child;
                    child_index = this.left_child(current_index);
                }
                else
                {
                    lesser_child = right_child;
                    child_index = this.right_child(current_index);
                }
            }

            if (lesser_child.CompareTo(current) < 0)
            {
                swapping = true;
                this.swap(current_index, child_index);
                current_index = child_index;
            }
        }
    }

    public Heap()
    {
        this.items = new List<T>();
        this.locations = new Dictionary<T, int>();
    }

    public int Count
    {
        get => this.items.Count;
    }

    public bool contains(T item)
    {
        return this.locations.ContainsKey(item);
    }

    public T get(T item)
    {
        return this.items[this.locations[item]];
    }

    public void push(T item)
    {
        this.locations[item] = this.Count;
        this.items.Add(item);

        this.updateUp(this.items.Count - 1);
    }

    public T pop()
    {
        T top = this.top();

        this.swap(0, this.items.Count - 1);
        this.items.RemoveAt(this.items.Count - 1);
        this.locations.Remove(top);

        this.updateDown(0);

        return top;
    }

    public void update(T item)
    {
        this.update(this.locations[item]);
    }

    public T top()
    {
        return this.items[0];
    }

    public override string ToString()
    {
        string s = "{";
        for (int i = 0; i < this.items.Count; i++)
        {
            s += $"{this.items[i]}, ";
        }
        s += "}\n";

        return s;
    }

    public bool empty
    {
        get => this.items.Count == 0;
    }
}
