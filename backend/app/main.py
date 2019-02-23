from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socket = SocketIO(app)


@app.route('/')
def index_route():
    return render_template('landing.html')


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=80, debug=True)
