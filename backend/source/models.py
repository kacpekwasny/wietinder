from __future__ import annotations

import json
from typing import Any, Literal
import uuid
import time
import jwt as pyjwt

from datetime import datetime
from enum import Enum, EnumType
from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy.schema import DDL

from .agh import AGH_FIELDS_OF_STUDY
from .config import CONFIG


from . import db

EMAIL_LEN: int = 150
NAME_LEN:  int = 30
BIO_LEN:   int = 300


JWT = dict[Literal["public_id", "time"],
           str | float | list | dict]

def unix_timestamp() -> float:
    # time.time returns seconds since 1/1/1970
    # JS Date.now uses miliseconds since that date.
    return time.time() * 1000

class Sex(Enum):
    male = 'male'
    female = 'female'

class TargetActivity(Enum):
    beer = 'beer'   # Na piwo
    life = 'life'   # Na stałe
    project = 'project' # Do projektu

class MatchChoice(Enum):
    like    = 'like'
    dislike = 'dislike'
    block   = 'block'
    none    = 'none'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    ##### Private #####
    id          = db.Column(db.Integer, primary_key=True)
    public_id   = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    email       = db.Column(db.String(EMAIL_LEN), unique=True)
    password    = db.Column(db.String(250))

    ##### Public #####
    name        = db.Column(db.String(NAME_LEN))
    bio         = db.Column(db.String(BIO_LEN), default='')
    sex         = db.Column(db.Enum(Sex), default=Sex.male.value)
    """The sex of user. Enum 'Female'/'Male' """

    fields_of_study = db.Column(db.Text(), default="[]")
    """json format list from agh.FIELDS_OF_STUDY"""

    target_sex  = db.Column(db.String(30), default='[]')
    """ json Enum[female, male] """

    target_activity = db.Column(db.String(150), default=json.dumps([t.value for t in TargetActivity]))
    """ The desired activity for the match. """

    images = db.Column(db.Text(), default="[]")
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
    
    def set_name(self, name: str):
        self.name = str(name)[:NAME_LEN]

    def set_bio(self, bio: str):
        self.bio = str(bio)[:BIO_LEN]

    def set_sex(self, sex: str):
        sex = str(sex)
        if Sex(sex) in Sex:
            self.sex = sex
            return
        raise ValueError(f"{sex} not in {Sex}")

    def get_fields_of_study(self) -> list[str]:
        return json.loads(self.fields_of_study)
    def set_fields_of_study(self, fields_of_study: list[str]):
        set_enum_valid(self, AGH_FIELDS_OF_STUDY, fields_of_study, "fields_of_study")

    def get_target_activity(self) -> list[str]:
        return json.loads(self.target_activity)
    def set_target_activity(self, target_activity: list[str]):
        set_enum_valid(self, TargetActivity, target_activity, "target_activity")

    def get_target_sex(self) -> list[str]:
        return json.loads(self.target_sex)
    def set_target_set(self, target_sex: list[str]):
        set_enum_valid(self, Sex, target_sex, "target_sex")

    def get_images(self) -> list[str]:
        return json.loads(self.images)
    def set_images(self, images: list[str]) -> list[str]:
        self.images = json.dumps(images)

    def refresh_jwt(self) -> str:
        return pyjwt.encode({"public_id": self.public_id,
                             "time": unix_timestamp()},
                              CONFIG.JWT_SECRET,
                              algorithm="HS256")
    @classmethod
    def get_user_by_jwt(cls, jwt: str) -> User:
        try:
            jwt: JWT = pyjwt.decode(jwt, CONFIG.JWT_SECRET, algorithms=["HS256"])
        except pyjwt.exceptions.DecodeError:
            return None
        
        user = cls.query.filter_by(public_id=jwt["public_id"]).first()
        if user is None:
            return None
        
        if unix_timestamp() - jwt["time"] > CONFIG.JWT_TIMEOUT:
            return None
        
        return user
    
    def json(self) -> dict[str, str | list[str]]:
        return {
            "name":      self.name,
            "public_id": self.public_id,
            "bio":       self.bio,
            "sex":       self.sex.value,
            "fields_of_study": self.get_fields_of_study(),
            "target_sex":      self.get_target_sex(),
            "target_activity": self.get_target_activity(),
            "images":          self.get_images(),
        }
    
    def set_from_json(self, *,
                  bio: str=None,
                  sex: str=None,
                  images:          list[str]=None,
                  target_sex:      list[str]=None,
                  target_activity: list[str]=None,
                  fields_of_study: list[str]=None,
                  **_
                ) -> None:

        # if x is not None:
        #    self.set_x(x)
        # The above notation is identical to the below ones:
        bio             is not None and self.set_bio(bio)
        sex             is not None and self.set_sex(sex)
        fields_of_study is not None and self.set_fields_of_study(fields_of_study)
        target_sex      is not None and self.set_target_set(target_sex)
        target_activity is not None and self.set_target_activity(target_activity)
        images          is not None and self.set_images(images)

    def change_match_choice(self, my_choice: MatchChoice, other_public_id: str):
        match: PossibleMatch = PossibleMatch.query.filter(
            ((PossibleMatch.user1_public_id == self.public_id)  & (PossibleMatch.user2_public_id == other_public_id)) |
            ((PossibleMatch.user1_public_id == other_public_id) & (PossibleMatch.user2_public_id == self.public_id))
        ).first()

        was_like = False
        if match.user1_choice == MatchChoice.like and match.user2_choice == MatchChoice.like:
            was_like = True

        
        if match.user1_public_id == self.public_id:
            match.user1_choice = my_choice
        else:
            match.user2_choice = my_choice

        if my_choice == MatchChoice.like and not was_like:
            match.matched_timestamp = unix_timestamp()

        db.session.commit()

    def likes_me(self) -> list[PossibleMatch]:
        return PossibleMatch.query.filter(
            ((PossibleMatch.user1_public_id == self.public_id) & (PossibleMatch.user2_choice == MatchChoice.like)) 
            | ((PossibleMatch.user2_public_id == self.public_id) & (PossibleMatch.user1_choice == MatchChoice.like))
        )
    
    def my_matches(self) -> list[PossibleMatch]:
         return PossibleMatch.query.filter(
            # either user1 or user2 is me
            ((PossibleMatch.user1_public_id == self.public_id) | (PossibleMatch.user2_public_id == self.public_id)) 
            # user1 and user2 like each other
          & ((PossibleMatch.user2_choice == MatchChoice.like) & (PossibleMatch.user1_choice == MatchChoice.like))
        )


