import uuid

from enum import Enum
from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy.schema import DDL

from . import db

class Sex(Enum):
    male = 'male'
    female = 'female'



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True)
    public_id   = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    email       = db.Column(db.String(150), unique=True)
    password    = db.Column(db.String(150))
    first_name  = db.Column(db.String(30))
    bio         = db.Column(db.String(300), default='')
    sex         = db.Column(db.Enum(Sex), default=Sex.male.value)
    """The sex of user. Enum 'Female'/'Male' """

    target_sex  = db.Column(db.String(30), default='')
    """
    List of the target sex of interest for the user as a string.
    Ex.: 'female;male'
    """

    target_activity = db.Column(db.String(150), default='')
    """
    The desired activity for the match.
    """

    college_major   = db.Column(db.String(150), default='student debil')

    images = db.Column(db.Text(), default="")
    """List of filenames in JSON format."""

    def possible_matches_all(self):
        return PossibleMatch.query.filter(
            (PossibleMatch.user1_public_id == self.public_id) | (PossibleMatch.user2_public_id == self.public_id)
        )
    
    def possible_matches_undecided(self):
        return PossibleMatch.query.filter(
            ((PossibleMatch.user1_public_id == self.public_id) & (PossibleMatch.user1_choice == MatchChoice.none)) \
          | ((PossibleMatch.user2_public_id == self.public_id) & (PossibleMatch.user2_choice == MatchChoice.none)) \
        )


class MatchChoice(Enum):
    like    = 'like'
    dislike = 'dislike'
    block   = 'block'
    none    = 'none'

class PossibleMatch(db.Model):
    __tablename__ = 'possible_matches'
    id              = db.Column(db.Integer, primary_key=True)
    user1_public_id = db.Column(db.String(36), db.ForeignKey('users.public_id'))
    user2_public_id = db.Column(db.String(36), db.ForeignKey('users.public_id'))
    user1_choice    = db.Column(db.Enum(MatchChoice), default=MatchChoice.none.value)
    user2_choice    = db.Column(db.Enum(MatchChoice), default=MatchChoice.none.value)


event.listen(
    User.__table__,
    "after_create",
    DDL(f"""
CREATE TRIGGER make_pairs
AFTER INSERT ON {User.__tablename__}
FOR EACH ROW
BEGIN
INSERT INTO {PossibleMatch.__tablename__}
    (user1_public_id, user2_public_id, user1_choice, user2_choice)
SELECT
    NEW.public_id, users.public_id, "none", "none"
FROM users WHERE id!=NEW.id;
END
""")
)
    