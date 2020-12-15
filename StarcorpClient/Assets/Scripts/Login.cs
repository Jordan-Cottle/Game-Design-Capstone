using UnityEngine;
using UnityEngine.UI;

using System.Text.RegularExpressions;

using Newtonsoft.Json.Linq;

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

    [SerializeField]
    private Text statusLabel;

    private Regex emailPattern = new Regex(@"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$");
    private bool checkEmailReminder = false;
    private string emailChecked = "";

    private bool registrationShown;
    // Start is called before the first frame update
    private Socket socket;

    void Start()
    {
        this.socket = FindObjectOfType<Socket>();
    }
    public void LoginUser()
    {
        string email = this.emailInput.text;
        string password = this.passwordInput.text;

        Debug.Log($"Logging in with: {email}, {password}");

        this.statusLabel.text = "Logging in...";
        this.statusLabel.color = Color.green;
        this.socket.Login(email, password);
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
            this.SubmitRegistration();
        }
    }

    private void SubmitRegistration()
    {
        string username = this.usernameInput.text;
        string email = this.emailInput.text;
        string password = this.passwordInput.text;
        string rePassword = this.rePasswordInput.text;

        if (password != rePassword)
        {
            this.statusLabel.gameObject.SetActive(true);
            this.statusLabel.text = "Both password fields must match!";
            return;
        }

        if (username.Length < 3)
        {
            this.statusLabel.gameObject.SetActive(true);
            this.statusLabel.text = "Username must be at least 4 characters long!";
            return;
        }

        if (password.Length < 5)
        {
            this.statusLabel.gameObject.SetActive(true);
            this.statusLabel.text = "Password must be at least 6 characters long!";
            return;
        }

        if (!this.ValidEmail(email))
        {
            this.statusLabel.gameObject.SetActive(true);
            if (!this.checkEmailReminder)
            {
                this.statusLabel.text = "Please double check that your email is valid!";
                this.checkEmailReminder = true;
                this.emailChecked = email;
                return;
            }
            if (this.emailChecked != email)
            {
                this.statusLabel.text = "Please double check that your email is valid!";
                this.emailChecked = email;
                return;
            }
        }

        Debug.Log("Submitting registration");
        this.socket.Register("registration_success", (ev) =>
        {
            var data = ev.Data[0];

            Debug.Log($"Registration successful: {data}");

            this.socket.UnRegister("registration_success");
            this.usernameInput.gameObject.SetActive(false);
            this.rePasswordInput.gameObject.SetActive(false);
            this.passwordInput.text = "";
            this.statusLabel.text = "Registration successful, please log in now";
            this.statusLabel.color = Color.green;

        });


        this.socket.Emit("register", JObject.Parse($"{{'user_name': '{username}', 'email': '{email}', 'password': '{password}'}}"));
    }


    private bool ValidEmail(string email)
    {
        return this.emailPattern.IsMatch(email);
    }
}
