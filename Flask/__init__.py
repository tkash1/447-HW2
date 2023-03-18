from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = "users.db"

def application():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "I AM READY FOR SPRING BREAK"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String(200))
        userID = db.Column(db.Integer)
        points = db.Column(db.Integer)
    """
    # create form
    class UserForm(FlaskForm):
        name = StringField("Name", validators=[DataRequired()])
        userID = StringField("ID", validators=[DataRequired()])
        points = StringField("Name", validators=[DataRequired()])
        submit = SubmitField("Submit")
    """

    @app.route('/')
    def homepage():
        users = User.query.order_by(User.id)
        return render_template("view.html", users = users)


    @app.route("/adduser.html", methods = ["GET", "POST"])
    def addUser():
        if request.method == 'POST':
            name = request.form.get('name')
            userID = request.form.get('userID')
            points = request.form.get('points')
            new_user = User(name = name, userID = userID, points = points)
            db.session.add(new_user)
            db.session.commit()
        
        return render_template("adduser.html")

    @app.route("/search.html", methods = ["GET", "POST"])
    def searchUser():
        if request.method == 'POST':
            name = request.form.get('name')
            user = User.query.filter_by(name = name).first()
            if user:
                flash("Name: " + user.name + "  ID: " + str(user.userID) + " Points: " + str(user.points))
                return redirect(url_for('searchUser'))
            else:
                flash(name + " does not exist.")
                return redirect(url_for('searchUser'))
            
        return render_template("search.html")

    @app.route('/removeuser.html', methods=['GET', 'POST'])
    def removeUser():
        if request.method == 'POST':
            name = request.form.get('name')
            user = User.query.filter_by(name = name).first()

            try:
                db.session.delete(user)
                db.session.commit()
                flash(user.name + " deleted.")
                return redirect(url_for('removeUser'))
            except:
                flash(name + " does not exist.")
                return redirect(url_for('removeUser'))
            
        return render_template("removeuser.html")

    with app.app_context():
        db.create_all()
        
    return app

"""
import sqlite3
import random
from flask import Flask, session, render_template, request, g

app = Flask(__name__)
app.secret_key = "select_a_COMPLEX_secret_key_please"

@app.route("/")
def index():
    data = get_db()
    return render_template("index.html", all_data = data)

@app.route("/add_user", methods =["post"])
def add_user():
    return request.form["select_user"]

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('users.db')
        cursor = db.cursor()
        cursor.execute("select * from users")
        all_data = cursor.fetchall()
    return all_data

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()
"""