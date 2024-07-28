from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Habits(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    desc = db.Column(db.String())
    date_added = db.Column(db.DateTime(),default=datetime.now)
    completed = db.Column(db.String(), default='[]')
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))