from flask import Flask, request, render_template, redirect, session

import db

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    button = request.form['button']
    username = request.form['username']
    password = request.form['password']
    valid_user = valid(username, password)
    if button == 'cancel' or not(valid_user):
        return render_template('login.html')
    else:
        criteria = {'username': username, 'password': password}
        user = db.find_user(criteria)
        if user:
            session['username'] = username
            return redirect('/')
        else:
            return 'Invalid username and password combination'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    button = request.form['button']
    username = request.form['username']
    password = request.form['password']
    if button == 'cancel':
        return redirect('/')
    else:
        criteria = {'username': username}
        if db.find_user(criteria):
            return render_template('register.html')
        else:
            user_params = {'username': username, 'password': password}
            db.new_user(user_params)
            session['username'] = username
            return redirect('/')


@app.route('/display')
def display():
    if 'username' in session:
        username = session['username']
        password = db.find_user({'username': username})['password']
        return render_template('display.html', username=username, password=password)
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/account/change', methods=['GET', 'POST'])
def change_account():
    if not session['username']:
        redirect('/')

    if request.method == 'GET':
        return render_template('change_account.html')

    if request.form['button'] == 'cancel':
        return redirect('/')

    criteria = {'username': session['username']}

    username = request.form['username']
    password = request.form['password']
    changeset = {}
    if username:
        changeset['username'] = username
    if password:
        changeset['password'] = password

    if valid_change(changeset):
        db.update_user(criteria, changeset)
        if username:
            session['username'] = username
        return redirect('/')
    else:
        return render_template('change_account.html')


def valid_change(changeset):
    if changeset['username'] == session['username']:
        return False
    if db.find_user(changeset['username']):
        return False
    return True


def check_logged_in():
    if 'username' in session:
        return '<a href="/display">Logged in as ' + session['username']
    else:
        return '<a href="/login">Log In'


def valid(username, password):
    return True


if __name__ == '__main__':
    app.secret_key = 'Happy Halloween'
    app.debug = True
    app.run()
