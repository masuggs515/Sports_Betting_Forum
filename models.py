from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

# SCHEMA for forum

# log in/sign up schema

class User(db.Model):
    """users table"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    email = db.Column(db.Text,
                    nullable=False,
                    unique=True)
    username = db.Column(db.String(20),
                    nullable=False,
                    unique=True)
    password = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text,
                            default='/static/images/defaultProfileImage.jpg')

    @classmethod
    def signup(cls, username, password, email):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            email=email,
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    comment = db.relationship("Comment",cascade="all, delete-orphan", backref="user")
    like = db.relationship("Like", cascade="all, delete-orphan", backref="user")

# Save game schema

class Game(db.Model):
    """games"""

    __tablename__ = "games"

    id = db.Column(db.Text,
                    primary_key=True)
    
    team_one = db.Column(db.Text)

    team_two = db.Column(db.Text)

    team_one_odds = db.Column(db.Text)

    team_two_odds = db.Column(db.Text)

    comment = db.relationship("Comment", cascade="all, delete-orphan", backref='game')

# Comments for game schema

class Comment(db.Model):
    """comments table"""

    __tablename__ = "comments"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete='cascade'),
                        nullable=False)

    game_id = db.Column(db.Text,
                        db.ForeignKey("games.id", ondelete='cascade'),
                        nullable=False)

    text = db.Column(db.Text,
                    nullable=False)

    timestamp = db.Column(db.DateTime,
                    nullable=False,
                    default=datetime.now)

    like = db.relationship("Like", cascade="all, delete-orphan", backref="comment")

# Likes schema
    
class Like(db.Model):
    """likes table"""

    __tablename__ = "likes"

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete='cascade'),
                        primary_key=True,
                        nullable=False)

    comment_id = db.Column(db.Integer,
                        db.ForeignKey("comments.id", ondelete='cascade'),
                        primary_key=True,
                        nullable=False)