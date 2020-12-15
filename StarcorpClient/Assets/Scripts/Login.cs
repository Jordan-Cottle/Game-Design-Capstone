using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

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

        this.SetMessage("Logging in...", Color.green);
        this.login(email, password);
    }

    private void login(string email, string password)
    {
        Debug.Log("Logging in");

        this.socket.Register("login_accepted", (ev) =>
        {
            var data = ev.Data[0];

            this.socket.userID = (string)data["id"];

            Debug.Log($"Logged in successfully with ID: {this.socket.userID}");

            this.socket.ready = true;
            this.socket.UnRegister("login_accepted");
            this.socket.UnRegister("login_failed");

            this.socket.Register("player_logout", (eve) =>
            {
                Debug.Log("Checking for client being logged out due to inactivity");
                string userID = (string)eve.Data[0]
            ["user_id"];

                Debug.Log($"This: {this.socket.userID}, Other: {userID}");
                if (userID == this.socket.userID)
                {
                    Debug.Log("Client inactive, shutting down socket.");
                    this.socket.Close();

                    SceneManager.LoadScene("MainMenu");
                }
            });

            SceneManager.LoadScene("MainScene");
        });

        this.socket.Register("login_failed", (ev) =>
        {
            var data = ev.Data[0];

            string reason = (string)data["reason"];
            string error_id = (string)data["id"];

            Debug.Log($"Problem encountered with logging in: {reason}, {error_id}");

            this.SetMessage(reason, Color.red);

            this.socket.UnRegister("login_accepted");
            this.socket.UnRegister("login_failed");
        });

        this.socket.Emit("login", JObject.Parse($"{{'email': '{email}', 'password': '{password}'}}"));
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
            this.SetMessage("Both password fields must match!", Color.red);
            return;
        }

        if (username.Length < 3)
        {
            this.SetMessage("Username must be at least 4 characters long!", Color.red);
            return;
        }

        if (password.Length < 5)
        {
            this.SetMessage("Password must be at least 6 characters long!", Color.red);
            return;
        }

        if (!this.ValidEmail(email))
        {
            this.statusLabel.gameObject.SetActive(true);
            if (!this.checkEmailReminder)
            {
                this.SetMessage("Please double check that your email is valid!", Color.red);
                this.checkEmailReminder = true;
                this.emailChecked = email;
                return;
            }
            if (this.emailChecked != email)
            {
                this.SetMessage("Please double check that your email is valid!", Color.red);
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
            this.SetMessage("Registration successful, please log in now", Color.green);
        });

        this.socket.Register("registration_failed", (ev) =>
        {
            var data = ev.Data[0];

            string reason = (string)data["reason"];
            string error_id = (string)data["id"];

            Debug.Log($"Registration unsuccessful: {reason}, {error_id}");

            this.socket.UnRegister("registration_failed");

            this.SetMessage(reason, Color.red);
        });


        this.socket.Emit("register", JObject.Parse($"{{'user_name': '{username}', 'email': '{email}', 'password': '{password}'}}"));
    }

    private void SetMessage(string message, Color color)
    {
        this.statusLabel.gameObject.SetActive(true);
        this.statusLabel.text = message;
        this.statusLabel.color = color;
    }


    private bool ValidEmail(string email)
    {
        return this.emailPattern.IsMatch(email);
    }
}
