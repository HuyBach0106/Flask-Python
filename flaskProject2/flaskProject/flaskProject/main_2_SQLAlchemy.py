import os
from flask import Flask, render_template
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/website.db')
db = SQLAlchemy(app)

class user(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

@app.route('/')
def introduction():
    return ('Successfully setting up and configuring the Database!'
            '<br></br><a href="/Users">Users</a>')
@app.route('/Users')
def index():
    records = user.query.all()
    for record in records:
        print(f"ID: {record.id}, "
              f"Name: {record.name}, "
              f"Email: {record.email}, "
              f"Password: {record.password}, ")
        return render_template('UserData.html', data=records)
if __name__ == '__main__':
    app.run(debug=True)
