using UnityEngine;
using Newtonsoft.Json.Linq;

public class UpgradePanelManager : MonoBehaviour
{

    public NumericLabel GatherPowerLabel;
    public NumericLabel CarryCapacityLabel;
    public UpgradeOption WeaponUpgrade;
    public UpgradeOption StorageUpgrade;
    // Start is called before the first frame update

    private Vector3 _position;
    void Start()
    {
        _position = transform.position;
        Hide();
    }

    public void Hide()
    {
        transform.position = new Vector3(10000, 10000, 10000);
    }

    public void Show()
    {
        transform.position = _position;
    }

    public void Initialize(JArray data)
    {
        foreach (JObject system in data)
        {
            Debug.Log($"Initializing UpgradePanel with {system}");

            string name = (string)system["name"];
            if (name.Contains("Laser"))
            {
                WeaponUpgrade.Initialize(system);
            }
            else if (name.Contains("Cargo Bay"))
            {
                StorageUpgrade.Initialize(system);
            }
            else
            {
                Debug.Log($"WARNING unrecognized ship system {name}");
            }
        }

        UpdatePanels(data);
    }

    public void UpdatePanels(JArray data)
    {
        Debug.Log($"Updating UpgradePanel with {data}");

        int totalGatherPower = 0;
        int totalCarryCapacity = 0;

        foreach (JObject system in data)
        {
            Debug.Log($"Updating {system}");

            string name = (string)system["name"];
            if (name.Contains("Laser"))
            {
                totalGatherPower += (int)system["gather_power"];
                WeaponUpgrade.UpdateLabels(system);
            }
            else if (name.Contains("Cargo Bay"))
            {
                totalCarryCapacity += (int)system["carry_capacity"];
                StorageUpgrade.UpdateLabels(system);
            }
            else
            {
                Debug.Log($"WARNING unrecognized ship system {name}");
            }
        }

        GatherPowerLabel.Value = totalGatherPower;
        CarryCapacityLabel.Value = totalCarryCapacity;
    }
}
