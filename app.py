from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timezone, datetime, timedelta
from data_handler import db, User, bcrypt, app, Message, TokenBlocklist, Listing, jwt, Chat, init_db
from flask_jwt_extended import (
JWTManager, jwt_required, create_access_token, get_jwt, get_jwt_identity
)

"""
This file contains the main code for the backend of the web application.
It contains the code for the user authentication, user profile management,
and the listings management.
"""

# @app.before_request
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    """
    Function that checks if the token is revoked.
    A token is revoked if it is in the blocklist.
    """
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

# ______________________________
# ---------- Homepage ---------- 
@app.route("/", methods=["GET"])
@jwt_required(optional=True)
def home_page():
    """
    Function that handles what happens when the user
    visits the home page.
    """
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({"message": "Welcome to LiU-böcker!", "status": "You are logged in as {}".format(current_user)}), 200
    return jsonify({"message": "Welcome to LiU-böcker!", "status": "You are not logged in."}), 200

# _________________________________________
# ---------- User authentication ---------- 
@app.route("/login", methods=["POST"])
def login_page():
    """
    Function that handles the login process for users.
    """
    data = request.get_json()
    user = User.query.filter_by(name=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user, expires_delta=timedelta(days=1))
        return jsonify({"message": "Welcome back!"}, access_token=access_token), 200
    return jsonify("ERROR: Invalid username or password."), 401

@app.route("/signup", methods=["POST"])
def signup_page():
    """
    Function that handles the signup process for users.
    """
    data = request.get_json()

    if User.query.filter_by(name=data["username"]).first():
        return jsonify("ERROR: Username already exists."), 400
    if User.query.filter_by(email=data["email"]).first(): 
        return jsonify("ERROR: Email is already used."), 400
    if User.query.filter_by(phone_number=data["phone_number"]).first():
        return jsonify("ERROR: Phone number is already used."), 400
    

    db.session.add(
        User(username=data["username"], password=data["password"],
        email=data["email"], first_name=data["first_name"], last_name=data["last_name"], 
        phone_number=data["phone_number"]))

    db.session.commit()
    return redirect("/login", 200, jsonify({"message": "Successfully signed up"}))


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout_page():
    """
    Function that handles the logout process for users.
    """
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, revoked_at=now))
    db.session.commit()
    return redirect("/", 200, jsonify({"message": "Successfully logged out"}))
# __________________________________
# ---------- User profile ----------
 
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile_page():
    """
    The function that handles the process of showing the user profile.
    """
    user = get_jwt_identity()
    if not user:
        return redirect("/login")
    return jsonify(user.serialize())
    # return jsonify({"username": user.username, "email": user.email, "phone_number": user.phone_number,
    #                  "first_name": user.first_name, "last_name": user.last_name}), 200

@app.route("/profile", methods=["POST"])
@jwt_required()
def edit_profile_page():
    """
    Function that handles the process of editing a user profile.
    That also handles if some fields are not filled in.
    """
    user = get_jwt_identity()
    if not user:
        return redirect("/login")
    data = request.get_json()
    if data["phone_number"] != None:
        user.phone_number = data["phone_number"]
    if data["first_name"] != None:
        user.first_name = data["first_name"]
    if data["last_name"] != None:
        user.last_name = data["last_name"]
    if data["password"] != None:
        user.password = data["password"]
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

@app.route("/profile/delete", methods=["POST"])
@jwt_required()
def delete_profile_page(): #Remove all user content/data
    """
    Function that handles the process of deleting a user profile.
    """
    user = get_jwt_identity()
    if not user:
        return redirect("/login")
    db.session.delete(user)
    db.session.commit()
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    return redirect("/", 200, jsonify({"message": "Profile deleted successfully"}))

# _________________________________________
# ---------- Listings management ---------- 

@app.route("/listing/add", methods=["POST"])
@jwt_required()
def add_listing_page():
    """
    Function that handles the process of adding a new book listing.
    """
    user = get_jwt_identity()
    if not user:
        return redirect("/login")
    data = request.get_json()
    new_listing = Listing(
        title=data["title"], price=data["price"], location=data["location"],
        description=data["description"], isbn=data["isbn"], seller_id=user)
    if not new_listing:
        return jsonify("ERROR: Listing could not be created"), 400
    db.session.add(new_listing)
    db.session.commit()
    return jsonify({"message": "Listing has been posted"}), 200

