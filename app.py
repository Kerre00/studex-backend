from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timezone, datetime, timedelta
from data_handler import db, User, bcrypt, app, Message, TokenBlocklist, Listing, jwt, Chat, Program, Course, course_listings, program_listings, favorite_listings, init_db
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
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({"message": "Welcome to Studex!", "status": "You are logged in as {}".format(current_user)}), 200
    return jsonify({"message": "Welcome to Studex!", "status": "You are not logged in. Please make an account."}), 200

# _________________________________________
# ---------- User authentication ---------- 

@app.route("/login", methods=["POST"])
def login_page(): #FUNGERAR
    """
    Function that handles the login process for users.
    """
    data = request.get_json()
    username = data["username"].lower()
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        # if user.is_online():
        #     return jsonify({"message": "User is already logged in."}), 400
        access_token = create_access_token(identity=user.serialize(), expires_delta=timedelta(hours=1))
        user.login()
        return jsonify({"message": "Successfully logged in", "token": access_token, "id": user.id}), 200
    return jsonify({"message": "Invalid username or password."}), 401

@app.route("/signup", methods=["POST"])
def signup_page(): #FUNGERAR
    """
    Function that handles the signup process for users.
    """
    data = request.get_json()
    username = data["username"].lower()
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists."}), 400
    if User.query.filter_by(email=data["email"]).first(): 
        return jsonify({"message": "Email is already used."}), 400
    if User.query.filter_by(phone_number=data.get("phone_number")).first() and data.get("phone_number"):
        return jsonify({"message": "Phone number is already used."}), 400

    # Initialize user with default values for optional arguments
    new_user = User(
        username=username, 
        password=data["password"], 
        email=data["email"], 
        first_name=data.get("first_name"), 
        last_name=data.get("last_name"), 
        phone_number=data.get("phone_number")

    )

    db.session.add(new_user)

    db.session.commit()
    return jsonify({"message": "Successfully signed up"}), 200


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
    return jsonify({"message": "Successfully logged out"}), 200

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
    db.session.add(TokenBlocklist(jti=get_jwt()["jti"]))
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted successfully"}), 200

# _________________________________________
# ---------- Listings management ---------- 

@app.route("/listing/add", methods=["POST"])
@jwt_required()
def add_listing_page(): #FUNGERAR HALVT KOLLA LISTING_COURSE + LISTING_PROGRAM
    """
    Function that handles the process of adding a new book listing.
    """
    user = get_jwt_identity()
    data = request.get_json()

    new_listing = Listing(
        title=data.get("title"), 
        price=data.get("price"), 
        owner_id=user["id"],
        location=data.get("location"),
        description=data.get("description"),
        image=data.get("image"))

    if not new_listing.title:
        return jsonify({"message": "Title is missing"}), 400
    if not new_listing.price:
        return jsonify({"message": "Price is missing"}), 400

    if not new_listing:
        return jsonify({"message": "Listing could not be created"}), 400

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

    if not listing:
        return jsonify({"message": "Listing not found"}), 400
    if listing.owner_id != user['id']:
        return jsonify({"message": "You are not the owner of this listing"}), 400
    data = request.get_json()   

    listing.title = data.get("title", listing.title)
    listing.price = data.get("price", listing.price)
    listing.location = data.get("location", listing.location)
    listing.description = data.get("description", listing.description)
    listing.image = data.get("image", listing.image)
    # listing.course = data.get("course", listing.course)
    # listing.program = data.get("program", listing.program)

    db.session.commit()
    return jsonify({"message": "Listing updated successfully", "listing_id": listing.id}), 200


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
    return jsonify({"message": "Listing was not found."}), 400

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
    return jsonify({"message": "Listing was not found."}), 400

# Add listing to favorites
@app.route("/listing/<ListingID>/favorite", methods=["POST"])
@jwt_required()
def favorite_listing_page(ListingID): # FUNGERAR
    """
    Function that handles the process of adding a book listing to favorites.
    """
    listing = Listing.query.filter_by(id=ListingID).first()
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity["id"]).first()
    if listing and identity:
        if listing in user.favorites:
            return jsonify({"message": "Listing is already in favorites."}), 400
        user.favorites.append(listing)
        db.session.commit()
        return jsonify({"message": "Listing added to favorites."}), 200
    return jsonify({"message": "Listing was not found."}), 400

