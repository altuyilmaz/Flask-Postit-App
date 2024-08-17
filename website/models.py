from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    notes = db.relationship("Note", backref="author", lazy=True)
    likes = db.relationship("Like", backref="user", lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    likes = db.relationship("Like", backref="note", lazy=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"),nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Ban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    banned_user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    banning_user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    date = db.Column(db.DateTime(timezone=True),default=func.now())