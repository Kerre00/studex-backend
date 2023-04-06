from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import os
import sys
from flask_bcrypt import Bcrypt
from datetime import timezone, datetime, timedelta
import re
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

favorite_listings = db.Table("favorite_listings", # This is the table that connects the user and the listing
    db.Column("user_id", db.String(12), db.ForeignKey("user.id"), primary_key=True),
    db.Column("listing_id", db.Integer, db.ForeignKey("listing.id"), primary_key=True))

viewed_listings = db.Table("viewed_listings", # This is the table that connects the user and the listing
    db.Column("user_id", db.String(12), db.ForeignKey("user.id"), primary_key=True),
    db.Column("listing_id", db.Integer, db.ForeignKey("listing.id"), primary_key=True))

# book_topic = db.Table("listing_topic", # This is the table that connects the listing and the topic
#     db.Column("listing_id", db.Integer, db.ForeignKey("listing.id"), primary_key=True),
#     db.Column("topic_id", db.String(12), db.ForeignKey("topic.id"), primary_key=True))

class User(db.Model):
    """
    This class represents the user model.
    """
    id = db.Column(db.String(12), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(30), nullable=True, unique=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=True) # The chat the user is currently in
    last_seen = db.Column(db.DateTime, nullable=True) # The last time the user was seen
    online = db.Column(db.Boolean, nullable=False, default=False) # If the user is online or not

    listings = db.relationship("Listing", backref=db.backref("user", lazy=True), cascade="all, delete-orphan") # Owner of the listing
    favorites = db.relationship("Listing", secondary=favorite_listings, backref=db.backref("favorited_by", lazy=True)) # Users favorite listings
    viewed_listings = db.relationship("Listing", secondary=viewed_listings, backref=db.backref("viewed_listings", lazy=True)) # Users viewed listings
    # profile_picture = db.relationship("Image", uselist=False, backref=db.backref("user", lazy=True), cascade="all, delete-orphan") # Profile picture

    def __init__(self, username, password, email, phone_number=None, first_name=None, last_name=None):
        
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.created_at = datetime.now(timezone.utc)
        self.id = secrets.token_hex(12)
        self.phone_number = phone_number
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @validates("username")
    def validate_username(self, key, username):
        """
        This method validates the username.
        """
        if len(username) < 4:
            raise ValueError("Username must be between 4 and 30 characters long")
        pattern = r'^[0-9a-zA-ZåäöÅÄÖ]+$'
        if not re.match(pattern, username):
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

    def __repr__(self):
        return f"{self.username}"
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            # "profile_picture": self.profile_picture[0].url if self.profile_picture else None
        }
    
    def login(self):
        """
        This method updates the user's last seen time to the current time when the user logs in.
        """
        self.last_seen = datetime.now(timezone.utc)
        self.online = True
        db.session.commit()

    def logout(self):
        """
        This method updates the user's last seen time to the current time when the user logs out.
        """
        self.last_seen = datetime.now(timezone.utc)
        self.online = False
        db.session.commit()

    def is_online(self):
        """
        This method checks whether the user is currently online.
        """
        if self.last_seen is None:
            return False
        now = datetime.now(timezone.utc)
        return (now - self.last_seen) < timedelta(minutes=10) # If the user was last seen less than 10 minutes ago, consider them online
    
    


class Listing(db.Model):
    """
    This class represents the listing model.
    """
    id = db.Column(db.String(12), primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(30), nullable=True)
    description = db.Column(db.String(240), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    seller_id = db.Column(db.String(12), db.ForeignKey("user.id"), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)

    # images = db.relationship("Image", backref=db.backref("listing", lazy=True), cascade="all, delete-orphan")
    seller = db.relationship("User", backref=db.backref("listing_seller", lazy=True))
    viewed_by = db.relationship("User", secondary=viewed_listings, backref=db.backref("viewed_listing", lazy=True))
    course = db.relationship('Course', backref='listings')
    program = db.relationship('Program', backref='listings')

    def __init__(self, title, price, location, description, course_id = None, program_id = None, seller_id = None):
        self.id = str(secrets.token_hex(12))
        self.title = title
        self.price = price
        self.location = location
        self.description = description
        self.course_id = course_id
        self.program_id = program_id
        # self.images = images
        self.seller_id = seller_id


    def __repr__(self):
        return f"{self.id}"
    
    def edit_listing(self, title, price, location, description):
        self.title = title
        self.price = price
        self.location = location
        self.description = description
        db.session.commit()

    def remove_listing(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "location": self.location,
            "description": self.description,
            "created_at": self.created_at,
            "course": self.course.serialize(),
            "program": self.program.serialize(),
            "seller": self.seller.serialize(),
            # "images": [image.serialize() for image in self.images]
        }

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
    messages = db.relationship("Message", backref=db.backref("chat", lazy=True), cascade="all, delete-orphan")

    def __init__(self, listing_id, buyer_id, seller_id, messages = []):
        self.id = secrets.token_hex(12)
        self.listing_id = listing_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.messages = messages

    def __repr__(self):
        return f"{self.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "listing": self.listing.serialize(),
            "buyer": self.buyer.serialize(),
            "seller": self.seller.serialize(),
            "messages": [message.serialize() for message in self.messages]
        }
    
    # Add new message to chat
    def add_message(self, message):
        self.messages.append(message)
        db.session.commit()

class Message(db.Model):
    """
    This class represents the message model.
    """
    id = db.Column(db.String(12), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(140), nullable=False)
    author_id = db.Column(db.String(12), db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    author = db.relationship("User", foreign_keys=[author_id])

    def __init__(self, message, author_id, chat_id):
        self.id = secrets.token_hex(12)
        self.created_at = datetime.now()
        self.message = message
        self.author_id = author_id
        self.chat_id = chat_id

    def __repr__(self):
        return f"{self.id}"
    
    def add_message_to_chat(self, message, author_id, chat_id):
        message = Message(message, author_id, chat_id)
        db.session.add(message)
        db.session.commit()

    

# class Image(db.Model):
#     """
#     This class represents the image model.
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(120), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
#     listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
#     user_id = db.Column(db.String(12), db.ForeignKey('user.id'))


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

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"

class Program(db.Model):
    """
    This class represents the program search category model.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"

class TokenBlocklist(db.Model):
    """
    This class represents the token blocklist model.
    """
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti):
        self.jti = jti
        self.revoked_at = datetime.datetime.now()

    def __repr__(self):
        return f"{self.id}"
    
    def is_revoked(self):
        return self.revoked_at is not None
    
    def revoke(self):
        self.revoked_at = datetime.datetime.now()
        db.session.commit()

    def unrevoke(self):
        self.revoked_at = None
        db.session.commit()

# --------------------------------------DATABASE END--------------------------------------

def init_db():
    """
    This method initializes the database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()