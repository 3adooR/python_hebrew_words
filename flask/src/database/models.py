import uuid

from werkzeug.security import generate_password_hash

from src import db


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    rus = db.Column(db.String(255), nullable=False)
    heb = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Integer, default=0)

    def __init__(self, rus, heb):
        self.uuid = str(uuid.uuid4())
        self.rus = rus
        self.heb = heb

    def __repr__(self):
        return f'Word({self.uuid}, {self.rus}, {self.heb})'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, is_admin=False):
        self.uuid = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f'User({self.uuid}, {self.username}, {self.email})'

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()
