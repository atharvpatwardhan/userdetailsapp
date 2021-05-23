from flask import Flask,render_template,redirect,url_for,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "12345"
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=1)
#app.run(host="0.0.0.0")
#app.run('flask run -h localhost -p 3000')


db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self,name,email):
        self.name = name
        self.email = email


@app.route("/")

def home():
    return render_template("index3.html")

@app.route("/view")
def view():
    return render_template("view.html",values=users.query.all())

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method =="POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email

        else:    
            usr = users(user,"")
            db.session.add(usr)
            db.session.commit()
        flash("Logged In Successfully!","info")
        return redirect(url_for("user"))
    
    else: 
        if "user" in session:
            flash("Already Logged In")
            return redirect(url_for("user"))
        return render_template("login1.html")

@app.route("/user",methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST" :
            email = request.form["email"]
            session["email"] = email
            flash("Email saved successfully!")
        else:
            if "email" in session :
                email = session["email"]
                found_user = users.query.filter_by(name=user).first()
                found_user.email = email
                db.session.commit()
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))
    return render_template("user.html",email = email)

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out,{user}","info")
    session.pop("user", None)
    session.pop("email", None)
    flash("Logout Successful!","info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(threaded=True, port=5000)

