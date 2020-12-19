
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

        var bonusLabel = attributeLabel.transform.Find("UpgradeBoost").gameObject.GetComponent<Text>();

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

    void Initialize(JObject data)
    {
        int i = 0;
        foreach (JObject attribute in data["attributes"])
        {
            var label = transform.Find($"NumericLabel {i++}").GetComponent<NumericLabel>();
            string name = (string)attribute["name"];
            _attributeLabels[name] = label;
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
            SetAttributeValue(name, (int)attribute["value"]);
            SetUpgradeBonus(name, (int)attribute["upgrade_bonus"]);
        }
    }
}
