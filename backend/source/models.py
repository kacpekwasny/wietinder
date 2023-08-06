from enum import Enum
import uuid

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

    def possible_pairs_all(self):
        return PossiblePair.query.filter(
            (PossiblePair.user1_id == self.id) | (PossiblePair.user2_id == self.id)
        )
    
    def possible_pairs_undecided(self):
        return PossiblePair.query.filter(
            (PossiblePair.user1_id == self.id & PossiblePair.user1_choice == PairChoice.NONE) \
          | (PossiblePair.user2_id == self.id & PossiblePair.user2_choice == PairChoice.NONE) \
        )


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='images')


class PairChoice(Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'
    BLOCK = 'block'
    NONE = 'none'

class PossiblePair(db.Model):
    __tablename__ = 'possible_pairs'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()))
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user1_choice = db.Column(db.Enum(PairChoice))
    user2_choice = db.Column(db.Enum(PairChoice))




    