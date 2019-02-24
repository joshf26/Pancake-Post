from flask import Flask, escape, session, request, render_template, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room

from database import Database

app = Flask(__name__)
app.secret_key = 'dev'
socket = SocketIO(app)
socket.init_app(app)

database = Database()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and request.form['username'] and \
                'password' in request.form and request.form['password']:
            if database.check_user(request.form['username'], request.form['password']):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
        flash('Invalid login credentials.')
        return redirect(url_for('index'))

    if 'username' in session:
        return render_template('index.html', username=session['username'], domain='allforum.com')

    return render_template('landing.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        if 'username' in request.form and request.form['username'] and \
                'password' in request.form and request.form['password']:
            if database.create_user(request.form['username'], request.form['password']):
                flash('Account Created')
                return redirect(url_for('index'))
            flash('Username Already Exists')
    return render_template('create.html')


@app.route('/change')
def change():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/post', methods=['POST'])
def post():
    if 'title' in request.form and request.form['title'] and 'content' in request.form:
        pass


@socket.on('chat')
def text(chat):
    socket.emit('chat', {
                            'msg': escape(chat['msg']),
                            'from': escape(session['username'])
                        })


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=80, debug=True)
