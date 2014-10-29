from flask import Flask,request,render_template,redirect,session
from pymongo import Connection

app=Flask(__name__)

@app.route("/")
def home():
    if "username" in session:
        return "Logged in as %s" % (session["username"])
    return "You are not logged in"

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
            conn = Connection()
            db = conn["hi"] 
            if db.users.find({username:username,password:password})==None:
                return "Invalid username and password combination"
            else:
                session["username"] = username
                return redirect("/")
            

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        button = request.form["button"]
        username = request.form["username"]
        password = request.form["password"]
        valid_user = valid(username,password)
        if button=="cancel":
            return redirect("/")
        else:
            conn = Connection()
            db = conn["hi"]
            if db.users.find({username:username})==None:
                entry = {"username":username,"password":password}
                db.users.insert(entry)
                print entry
                session["username"] = username
                return redirect("/")
            else:
                return render_template("register.html")

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