# Remove listing from favorites
@app.route("/listing/<ListingID>/favorite", methods=["DELETE"])
@jwt_required()
def unfavorite_listing_page(ListingID): # FUNGERAR
    """
    Function that handles the process of removing a book listing from favorites.
    """
    listing = Listing.query.filter_by(id=ListingID).first()
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity["id"]).first()
    if listing and user:
        if listing not in user.favorites:
            return jsonify({"message": "Listing is not in favorites."}), 400
        user.favorites.remove(listing)
        db.session.commit()
        return jsonify({"message": "Listing removed from favorites."}), 200
    return jsonify({"message": "Listing was not found."}), 400

@app.route("/listings", methods=["GET"])
@jwt_required(optional=True)
def listings_page(): # FUNGERAR
    """
    Function that handles the process of displaying all book listings.
    """
    listings = Listing.query.all()
    if listings:
        return jsonify([listing.serialize() for listing in listings]), 200
    return jsonify({"message": "No listings found."}), 400

# Show all favorite listings
@app.route("/listings/favorites", methods=["GET"])
@jwt_required()
def favorites_page(): # FUNGERAR
    """
    Function that handles the process of displaying all favorite book listings.
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity["id"]).first()
    if user:
        return jsonify([listing.serialize() for listing in user.favorites]), 200
    return jsonify({"message": "No favorites found."}), 400

# Show all listings by a specific user
@app.route("/listings/user/<Username>", methods=["GET"])
@jwt_required(optional=True)
def user_listings_page(Username): # FUNGERAR
    """
    Function that handles the process of displaying all book listings by a specific user.
    """
    user = User.query.filter_by(username=Username).first()
    if user and user.listings:
        return jsonify([listing.serialize() for listing in user.listings]), 200
    return jsonify({"message": "No listings found."}), 400

# Get all listings that have not been viewed by the user
@app.route("/listings/unviewed", methods=["GET"])
@jwt_required()
def unviewed_listings_page(): # FUNGERAR
    """
    Function that handles the process of displaying all book listings that 
    have not been viewed by the user.
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity["id"]).first()
    listings = Listing.query.all()
    unviewed_listings = []
    for listing in listings:
        if listing not in user.viewed_listings:
            unviewed_listings.append(listing)

    if user and unviewed_listings:
        return jsonify([listing.serialize() for listing in listings if listing not in user.viewed_listings]), 200
    return jsonify({"message": "No unviewed listings found."}), 400

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
    return jsonify({"message": "No listings found."}), 400

# Show all listings of a specific program
@app.route("/listings/program/<ProgramID>", methods=["GET"])
@jwt_required(optional=True)
def program_listings_page(ProgramID):
    """
    Function that handles the process of displaying all book listings of a specific program.
    """
    program = Program.query.filter_by(id=ProgramID).first()
    if program:
        return jsonify([listing.serialize() for listing in program.listings]), 200
    return jsonify({"message": "No listings found."}), 400

# Show all listings of a specific course
@app.route("/listings/course/<CourseID>", methods=["GET"])
@jwt_required(optional=True)
def course_listings_page(CourseID):
    """
    Function that handles the process of displaying all book listings of a specific course.
    """
    course = Course.query.filter_by(id=CourseID).first()
    if course:
        return jsonify([listing.serialize() for listing in course.listings]), 200
    return jsonify({"message": "No listings found."}), 400

# ______________________________
# ---------- Chatting ---------- 

@app.route("/listing/<ListingID>/new_chat", methods=["POST"])
@jwt_required(optional=True)
def new_chat_page(ListingID): # FUNGERAR
    """
    Function that handles the process of creating a new chat.
    """
    user = get_jwt_identity()
    if user:
        listing = Listing.query.filter_by(id=ListingID).first()
        if not listing:
            return jsonify({"message": "Listing was not found."}), 400
        if listing.owner_id == user["id"]:
            return jsonify({"message": "You cannot chat with yourself."}), 400
        new_chat = Chat(buyer_id=user["id"], seller_id=listing.owner_id, listing_id=listing.id)
        db.session.add(new_chat)
        db.session.commit()
        return jsonify({"message": "Chat created successfully", "chat_id": new_chat.serialize()}), 200
    return jsonify({"message": "You must be logged in to chat."}), 400

