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
app.config['JWT_SECRET_KEY'] = "Eliottana"

jwt = JWTManager(app)
db = SQLAlchemy(app)

# -------------------------------------DATABASE START-------------------------------------

# --------------------------------------DATABASE END--------------------------------------

# ______________________________
# ---------- Homepage ---------- 
@app.route("/", methods=["GET"])
def home_page():
    """
    The main page of the application where users can view the
    available books for sale and search for books based on 
    different criteria such as author, title, or subject.
    """
    pass

# _________________________________________
# ---------- User authentication ---------- 
@app.route("/login", methods=["POST"])
def login_page():
    """
    The page where users can log in to their account.
    """
    pass

@app.route("/login", methods=["GET"])
def login_process_page():
    """
    The route that processes the user's login credentials and 
    logs them in.
    """
    pass

@app.route("/signup", methods=["POST"])
def signup_page():
    """
    The page where users can sign up for a new account.
    """
    pass

@app.route("/signup", methods=["GET"])
def signup_process_page():
    """
    The route that processes the user's sign up information 
    and creates a new account in the database.
    """
    pass

@app.route("/logout", methods=["GET"])
def logout_process_page():
    """
    The route that logs out the current user and redirects 
    them to the home page.
    """
    pass 

# __________________________________
# ---------- User profile ---------- 
@app.route("/profile", methods=["GET"])
def profile_page():
    """
    The page where users can view and edit their profile
    information.
    """
    pass

@app.route("/profile", methods=["POST"])
def profile_process_page():
    """
    The route that processes the user's updated profile
    information and saves it to the database.
    """
    pass

# _____________________________________
# ---------- Book management ---------- 
@app.route("/sell", methods=["GET"])
def add_listing_page():
    """
    The page where users can create a new book listing
    for sale.
    """
    pass

@app.route("/sell", methods=["POST"])
def add_listing_process_page():
    """
    The route that processes the book information and 
    saves it to the database as a new listing.
    """
    pass

@app.route("/edit/int:book_id", methods=["GET"])
def edit_listing_page():
    """
    The page where users can edit an existing book listing.
    """
    pass

@app.route("/edit/int:book_id", methods=["POST"])
def edit_listing_process_page():
    """
    The route that processes the updated book information 
    and saves it to the database.
    """
    pass

@app.route("/delete/int:book_id", methods=["GET"])
def delete_listing_page():
    """
    The route that deletes a book listing from the 
    database.
    """
    pass

# ______________________________
# ---------- Chatting ---------- 
@app.route("/messages", methods=["GET"])
def all_chat_page():
    """
    The page where users can view their message history 
    and open a chat with a specific user.
    """
    pass

@app.route("/messages/int:user_id", methods=["GET"])
def chat_page():
    """
    The page where users can chat with another user.
    """
    pass

@app.route("/messages/int:user_id", methods=["GET"])
def chat_process_page():
    """
    The route that processes the user's message and 
    saves it to the database.
    """
    pass


# # ----------------------------------------------------------------------------

# read_by = db.Table("read_by",
#     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
#     db.Column("message_id", db.String(12), db.ForeignKey("message.id"), primary_key=True))


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True)
#     messages = db.relationship('Message', backref='person', lazy=True)
#     read_by = db.relationship('Message', secondary=read_by, back_populates='readers')
#     password = db.Column(db.String(200), unique=False, nullable=False)

#     def __init__(self, name, password):
#         self.name = name
#         self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
#     def to_dict(self):
#         result = {}
#         result['name'] = self.name
#         result['id'] = self.id
#         result['messages'] = [x.message for x in self.messages]
#         return result


# class Message(db.Model):
#     id = db.Column(db.String(24), primary_key=True, default=lambda: str(secrets.token_hex(12)))
#     message = db.Column(db.String(140))
#     author = db.Column(db.String(50), db.ForeignKey('user.name'), nullable=False)
#     readers = db.relationship("User", secondary=read_by, back_populates="read_by")

# class TokenBlocklist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     jti = db.Column(db.String(36), nullable=False, index=True)
#     revoked_at = db.Column(db.DateTime, nullable=False)

# def init_db():
#     db.drop_all()
#     db.create_all()
#     meta = db.metadata
#     for table in reversed(meta.sorted_tables):
#         db.session.execute(table.delete())


# @jwt.token_in_blocklist_loader
# def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
#     jti = jwt_payload["jti"]
#     token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
#     return token is not None

# # @jwt.revoked_token_loader
# # def token_revoked_callback(jwt_header, jwt_payload):
# #     jti = jwt_payload["jti"]
# #     token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
# #     if token is not None:
# #         return jsonify({"msg": "Token has been revoked"}), 401
# #     else:
# #         return jsonify({"msg": "Token is valid"})

# # ----------------------------------------------------------------------------

# @app.route("/")
# @jwt_required()
# def welcome():
#     user = get_jwt_identity()
#     return "Welcome " + user


