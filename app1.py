from flask import Flask, request, render_template, redirect, session

import db

app = Flask(__name__)


@app.route("/")
def home():
    if "username" in session:
        return "Logged in as %s" % (session["username"])
    return render_template('home.html')


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        button = request.form["button"]
        username = request.form["username"]
        password = request.form["password"]
        valid_user = valid(username,password)
        if button=="cancel" or not(valid_user):
            return render_template("login.html")
        else:
            user_params = {'username': username, 'password': password}
            user = db.new_user(user_params)
            print user
            session['username'] = username
            return redirect("/")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


def valid(username, password):
    return True


if __name__=="__main__":
    app.secret_key="Happy Halloween"
    app.debug=True
    app.run();
