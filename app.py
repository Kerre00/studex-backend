from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timezone, datetime, timedelta
from data_handler import db, User, bcrypt, app, Message, TokenBlocklist, Listing, jwt, Chat, Program, Course, course_listings, program_listings, favorite_listings
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
def home_page(): #FUNGERAR
    """
    Function that handles what happens when the user
    visits the home page.
    """
    url = 'http://127.0.0.1:5000/signup'
    link = '<a href="{}">{}</a>'.format(url, url)
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({"message": "Welcome to LiU-böcker!", "status": "You are logged in as {}".format(current_user)}), 200
    return jsonify({"message": "Welcome to LiU-böcker!", "status": "You are not logged in. Please make an account at " + link}), 200

# _________________________________________
# ---------- User authentication ---------- 
@app.route("/login", methods=["POST"])
def login_page(): #FUNGERAR
    """
    Function that handles the login process for users.
    """
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        # if user.is_online():
        #     return jsonify("ERROR: User is already logged in."), 400
        access_token = create_access_token(identity=user.serialize(), expires_delta=timedelta(hours=1))
        user.login()
        return jsonify({"message": "Successfully logged in", "token": access_token}), 200
    return jsonify("ERROR: Invalid username or password."), 401

@app.route("/signup", methods=["POST"])
def signup_page(): #FUNGERAR
    """
    Function that handles the signup process for users.
    """
    data = request.get_json()

    if User.query.filter_by(username=data["username"]).first():
        return jsonify("ERROR: Username already exists."), 400
    if User.query.filter_by(email=data["email"]).first(): 
        return jsonify("ERROR: Email is already used."), 400
    if User.query.filter_by(phone_number=data.get("phone_number")).first() and data.get("phone_number"):
        return jsonify("ERROR: Phone number is already used."), 400

    # Initialize user with default values for optional arguments
    new_user = User(
        username=data["username"], 
        password=data["password"], 
        email=data["email"], 
        first_name=data.get("first_name"), 
        last_name=data.get("last_name"), 
        phone_number=data.get("phone_number")
    )
    
    db.session.add(new_user)

    db.session.commit()
    return redirect("/login", 200, jsonify({"message": "Successfully signed up"}))


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout_page(): #FUNGERAR
    """
    Function that handles the logout process for users.
    """
    identity = get_jwt_identity()
    db.session.add(TokenBlocklist(jti=get_jwt()["jti"]))
    db.session.commit()
    user = User.query.filter_by(id=identity['id']).first()
    user.logout()
    return redirect("/", 200, jsonify({"message": "Successfully logged out"}))
# __________________________________
# ---------- User profile ----------
 
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile_page(): #FUNGERAR
    """
    The function that handles the process of showing the user profile.
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity['id']).first()
    if not user:
        return redirect("/login", 400)
    return jsonify(user.serialize()), 200
    # return jsonify({"username": user.username, "email": user.email, "phone_number": user.phone_number,
    #                  "first_name": user.first_name, "last_name": user.last_name}), 200

@app.route("/profile", methods=["PUT"])
@jwt_required()
def edit_profile_page(): #FUNGERAR
    """
    Function that handles the process of editing a user profile.
    That also handles if some fields are not filled in.
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity['id']).first()
    if not user:
        return redirect("/login")
    data = request.get_json()

    user.phone_number = data.get("phone_number", user.phone_number)
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.password = data.get("password", user.password)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

