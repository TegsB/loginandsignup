

from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import random 

app = Flask(__name__)
app.secret_key = "dungeonsanddragons"


#configure SQL alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#database model
class User(db.Model):
    #class variables
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



#routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")


#Login route
@app.route("/Login", methods=["POST"])
def login():
    username = request.form["Username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template("index.html")
    


#Sign up 
@app.route("/register", methods=['POST'])
def register():
    username = request.form["Username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("signedup.html")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard'))

@app.route("/signedup")
def signedup():
    return render_template("index.html")


#Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session['username'])
    return redirect(url_for('home'))


#Logout
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))

#new game
@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/continue")
def continue_game():
    return render_template("continue.html")

@app.route("/save")
def save():
    return render_template('save.html')

#the main game

@app.route("/start")
def start():
    return render_template("start.html")

@app.route("/river")
def river():
    return render_template("river.html")

@app.route("/clearing")
def clearing():
    return render_template("clearing.html")

@app.route("/man")
def man():
    return render_template("man.html")

@app.route("/east")
def east():
    return render_template("east.html")

@app.route("/westNight")
def westNight():
    return render_template("west-night.html")

@app.route("/doorway")
def doorway():
    return render_template("doorway.html")

@app.route("/shop")
def shop():
    return render_template("shopclosed.html")

@app.route("/inn")
def inn():
    return render_template("inn.html")

@app.route("/west")
def west():
    return render_template("west.html")

@app.route("/seduce")
def seduce():
    chance = random.randint(1,5)
    if chance <3:
        return render_template('west-night.html')
    else:
        return render_template("room.html")

@app.route("/room")
def room():
    return render_template("room.html")




if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)