@app.route("/messages/<ChatID>", methods=["GET"])
@jwt_required()
def chat_page(ChatID): # FUNGERAR
    """
    Function that handles the process of displaying a chat.
    """
    user = get_jwt_identity()
    chat = Chat.query.filter_by(id=ChatID).first()
    if not chat:
        return jsonify({"message": "Chat was not found."}), 400
    if chat.buyer_id != user["id"] and chat.seller_id != user["id"]:
        return jsonify({"message": "You are not part of this chat."}), 400
    
    messages = Message.query.filter_by(chat_id=ChatID).all()

    if messages:
        return jsonify([message.serialize() for message in messages]), 200
    
    return jsonify({"message": "No messages found."}), 400
    # return jsonify({"messages": chat.serialize()["messages"]}), 200 -------------------------------------------------------------------------------------

@app.route("/messages/<ChatID>/send", methods=["POST"])
@jwt_required()
def send_message_page(ChatID): # FUNGERAR
    """
    Function that handles the process of sending a message.
    """
    user = get_jwt_identity()
    chat = Chat.query.filter_by(id=ChatID).first()
    if not chat:
        return jsonify({"message": "Chat was not found."}), 400
    if chat.buyer_id != user["id"] and chat.seller_id != user["id"]:
        return jsonify({"message": "You are not part of this chat."}), 400
    data = request.get_json()
    new_message = Message(
        message=data["message"],
        chat_id=ChatID,
        author_id=user["id"])
    if not new_message:
        return jsonify({"message": "Message could not be created"}), 400
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
    chats = Chat.query.filter(db.or_(Chat.buyer_id==user["id"], Chat.seller_id==user["id"])).all()
    if not chats:
        return jsonify({"message": "No chats found."}), 400
    return jsonify([chat.serialize() for chat in chats]), 200

# -------------------------------------Initialize courses and programs-------------------------------------

def add_courses_and_programs():
    # This is the list of courses that are available
    courses = [
        {"id": 1, "name": "Biologi"}, 
        {"id": 2, "name": "Fysik"}, 
        {"id": 3, "name": "Kemi"}, 
        {"id": 4, "name": "Matematik"}, 
        {"id": 5, "name": "Programmering"}, 
        {"id": 6, "name": "Teknik"}, 
        {"id": 7, "name": "Språk"}, 
        {"id": 8, "name": "Historia"}, 
        {"id": 9, "name": "Geografi"}, 
        {"id": 10, "name": "Samhällskunskap"}, 
        {"id": 11, "name": "Religion"}, 
        {"id": 12, "name": "Ekonomi"}, 
        {"id": 13, "name": "Juridik"}, 
        {"id": 14, "name": "Medicin"}, 
        {"id": 15, "name": "Psykologi"}, 
        {"id": 16, "name": "Sociologi"}, 
        {"id": 17, "name": "Filosofi"}, 
        {"id": 18, "name": "Musik"}, 
        {"id": 19, "name": "Konst"}, 
        {"id": 20, "name": "Sport"}, 
        {"id": 21, "name": "Naturvetenskap"}, 
        {"id": 22, "name": "Samhällsvetenskap"}, 
        {"id": 23, "name": "Humaniora"}, 
        {"id": 24, "name": "Teknik och naturvetenskap"}, 
        {"id": 25, "name": "Samhällsvetenskap och humaniora"}, 
        {"id": 26, "name": "Alla ämnen"}
        ]

    # This is the list of programs that are available
    programs = [
        {"id": 1, "name": "Civilingenjör inom mjukvaruteknik"},
        {"id": 2, "name": "Civilingenjör inom datateknik"},
        {"id": 3, "name": "Civilingenjör inom datavetenskap"},
        {"id": 4, "name": "Civilingenjör inom datalogi"},
        {"id": 5, "name": "Civilingenjör inom industriell ekonomi"},
        {"id": 6, "name": "Civilingenjör inom maskinteknik"},
        {"id": 7, "name": "Civilingenjör inom materialvetenskap"},
        {"id": 8, "name": "Civilingenjör inom teknisk fysik"},
        {"id": 9, "name": "Civilingenjör inom teknisk matematik"},
        {"id": 10, "name": "Civilingenjör inom teknisk nanovetenskap"}
        ]

    # Add the courses to the database
    for course in courses:
        db.session.add(Course(name=course["name"]))

    # Add the programs to the database
    for program in programs:
        db.session.add(Program(name=program["name"]))

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    app.debug = True
    # add_courses_and_programs()
    app.run(port='5000')


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