@app.route("/profile/delete", methods=["DELETE"])
@jwt_required()
def delete_profile_page(): #Remove all user content/data
    """
    Function that handles the process of deleting a user profile.
    The deletion of the user profile also deletes all the listings
    which is handled by the cascade delete in the database.
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity['id']).first()
    if not user:
        return redirect("/login")
    db.session.add(TokenBlocklist(jti=get_jwt()["jti"]))
    db.session.delete(user)
    db.session.commit()
    return redirect("/", 200, jsonify({"message": "Account deleted successfully"}))

# _________________________________________
# ---------- Listings management ---------- 

@app.route("/listing/add", methods=["POST"])
@jwt_required()
def add_listing_page(): #FUNGERAR HALVT KOLLA LISTING_COURSE + LISTING_PROGRAM
    """
    Function that handles the process of adding a new book listing.
    """
    user = get_jwt_identity()
    if not user:
        return redirect("/login")
    data = request.get_json()

    if not data.get('title') or not data.get('price'):
        return jsonify("ERROR: Listing could not be created"), 400

    new_listing = Listing(
        title=data["title"], 
        price=data["price"], 
        owner_id=user["id"],
        location=data.get("location"),
        description=data.get("description"))
    
    # new_listing.course = Course.query.filter_by(id=data.get("course_id")).first()
    # new_listing.program = Program.query.filter_by(id=data.get("program_id")).first()

    db.session.add(new_listing)
    db.session.commit()
    return jsonify({"message": "Listing has been posted", "listing_id": new_listing.id}), 200

@app.route("/listing/edit/<ListingID>", methods=["PUT"])
@jwt_required()
def edit_listing_page(ListingID): #FUNGERAR HALVT KOLLA LISTING_COURSE + LISTING_PROGRAM
    """
    Function that handles the process of editing a book listing.
    """
    user = get_jwt_identity()
    listing = Listing.query.filter_by(id=ListingID).first()

    if not user:
        return redirect("/login")
    if not listing:
        return jsonify("ERROR: Listing not found"), 400
    if listing.owner_id != user['id']:
        return jsonify("ERROR: You are not the owner of this listing"), 400
    data = request.get_json()   

    listing.title = data.get("title", listing.title)
    listing.price = data.get("price", listing.price)
    listing.location = data.get("location", listing.location)
    listing.description = data.get("description", listing.description)
    # listing.course = data.get("course", listing.course)
    # listing.program = data.get("program", listing.program)

    db.session.commit()
    return redirect("/listing/edit/" + ListingID, 200, jsonify(
        {"message": "Listing updated successfully"}))


@app.route("/listing/delete/<ListingID>", methods=["DELETE"])
@jwt_required()
def delete_listing_page(ListingID): #FUNGERAR
    """
    Function that handles the process of deleting a book listing.
    """
    listing = Listing.query.filter_by(id=ListingID).first()
    identity = get_jwt_identity()
    if listing and listing.owner_id == identity['id']:
        db.session.delete(listing)
        db.session.commit()
        return jsonify({"message": "Listing deleted successfully"}), 200
    return jsonify("ERROR: Listing was not found."), 400

@app.route("/listing/<ListingID>", methods=["GET"])
@jwt_required(optional=True)
def listing_page(ListingID): # FUNGERAR
    """
    Function that handles the process of getting a book listing.
    """
    identity = get_jwt_identity()
    listing = Listing.query.filter_by(id=ListingID).first()
    if listing:
        if identity:
            user = User.query.filter_by(id=identity["id"]).first()
            if listing not in user.viewed_listings:
                user.viewed_listings.append(listing)
                db.session.commit()
        return jsonify(listing.serialize()), 200
    return jsonify("ERROR: Listing was not found."), 400

# Add listing to favourites
@app.route("/listing/<ListingID>/favourite", methods=["POST"])
@jwt_required()
def favourite_listing_page(ListingID): # FUNGERAR
    """
    Function that handles the process of adding a book listing to favourites.
    """
    listing = Listing.query.filter_by(id=ListingID).first()
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity["id"]).first()
    if listing and identity:
        if listing in user.favorites:
            return jsonify("ERROR: Listing is already in favourites."), 400
        user.favorites.append(listing)
        db.session.commit()
        return jsonify("Listing added to favourites."), 200
    return jsonify("ERROR: Listing was not found."), 400

# Remove listing from favourites
@app.route("/listing/<ListingID>/favourite", methods=["DELETE"])
@jwt_required()
def unfavourite_listing_page(ListingID): # FUNGERAR
    """
    Function that handles the process of removing a book listing from favourites.
    """
    listing = Listing.query.filter_by(id=ListingID).first()
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity["id"]).first()
    if listing and user:
        if listing not in user.favorites:
            return jsonify("ERROR: Listing is not in favourites."), 400
        user.favorites.remove(listing)
        db.session.commit()
        return jsonify("Listing removed from favourites."), 200
    return jsonify("ERROR: Listing was not found."), 400

@app.route("/listings", methods=["GET"])
@jwt_required()
def listings_page(): # FUNGERAR
    """
    Function that handles the process of displaying all book listings.
    """
    listings = Listing.query.all()
    if listings:
        return jsonify([listing.serialize() for listing in listings]), 200
    return jsonify("ERROR: No listings found."), 400

# Show all favourite listings
@app.route("/listings/favourites", methods=["GET"])
@jwt_required()
def favourites_page(): # FUNGERAR
    """
    Function that handles the process of displaying all favourite book listings.
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity["id"]).first()
    if user and user.favorites:
        return jsonify([listing.serialize() for listing in user.favorites]), 200
    return jsonify("ERROR: No favourites found."), 400

# Show all listings by a specific user
@app.route("/listings/user/<Username>", methods=["GET"])
@jwt_required()
def user_listings_page(Username): # FUNGERAR
    """
    Function that handles the process of displaying all book listings by a specific user.
    """
    user = User.query.filter_by(username=Username).first()
    if user and user.listings:
        return jsonify([listing.serialize() for listing in user.listings]), 200
    return jsonify("ERROR: No listings found."), 400