# @app.route("/messages", methods=["POST"])
# @jwt_required()
# def post_message():
#     """Creates a new message with an unique ID if the
#     request method is 'POST'. """
#     if request.method == "POST":
#         data = request.get_json()
#         new_message = Message(message=data["message"], author=get_jwt_identity())
#         db.session.add(new_message)
#         db.session.commit()
#         return jsonify({"id": new_message.id}) 
#     return jsonify("ERROR: Illegal request method."), 405


# @app.route("/messages", methods=["GET"])
# def get_messages():
#     """Fetches all messages in the database."""
#     if request.method == "GET":
#         messages = Message.query.all()
#         return jsonify([{'message': message.message, 'id': message.id, 'author': message.author, 
#         "read_by": [user.name for user in message.readers]} for message in messages])
#     return jsonify("ERROR: Illegal request method."), 405


# @app.route("/messages/<MessageID>", methods=["GET"])
# def get_message(MessageID):
#     """Return the message with the given ID if existing"""
#     if request.method == "GET":
#         message = Message.query.filter_by(id=MessageID).first()
#         if message:
#             return jsonify({"id": message.id, "message": message.message, "author": message.author, 
#             "read_by": [user.name for user in message.readers]})
#         return jsonify("ERROR: Message was not found."), 400
#     return jsonify("ERROR: Illegal request method."), 405


# @app.route("/messages/<MessageID>", methods=["DELETE"])
# @jwt_required()
# def delete_message(MessageID):
#     """Deletes the message with the given ID if existing"""
#     if request.method == "DELETE":
#         message = Message.query.filter_by(id=MessageID).first()
#         if message and message.author == get_jwt_identity():
#             db.session.delete(message)
#             db.session.commit()
#             return "", 200
#         return jsonify("ERROR: Message was not found."), 400
#     return jsonify("ERROR: Illegal request method."), 405


# @app.route("/messages/<MessageID>/read/<UserId>", methods=["POST"])
# @jwt_required()
# def mark_as_read(MessageID, UserId):
#     """Marks the message with the given ID as read by the given user"""
#     if request.method == "POST":
#         user = User.query.filter_by(id=UserId).first()
#         message = Message.query.filter_by(id=MessageID).first()
#         if not user:
#             return jsonify("ERROR: User was not found."), 400
#         if not message:
#             return jsonify("ERROR: Message was not found."), 400
#         if message in user.read_by:
#             return jsonify("Message already marked as read."), 200
#         user.read_by.append(message)
#         db.session.commit()
#         return "", 200
#     return jsonify("ERROR: Illegal request method."), 405


# @app.route("/messages/unread/<UserId>", methods=["GET"])
# @jwt_required()
# def get_unread_messages(UserId):
#     """Returns all existing messages not read by the given user"""
#     if request.method == "GET":
#         user = User.query.filter_by(id=UserId).first()
#         if user:
#             unread_messages = Message.query.filter(~Message.readers.contains(user)).all()
#             if not unread_messages:
#                 return jsonify("ERROR: No unread messages were found."), 400
#             else:
#                 # for message in unread_messages: #-- Marks fetched messages as read.
#                 #     user.read_by.append(message)
#                 #     db.session.commit()
#                 return jsonify([{"id": message.id, "message": message.message, "author": message.author}
#                                 for message in unread_messages])
#         return jsonify("ERROR: user was not found."), 400
#     return jsonify("ERROR: Illegal request method."), 405


# @app.route("/user", methods=["POST"])
# def create_user():
#     if request.method == "POST":
#         data = request.get_json()
#         new_user = User(name=data["name"], password=data["password"])
#         existing_user = User.query.filter_by(name=new_user.name).first()
#         if not existing_user:
#             db.session.add(new_user)
#             db.session.commit()
#             return "", 200
#         return jsonify("ERROR: Username already exists."), 400
#     return jsonify("ERROR: Illegal request method."), 405


# @app.route("/user/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     user = User.query.filter_by(name=data["name"]).first()
#     if user == None:
#         return jsonify({"message": "Invalid password"}), 400

#     if bcrypt.check_password_hash(user.password, data["password"]):
#         token = create_access_token(identity=user.name)
#         return jsonify(access_token=token), 200
    
#     return jsonify({"message": "Invalid password"}), 400


# @app.route("/user/logout", methods=["POST"])
# @jwt_required()
# def logout():
#     jti = get_jwt()["jti"]
#     now = datetime.now(timezone.utc)
#     db.session.add(TokenBlocklist(jti=jti, revoked_at=now))
#     db.session.commit()
#     return jsonify({'message': 'Successfully logged out'}), 200    

# # ----------------------------------------------------------------------------

# if __name__ == "__main__":
#     app.debug = True
#     app.run()


# #TODO Add redirect to log-in page if jwt_required sends error.