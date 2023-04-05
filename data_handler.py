from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import os
import sys
from flask_bcrypt import Bcrypt
from datetime import timezone, datetime, timedelta
from flask_jwt_extended import (
JWTManager, jwt_required, create_access_token, get_jwt, get_jwt_identity
)
from sqlalchemy.orm import validates

"""
This file contains the database models for the web application.
It contains the models for the user, listings, and messages.
"""

app = Flask(__name__)
bcrypt = Bcrypt(app)

cur_dir = os.path.dirname(os.path.abspath(__file__))

if "pytest" in sys.modules:
    db_uri = "sqlite:///" + cur_dir + "/test_database.db"
elif 'WEBSITE_HOSTNAME' in os.environ:  # running on Azure: use postgresql
    database = os.environ['DBNAME']  # postgres
    host_root = '.postgres.database.azure.com'
    host = os.environ['DBHOST'] + host_root  # app-name + root
    user = os.environ['DBUSER']
    password = os.environ['DBPASS']
    db_uri = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
    debug_flag = False
else: # when running locally: use sqlite
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    db_uri = "sqlite:///" + cur_dir + "/database.db"
    debug_flag = True

ACCESS_EXPIRES = timedelta(hours=1)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = "Elliotana"

jwt = JWTManager(app)
db = SQLAlchemy(app)

# -------------------------------------DATABASE START-------------------------------------

book_course = db.Table("listing_course", # This is the table that connects the listing and the course
    db.Column("listing_id", db.Integer, db.ForeignKey("listing.id"), primary_key=True),
    db.Column("course_id", db.String(12), db.ForeignKey("course.id"), primary_key=True))

book_program = db.Table("listing_program", # This is the table that connects the listing and the program
    db.Column("listing_id", db.Integer, db.ForeignKey("listing.id"), primary_key=True),
    db.Column("program_id", db.String(12), db.ForeignKey("program.id"), primary_key=True))

# book_topic = db.Table("listing_topic", # This is the table that connects the listing and the topic
#     db.Column("listing_id", db.Integer, db.ForeignKey("listing.id"), primary_key=True),
#     db.Column("topic_id", db.String(12), db.ForeignKey("topic.id"), primary_key=True))

class User(db.Model):
    """
    This class represents the user model.
    """
    id = db.Column(db.String(12), primary_key=True, default=lambda: str(secrets.token_hex(12)))
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(50), nullable=True, default="No Name")
    last_name = db.Column(db.String(50), nullable=True, default="No Last Name")
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    phone_number = db.Column(db.String(30), nullable=True, unique=True)
    listings = db.relationship("Listing", backref=db.backref("user", lazy=True))
    chats = db.relationship("Chat", backref=db.backref("user", lazy=True))
    messages = db.relationship("Message", backref=db.backref("user", lazy=True))

    def __init__(self, username, password, email, first_name, last_name):
        
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


    @validates("username")
    def validate_username(self, key, username):
        """
        This method validates the username.
        """
        valid_chars = "0123456789abcdefghijklmnopqrstuvwxyzåäöABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
        if len(username) < 4:
            raise ValueError("Username must be between 4 and 30 characters long")
        for char in username:
            if char not in valid_chars:
                raise ValueError("Username can only contain: A-ö, a-ö or 0-9")
        return username
    

    @validates("password")
    def validate_password(self, key, password):
        """
        This method validates the password.
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        dig, upp, low = False, False, False
        for char in password:
            if char.isdigit():
                dig = True
            if char.isupper():
                upp = True
            if char.islower():
                low = True
        if dig and upp and low:
            return password
        raise ValueError("Password must contain: digit, lower and uppercase")


    @validates("email")
    def validate_email(self, key, email):
        """
        This method validates the email.
        """
        if not email or "@" not in email:
            raise ValueError("Not a valid email address")
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already in use")
        return email
    


class Chat(db.Model):
    """
    This class represents the chat model.
    """
    id = db.Column(db.String(12), primary_key=True, default=lambda: str(secrets.token_hex(12)))
    listing_id = db.Column(db.String(12), db.ForeignKey("listing.id"), nullable = False)
    buyer_id = db.Column(db.String(12), db.ForeignKey("user.id"), nullable=False)
    seller_id = db.Column(db.String(12), db.ForeignKey("user.id"), nullable=False)
    listing = db.relationship("Listing", backref=db.backref("chats", lazy=True))
    buyer = db.relationship("User", foreign_keys=[buyer_id])
    seller = db.relationship("User", foreign_keys=[seller_id])
    messages = db.relationship("Message", backref='chat', lazy=True)


class Message(db.Model):
    """
    This class represents the message model.
    """
    id = db.Column(db.String(12), primary_key=True, default=lambda: str(secrets.token_hex(12)))
    message = db.Column(db.String(140), nullable=False)
    author_id = db.Column(db.String(12), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    author = db.relationship("User", foreign_keys=[author_id])


class Listing(db.Model):
    """
    This class represents the listing model.
    """
    id = db.Column(db.String(12), primary_key=True, default=lambda: str(secrets.token_hex(12)))
    title = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, default=0)
    location = db.Column(db.String(30), nullable=True)
    description = db.Column(db.String(240), nullable=True)
    # isbn = db.Column(db.String(17), nullable=True)
    seller_id = db.Column(db.String(12), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    viewed_by = db.relationship("Viewed", backref=db.backref("listing", lazy=True))
    seller = db.relationship("User", foreign_keys=[seller_id])
    course = db.relationship("Course", backref=db.backref("listings", lazy=True))
    program = db.relationship("Program", backref=db.backref("listings", lazy=True))
    # images = db.relationship("Image", backref=db.backref("listing", lazy=True))

# class Image(db.Model):
#     """
#     This class represents the image model.
#     """
#     id = db.Column(db.String(12), primary_key=True, default=lambda: str(secrets.token_hex(12)))
#     image = db.Column(db.String(100), nullable=False)
#     listing_id = db.Column(db.String(12), db.ForeignKey("listing.id"), nullable=False)


# class Topic(db.Model):
#     """
#     This class represents the topic search category model.
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True)


class Course(db.Model):
    """
    This class represents the course search category model.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


class Program(db.Model):
    """
    This class represents the program search category model.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


class TokenBlocklist(db.Model):
    """
    This class represents the token blocklist model.
    """
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime, nullable=False)


# --------------------------------------DATABASE END--------------------------------------

def init_db():
    """
    This method initializes the database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()