# Get all listings that have not been viewed by the user
@app.route("/listings/unviewed", methods=["GET"])
@jwt_required()
def unviewed_listings_page(): # FUNGERAR
    """
    Function that handles the process of displaying all book listings that have not been viewed by the user.
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity["id"]).first()
    listings = Listing.query.all()
    if user and listings:
        return jsonify([listing.serialize() for listing in listings if listing not in user.viewed_listings]), 200
    return jsonify("ERROR: No unviewed listings found."), 400

@app.route("/listings/search", methods=["GET"])
@jwt_required(optional=True)
def search_listings_page(): # FUNGERAR
    """
    Function that handles the process of searching for book listings.
    """
    query = request.args.get("query")
    listings = Listing.query.filter(db.or_(Listing.title.ilike(f"%{query}%"), 
                                           Listing.description.ilike(f"%{query}%"),
                                           Listing.location.ilike(f"%{query}%")
                                           )).all() # Lägg till sökning på program och kurs
    if listings:
        return jsonify([listing.serialize() for listing in listings]), 200
    return jsonify("ERROR: No listings found."), 400

# Show all listings of a specific program
@app.route("/listings/program/<ProgramID>", methods=["GET"])
@jwt_required()
def program_listings_page(ProgramID):
    """
    Function that handles the process of displaying all book listings of a specific program.
    """
    program = Program.query.filter_by(id=ProgramID).first()
    if program:
        return jsonify([listing.serialize() for listing in program.listings]), 200
    return jsonify("ERROR: No listings found."), 400

# Show all listings of a specific course
@app.route("/listings/course/<CourseID>", methods=["GET"])
@jwt_required()
def course_listings_page(CourseID):
    """
    Function that handles the process of displaying all book listings of a specific course.
    """
    course = Course.query.filter_by(id=CourseID).first()
    if course:
        return jsonify([listing.serialize() for listing in course.listings]), 200
    return jsonify("ERROR: No listings found."), 400

# ______________________________
# ---------- Chatting ---------- 

@app.route("/listing/<ListingID>/new_chat", methods=["POST"])
@jwt_required()
def new_chat_page(ListingID): # FUNGERAR
    """
    Function that handles the process of creating a new chat.
    """
    user = get_jwt_identity()
    listing = Listing.query.filter_by(id=ListingID).first()
    if not user:
        return redirect("/login")
    if not listing:
        return jsonify("ERROR: Listing was not found."), 400
    if listing.owner_id == user["id"]:
        return jsonify("ERROR: You cannot chat with yourself."), 400
    new_chat = Chat(buyer_id=user["id"], seller_id=listing.owner_id, listing_id=listing.id)
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({"message": "Chat created successfully", "chat_id": new_chat.id}), 200

@app.route("/messages/<ChatID>", methods=["GET"])
@jwt_required()
def chat_page(ChatID): # FUNGERAR
    """
    Function that handles the process of displaying a chat.
    """
    user = get_jwt_identity()
    chat = Chat.query.filter_by(id=ChatID).first()
    if not user:
        return redirect("/login")
    if not chat:
        return jsonify("ERROR: Chat was not found."), 400
    if chat.buyer_id != user["id"] and chat.seller_id != user["id"]:
        return jsonify("ERROR: You are not part of this chat."), 400
    return jsonify({"messages": chat.serialize()["messages"]}), 200

@app.route("/messages/<ChatID>/send", methods=["POST"])
@jwt_required()
def send_message_page(ChatID): # FUNGERAR
    """
    Function that handles the process of sending a message.
    """
    user = get_jwt_identity()
    chat = Chat.query.filter_by(id=ChatID).first()
    if not user:
        return redirect("/login")
    if not chat:
        return jsonify("ERROR: Chat was not found."), 400
    if chat.buyer_id != user["id"] and chat.seller_id != user["id"]:
        return jsonify("ERROR: You are not part of this chat."), 400
    data = request.get_json()
    new_message = Message(
        message=data["message"],
        chat_id=ChatID,
        author_id=user["id"])
    if not new_message:
        return jsonify("ERROR: Message could not be created"), 400
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message sent successfully", "message_id": new_message.id}), 200

@app.route("/chats/all", methods=["GET"])
@jwt_required()
def all_chats_page(): # FUNGERAR
    """
    Function that handles the process of displaying all chats for a user.
    """
    user = get_jwt_identity()
    if not user:
        return redirect("/login")
    chats = Chat.query.filter(db.or_(Chat.buyer_id==user["id"], Chat.seller_id==user["id"])).all()
    if not chats:
        return jsonify("ERROR: No chats found."), 400
    return jsonify([chat.serialize() for chat in chats]), 200

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
# TODO: I profile_page är detta förmodligen onödigt: user = User.query.filter_by(id=identity['id']).first()
                                                        # if not user:
                                                            # return redirect("/login", 400)
# TODO: Fixa att validate password inte validerar det hashade passwordet
# TODO: I edit_listings_page och i edit_profile_page och i andra också är detta förmodligen onödigt if not user:
                                                                                                      # return redirect("/login")

