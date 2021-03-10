from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# SCHEMA for forum

# log in/sign up schema

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    username = db.Column(db.String(14),
                    nullable=False,
                    unique=True)
    password = db.Column(db.String(99), nullable=False)

