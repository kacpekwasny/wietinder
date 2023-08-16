from enum import Enum
import uuid

from flask_login import UserMixin

from . import db

class Sex(Enum):
    male = 'male'
    female = 'female'



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(30))
    bio = db.Column(db.String(300), default='')
    
    sex = db.Column(db.Enum(Sex), default=Sex.male.value)
    """The sex of user. Enum 'Female'/'Male' """

    target_sex = db.Column(db.String(30), default='')
    """
    List of the target sex of interest for the user as a string.
    Ex.: 'female;male'
    """
    target_activity = db.Column(db.String(150), default='')
    """
    The desired activity for the match.
    """

    college_major = db.Column(db.String(150), default='student debil')


    images = db.relationship('Image', back_populates='user')

    def possible_matches_all(self):
        return PossibleMatch.query.filter(
            (PossibleMatch.user1_id == self.id) | (PossibleMatch.user2_id == self.id)
        )
    
    def possible_matches_undecided(self):
        return PossibleMatch.query.filter(
            (PossibleMatch.user1_id == self.id & PossibleMatch.user1_choice == MatchChoice.none) \
          | (PossibleMatch.user2_id == self.id & PossibleMatch.user2_choice == MatchChoice.none) \
        )


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='images')


class MatchChoice(Enum):
    like = 'like'
    dislike = 'dislike'
    block = 'block'
    none = 'none'

class PossibleMatch(db.Model):
    __tablename__ = 'possible_matches'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()))
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user1_choice = db.Column(db.Enum(MatchChoice), default=MatchChoice.none.value)
    user2_choice = db.Column(db.Enum(MatchChoice), default=MatchChoice.none.value)




    