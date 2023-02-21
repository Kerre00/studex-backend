from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timezone, datetime, timedelta
from data_handler import db, User, bcrypt, app, Message, TokenBlocklist, Listing, jwt, Chat
from flask_jwt_extended import (
JWTManager, jwt_required, create_access_token, get_jwt, get_jwt_identity
)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

# ______________________________
# ---------- Homepage ---------- 
@app.route("/", methods=["GET"])
@jwt_required(optional=True)
def home_page():
    """
    The main page of the application where users can view the
    available books for sale and search for books based on 
    different criteria such as author, title, or subject.
    """
    user = get_jwt_identity()
    if user:
        return jsonify("Welcome to LIU-Böcker.se " + user)
    return jsonify("Welcome to LIU-Böcker.se")

# _________________________________________
# ---------- User authentication ---------- 
@app.route("/login", methods=["POST"])
def login_page():
    """
    The page where users can log in to their accounts.
    """
    data = request.get_json()
    user = User.query.filter_by(name=data["name"]).first()
    if user == None:
        return jsonify({"message": "Invalid password"}), 400

    if bcrypt.check_password_hash(user.password, data["password"]):
        token = create_access_token(identity=user.name)
        return jsonify(access_token=token), 200
    
    return jsonify({"message": "Invalid password"}), 400


@app.route("/signup", methods=["POST"])
def signup_page():
    """
    The page where users can sign up for a new account.
    """
    if request.method == "POST":
        data = request.get_json()
        new_user = User(username=data["username"], password=data["password"],
        email=data["email"], first_name=data["first_name"], last_name=data["last_name"], 
        phone_number=data["phone_number"])
        existing_username = User.query.filter_by(name=new_user.username).first()
        existing_email = User.query.filter_by(email=new_user.email).first()
        if not existing_username and not existing_email:
            db.session.add(new_user)
            db.session.commit()
            return "", 200
        return jsonify("ERROR: Username already exists."), 400


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout_page():
    """
    The route that logs out the current user and redirects 
    them to the home page.
    """
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, revoked_at=now))
    db.session.commit()
    # return jsonify({"message": "Successfully logged out"}), 200
    return redirect("/", 200, jsonify({"message": "Successfully logged out"}))

# __________________________________
# ---------- User profile ----------
 
@app.route("/profile", methods=["GET", "POST"])
@jwt_required()
def profile_page():
    """
    The page where users can view and edit their profile
    information.
    """
    user = get_jwt_identity()
    if not user:
        return redirect("/login")
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        user.name = name
        user.email = email
        user.set_password(password)
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200

# _________________________________________
# ---------- Listings management ---------- 

@app.route("/listing/add", methods=["POST", "GET"])
@jwt_required()
def add_listing_page():
    """
    The page where users can create a new book listing
    for sale.
    """
    if request.method == "POST":
        data = request.get_json()
        user = get_jwt_identity()
        new_listing = Listing(
            title=data["title"], price=data["price"], location=data["location"],
            description=data["description"], isbn=data["isbn"], seller_id=user)
        db.session.add(new_listing)
        db.session.commit()
        return jsonify({"message": "Listing has been posted"}), 200
    else:
        pass
        # Render display form for adding a new listing
        # return render_template("add_listing.html")

@app.route("/listing/edit/<ListingID>", methods=["GET"])
@jwt_required()
def edit_listing_page(listing_id):
    """
    The page where users can edit an existing book listing.
    """
    listing = Listing.query.get(listing_id)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        price = request.form["price"]
        location = request.form["location"]
        listing["title"] = title
        listing["description"] = description
        listing["price"] = price
        listing["location"] = location
        return redirect("/listings")
    else:
        pass
        #template for editing listing

@app.route("/listing/delete/<ListingID>", methods=["GET"])
@jwt_required()
def delete_listing_page(ListingID):
    """
    The route that deletes a book listing from the 
    database.
    """
    listing = Listing.query.filter_by(id=ListingID).first()
    if listing and listing.seller_id == get_jwt_identity():
        db.session.delete(listing)
        db.session.commit()
        return "", 200
    return jsonify("ERROR: Listing was not found."), 400


# ______________________________
# ---------- Chatting ---------- 

@app.route("/messages/all", methods=["GET"])
@jwt_required()
def all_chats_page():
    """
    The page where users can view their message history 
    and open a chat with a specific user.
    """
    user = get_jwt_identity()
    chats = Chat.query.filter_by(buyer_id=user)
    chats =+ Chat.query.filter_by(seller_id=user)
    return jsonify([{"messages": chat.messages, "id": chat.id, "listing": chat.listing, 
    "buyer": chat.buyer, "seller": chat.seller} for chat in chats]) # Borde va säljaren, titel på listing, bild på listing, senaste meddelandet och dess tid.
    # , "read_by": [user.name for user in message.readers]



@app.route("/messages/int:user_id", methods=["GET"])
@jwt_required()
def chat_page():
    """
    The page where users can chat with another user.
    """
    selected_chat_id = request.get_json()["chat_id"]
    messages = Message.query.filter_by(chat_id=selected_chat_id).all()
    return jsonify([message.message for message in messages])

# # ----------------------------------------------------------------------------

if __name__ == "__main__":
    app.debug = True
    app.run()

# TODO: Add redirect to log-in page if jwt_required sends error.
# TODO: Possibility to log in with email, Google, LiuID???
# TODO: Add phonenumber to User table
# TODO: Add student.liu.se to email verification?
# TODO: Add all templates (eg: view_listing_page)