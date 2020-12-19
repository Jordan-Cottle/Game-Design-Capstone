using System.Collections;
using System.Collections.Generic;
using UnityEngine;

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
}