def set_enum_valid(self: object, enum_: Enum|list, values: list, propname: str):
    if isinstance(enum_, EnumType):
        return setattr(self, propname, json.dumps([v for v in values if enum_(v) in enum_]))
    return setattr(self, propname, json.dumps([v for v in values if v in enum_]))


class PossibleMatch(db.Model):
    __tablename__ = 'possible_matches'
    id              = db.Column(db.Integer, primary_key=True)
    user1_public_id = db.Column(db.String(36),  db.ForeignKey('users.public_id'))
    user2_public_id = db.Column(db.String(36),  db.ForeignKey('users.public_id'))
    user1_choice    = db.Column(db.Enum(MatchChoice),   default=MatchChoice.none)
    user2_choice    = db.Column(db.Enum(MatchChoice),   default=MatchChoice.none)
    messages        = db.relationship('Message', backref='possible_match')
    matched_timestamp = db.Column(db.Integer,           default=0)

    @property
    def user1(self) -> User:
        return User.query.filter(User.public_id == self.user1_public_id).first()

    @property
    def user2(self) -> User:
        return User.query.filter(User.public_id == self.user2_public_id).first()

    def get_other_user(self, my_id: str) -> User:
        if self.user1_public_id == my_id:
            return self.user2
        if self.user2_public_id == my_id:
            return self.user1
        raise RuntimeError("This is not your PossibleMatch. You are not user1, nor user2.")

    def messages_slice(self, start: int, end: int) -> list[Message]:
        return Message.query.filter(Message.possible_match_id == self.id).order_by(Message.id.desc()).slice(start, end).all()
    
    @classmethod
    def get_match(cls, my_pid: str, other_pid: str) -> PossibleMatch:
        return cls.query.filter(
            ((PossibleMatch.user1_public_id == my_pid) & (PossibleMatch.user2_public_id == other_pid)
            | (PossibleMatch.user2_public_id == my_pid) & (PossibleMatch.user1_public_id == other_pid))
            & ((PossibleMatch.user1_choice == MatchChoice.like) & (PossibleMatch.user2_choice == MatchChoice.like))
        ).first()

class Message(db.Model):
    __tablename__       = "messages"
    id                  = db.Column(db.Integer, primary_key=True)
    possible_match_id   = db.Column(db.Integer,     db.ForeignKey('possible_matches.id'))
    author              = db.Column(db.String,      db.ForeignKey('users.public_id'))
    timemstamp          = db.Column(db.Integer,         default=lambda: time.mktime(datetime.now().timetuple()))
    message             = db.Column(db.String(4000),    default="")

    def json(self) -> dict[str, str|int]:
        return {
            "id":           self.id,
            "author":       self.author,
            "timestamp":    self.timemstamp,
            "message":      self.message,
        }


# Stwórz trigger `make_pairs`.
# Aktywuj trigger za każdym razem po INSERT w tabeli `users` - czyli po utworzeniu nowego usera
# Treść triggera - właściwie zbiór komend, które zostaną uruchomione:
#   - Stwórz PossibleMatch dla nowego usera i każdego dotychczasowego usera w bazie danych
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
    