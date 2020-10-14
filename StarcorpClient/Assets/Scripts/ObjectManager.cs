using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Newtonsoft.Json.Linq;

public class ObjectManager
{
    private Dictionary<string, GameObject> objects;

    public ObjectManager()
    {
        this.objects = new Dictionary<string, GameObject>();
    }

    void Load(JObject data)
    {
        Debug.Log(data);
    }
}
