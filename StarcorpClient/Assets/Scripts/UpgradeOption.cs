
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using Newtonsoft.Json.Linq;

public class UpgradeOption : MonoBehaviour
{

    [SerializeField]
    private string _systemName = "NullSystem";

    private Dictionary<string, NumericLabel> _attributeLabels;
    private Dictionary<string, int> _upgradeBonuses;

    private float _upgradeCost = 0;

    public Text SystemNameLabel;
    public Text CostLabel;

    public string SystemName
    {
        get => _systemName; private set
        {
            _systemName = value;
            SystemNameLabel.text = _systemName;
        }
    }
    public float UpgradeCost
    {
        get => _upgradeCost; private set
        {
            _upgradeCost = value;
            this.CostLabel.text = $"${_upgradeCost:F2}";
        }
    }

    private void SetUpgradeBonus(string attributeName, int bonus)
    {
        this._upgradeBonuses[attributeName] = bonus;
        var attributeLabel = this._attributeLabels[attributeName];

        var bonusLabel = attributeLabel.transform.Find("CurrentValue/UpgradeBoost").gameObject.GetComponent<Text>();

        string prefix = bonus > 0 ? "+" : "-";
        bonusLabel.text = $"{prefix}{bonus}";
    }

    private void SetAttributeValue(string attributeName, int value)
    {
        var attributeLabel = this._attributeLabels[attributeName];
        attributeLabel.Value = value;
    }

    void Start()
    {
        _attributeLabels = new Dictionary<string, NumericLabel>();
        _upgradeBonuses = new Dictionary<string, int>();
    }

    public void Initialize(JObject data)
    {
        int i = 1;
        foreach (JObject attribute in data["attributes"])
        {
            string name = (string)attribute["name"];
            if (name.Contains("gather") || name.Contains("carry"))
            {
                string childName = $"NumericLabel {i++}";
                var label = transform.Find(childName).GetComponent<NumericLabel>();

                _attributeLabels[name] = label;
            }
            else
            {
                Debug.Log($"Not initializing unsupported {name} for display");
            }
        }

        UpdateLabels(data);
    }

    public void UpdateLabels(JObject data)
    {
        Debug.Log($"Updating upgrade option labels: {data}");

        SystemName = (string)data["name"];
        UpgradeCost = (float)data["upgrade_cost"];

        foreach (JObject attribute in data["attributes"])
        {
            string name = (string)attribute["name"];
            if (!_attributeLabels.ContainsKey(name))
            {
                Debug.Log($"Ignoring unsupported {name} for display");
                continue;
            }

            int currentValue = (int)attribute["value"];
            int upgradedValue = (int)attribute["upgraded_value"];
            SetAttributeValue(name, currentValue);
            SetUpgradeBonus(name, upgradedValue - currentValue);
        }
    }
}
