var connection;
var logonTimeout;

function logonCallback(res) {
    clearTimeout(logonTimeout);
    // Send Message back to Unity GameObject with name 'XXX' that has NetworkManager script attached 
    SendMessage('XXX', 'OnMatchJoined', JSON.stringify(response));
};

function Logon(str) {
    var data = JSON.parse(str);

    connection = io.connect();
    // Setup receiver client side function callback 
    connection.on('JoinMatchResult', logonCallback);
    // Attempt to contact server with user data 
    connection.emit('JoinMatchQueue', data);
    // Disconnect after 30 seconds if no response from server 
    logonTimeout = setTimeout(function () {
        connection.disconnect();
        connection = null;
        var response = { result: false };
        // Send Message back to Unity GameObject with name 'XXX' that has NetworkManager script attached 
        SendMessage('XXX', 'OnMatchJoined', JSON.stringify(response));
    }, 30000);
}

function QuitMatch() {
    if (connection) {
        connection.disconnect();
        connection = null;
    }
}