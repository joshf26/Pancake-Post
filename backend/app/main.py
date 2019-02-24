from flask import Flask, escape, session, request, render_template, redirect, url_for, flash
from flask_socketio import SocketIO, join_room

from conf import *
from database import Database, Orders

app = Flask(__name__)
app.secret_key = 'dev2'
socket = SocketIO(app)
socket.init_app(app)

database = Database()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and request.form['username'] and \
                'password' in request.form and request.form['password']:
            if request.form.get('action', None) == 'Create Account':
                if database.create_user(request.form['username'], request.form['password']):
                    flash('Account Created')
                else:
                    flash('Username Already Exists')

            elif database.check_user(request.form['username'], request.form['password']):
                session['username'] = request.form['username']
            else:
                flash('Invalid login credentials.')

        return redirect(url_for('index'))

    session['domain'] = request.args.get('domain', DEFAULT_DOMAIN)

    if 'username' in session:
        posts = database.get_posts(session.get('domain', DEFAULT_DOMAIN), 10, Orders.VOTES)
        return render_template('index.html', username=session['username'],
                               posts=posts, domain=session.get('domain', DEFAULT_DOMAIN))

    return render_template('landing.html')


@app.route('/change')
def change():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/post', methods=['POST'])
def post():
    if 'title' in request.form and request.form['title'] and 'body' in request.form:
        database.add_post(session['username'], request.form['title'], request.form['body'],
                          None, session.get('domain', DEFAULT_DOMAIN))
    else:
        flash('Error Posting')

    return redirect(url_for('index'))


@socket.on('connect')
def connect():
    join_room(session['domain'])


@socket.on('chat')
def text(chat):
    if 'msg' in chat and chat['msg']:
        socket.emit('chat', {
            'msg': escape(chat['msg'])[:120],
            'from': escape(session['username'])
        }, room=session.get('domain', DEFAULT_DOMAIN))


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=80, debug=True)