@app.route("/listing/edit/<ListingID>", methods=["POST", "GET"])
@jwt_required()
def edit_listing_page(listing_id):
    """
    Function that handles the process of editing a book listing.
    """
    user = get_jwt_identity()
    listing = Listing.query.get(listing_id)

    if not user:
        return redirect("/login")
    if not listing:
        return jsonify("ERROR: Listing not found"), 400
    if listing.seller_id != user.id:
        return jsonify("ERROR: You are not the owner of this listing"), 400
    if request.method == "POST":
        data = request.get_json()   
        if data["description"] != None:
            listing.description = data["description"]
        if data["location"] != None:
            listing.location = data["location"]
        if data["title"] != None:
            listing.title = data["title"]
        if data["price"] != None:
            listing.price = data["price"]
        if data["isbn"] != None:
            listing.isbn = data["isbn"]

        db.session.commit()
        return redirect("/listing/edit/" + listing_id, 200, jsonify(
            {"message": "Listing updated successfully"}))
    else: # If method is GET, get the listing 
        return jsonify(listing.serialize())

@app.route("/listing/delete/<ListingID>", methods=["DELETE"])
@jwt_required()
def delete_listing_page(ListingID):
    """
    Function that handles the process of deleting a book listing.
    """
    listing = Listing.query.filter_by(id=ListingID).first()
    if listing and listing.seller_id == get_jwt_identity(): # Kommer denna jämförelse funka? ger get_jwt_identity() id på en user?
        db.session.delete(listing)
        db.session.commit()
        return "", 200
    return jsonify("ERROR: Listing was not found."), 400

@app.route("/listing/<ListingID>", methods=["GET"])
@jwt_required()
def listing_page(ListingID):
    """
    Function that handles the process of getting a book listing.
    """
    listing = Listing.query.filter_by(id=ListingID).first()
    if listing:
        return jsonify(listing.serialize()), 200
    return jsonify("ERROR: Listing was not found."), 400

@app.route("/listings", methods=["GET"])
@jwt_required()
def listings_page():
    """
    Function that handles the process of displaying all book listings.
    """
    listings = Listing.query.all()
    if listings:
        return jsonify([listing.serialize() for listing in listings]), 200
    return jsonify("ERROR: No listings found."), 400

@app.route("/listings/search", methods=["GET"])
@jwt_required()
def search_listings_page():
    """
    Function that handles the process of searching for book listings.
    """
    query = request.args.get("query")
    listings = Listing.query.filter_by(title=query)
    if listings:
        return jsonify([listing.serialize() for listing in listings]), 200
    return jsonify("ERROR: No listings found."), 400

# ______________________________
# ---------- Chatting ---------- 

@app.route("/messages/all", methods=["GET"])
@jwt_required()
def all_chats_page():
    """
    Function that handles the process of displaying all chats for a user.
    """
    user = get_jwt_identity()
    if not user:
        return redirect("/login")
    chats = Chat.query.filter_by(buyer_id=user)
    chats += Chat.query.filter_by(seller_id=user)
    if not chats:
        return jsonify({"message": "You have no chats yet."}), 200
    return jsonify([{"messages": chat.messages, "id": chat.id, "listing": chat.listing, 
    "buyer": chat.buyer, "seller": chat.seller} for chat in chats]) # Borde va säljaren, titel på listing, bild på listing, senaste meddelandet och dess tid.
    # , "read_by": [user.name for user in message.readers]
    # Ksk kan använda serialize() i returnen?

@app.route("/messages/int:user_id", methods=["GET"])
@jwt_required()
def chat_page():
    """
    Function that handles the process of displaying a chat between two users.
    """
    selected_chat_id = request.get_json()["chat_id"]
    user = get_jwt_identity()
    if not user:
        return redirect("/login")
    if not selected_chat_id:
        return jsonify("ERROR: No chat id was provided."), 400
    messages = Message.query.filter_by(chat_id=selected_chat_id).all()
    if not messages:
        return jsonify({"message": "You have no messages yet."}), 200
    return jsonify([message.message for message in messages])

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    app.debug = True
    app.run()


# TODO: Add redirect to log-in page if jwt_required sends error.
# TODO: Possibility to log in with email, Google, LiuID???
# TODO: Add student.liu.se to email verification?
# TODO: Add all templates (eg: view_listing_page)
# TODO: Add search function
# TODO: Add image upload to listing
# TODO: Add image upload to profile
# TODO: Add image upload to chat
# TODO: Add image upload to message
# TODO: Add a user review/rating system?
# TODO: Delete_profile ska deletea allt som usern har gjort eller göra om usern till
#       en "deleted user" som syns i chattar mm.
# TODO: I add_listing_page ksk kolla att alla fält för en listing är ifyllda. Att
#       inlägget har ett pris, location, mm?

