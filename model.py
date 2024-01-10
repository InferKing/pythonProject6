from main import db
from flask_login import UserMixin
from datetime import datetime
import json


def to_json(obj):
    temp = obj.__dict__
    temp.pop('_sa_instance_state')
    if 'created_on' in temp and temp['created_on'] is not None:
        temp['created_on'] = temp['created_on'].strftime('%a %d %b %Y, %I:%M:%p')
    if 'updated_on' in temp and temp['updated_on'] is not None:
        temp['updated_on'] = temp['updated_on'].strftime('%a %d %b %Y, %I:%M:%p')
    return json.dumps(temp)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    posts = db.relationship('Post', backref='data')

    def __init__(self, id, username, password, mail):
        self.id = id
        self.username = username
        self.password = password
        self.mail = mail

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        return cls(**data)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
