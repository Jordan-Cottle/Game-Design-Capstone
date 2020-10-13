from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import json
from uuid import uuid4

app = Flask(__name__)
socketio = SocketIO(app)

class Player:
    count = 0

    def __init__(self, name):
        Player.count += 1

        self.name = name
        self.id = uuid4()

    @property
    def data(self):

        return {key: str(value) for key, value in self.__dict__.items()}

    @property
    def json(self):
        return json.dumps(self.data)

    def __str__(self):
        return f"{self.name} {self.id}"

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('loginRequest')
def processLogin(message):
    print(f"Login requested: {message}")
    emit("login", Player(message['data']).data)

@socketio.on("connect")
def test_connect():
    print("Client connecting!")


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    print("Starting server!")
    socketio.run(app, host="192.168.1.16", port="1234")