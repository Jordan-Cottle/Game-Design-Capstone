from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

with open("html/index.html") as home_page_file:
    home_page = home_page_file.read()


@socketio.on("message")
def handle_message(message):
    print("received message: " + message)


@socketio.on("my event")
def handle_my_custom_event(json):
    print("received json: " + str(json))


@socketio.on("connect")
def test_connect():
    emit("my response", {"data": "Connected"})


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")


@app.route("/")
def home():
    return home_page


if __name__ == "__main__":
    socketio.run(app)