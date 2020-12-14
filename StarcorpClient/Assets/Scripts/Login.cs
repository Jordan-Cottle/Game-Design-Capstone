using UnityEngine;
using UnityEngine.UI;

public class Login : MonoBehaviour
{
    [SerializeField]
    private InputField usernameInput;
    [SerializeField]
    private InputField emailInput;

    [SerializeField]
    private InputField passwordInput;
    [SerializeField]
    private InputField rePasswordInput;

    private bool registrationShown;
    // Start is called before the first frame update
    public Socket session;
    public void LoginUser()
    {
        string email = emailInput.text;
        string password = passwordInput.text;

        Debug.Log($"Logging in with: {email}, {password}");

        session.Login(email, password);
    }

    public void Registration()
    {
        if (!this.registrationShown)
        {
            this.usernameInput.gameObject.SetActive(true);
            this.rePasswordInput.gameObject.SetActive(true);
            this.registrationShown = true;
        }
        else
        {
            Debug.Log("Submit registration");
        }
    }
}
