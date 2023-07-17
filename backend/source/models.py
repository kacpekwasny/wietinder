from flask_login import UserMixin

from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    bio = db.Column(db.String(150), default='')
    sex = db.Column(db.String(150), default='')
    activity = db.Column(db.String(150), default='')
    college_major = db.Column(db.String(150), default='')
    images = db.relationship('Image', back_populates='user') 

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='images')
    