import os
import tempfile
import pytest
import app
import data_handler

import json
import requests

from flask_jwt_extended import (
JWTManager, jwt_required, create_access_token, get_jwt, get_jwt_identity
)

base_url = "http://127.0.0.1:5000"

@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE_FILE_PATH'] = tempfile.mkstemp()
    app.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + app.app.config['SQLALCHEMY_DATABASE_URI']
    app.app.config['TESTING'] = True

    client = app.app.test_client()


    with app.app.app_context():
        data_handler.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE_FILE_PATH'])

def test_check_if_token_revoked(client):
    pass

def test_home_page(client):
    pass

def test_signup_page(client):
    # Signing up a user with only mandatory data
    payload = {'username': 'testuser1', 'password': '123abcABC', 'email': 'test1@gmail.com'}
    r = client.post('/signup', json=payload, content_type='application/json')
    assert r.status_code == 200
 
    # Signing up a user with optional data
    payload = {'username': 'testuser2', 'password': '123abcABC', 'email': 'test2@gmail.com',
        'phone_number': '1234567890', 'first_name': 'testfirst', 'last_name': 'testlast'}
    r = client.post('/signup', json=payload, content_type='application/json')
    assert r.status_code == 200

    # Signing up a user with an existing username
    payload = {'username': 'testuser1', 'password': '123abcABC', 'email': 'test3@gmail.com'}
    r = client.post('/signup', json=payload, content_type='application/json')
    assert r.status_code == 400
    assert r.get_json() == 'ERROR: Username already exists.'

    # Signing up a user with an existing email
    payload = {'username': 'testuser3', 'password': '123abcABC', 'email': 'test1@gmail.com'}
    r = client.post('/signup', json=payload, content_type='application/json')
    assert r.status_code == 400
    assert r.get_json() == 'ERROR: Email is already used.'


def test_login_page(client):
    # Signing up a user
    password = '123abcABC'
    username = 'testuser1'
    payload = {'username': username, 'password': password, 'email': 'test1@gmail.com'}
    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the user
    payload = {'username': username, 'password': password}
    r = client.post('/login', json=payload, content_type='application/json')
    assert r.status_code == 200
    assert r.get_json()['message'] == 'Successfully logged in'

    # Logging in the user with the wrong password
    payload = {'username': username, 'password': 'WrongPassword123'}
    r = client.post('/login', json=payload, content_type='application/json')
    assert r.status_code == 401
    assert r.get_json() == 'ERROR: Invalid username or password.'

    # Logging in the user with the wrong username
    payload = {'username': 'wrongusername', 'password': password}
    r = client.post('/login', json=payload, content_type='application/json')
    assert r.status_code == 401
    assert r.get_json() == 'ERROR: Invalid username or password.'


def test_logout_page(client):
    # Signing up a user
    password = '123abcABC'
    username = 'testuser1'
    payload = {'username': username, 'password': password, 'email': 'test1@gmail.com'}
    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the user
    payload = {'username': username, 'password': password}
    r = client.post('/login', json=payload, content_type='application/json')
    token = r.get_json()['token']

    # Logging out the user
    r = client.post('/logout', headers={"Authorization": "Bearer " + token})
    assert r.status_code == 200

    # Logging out the same user again
    r = client.post('/logout', headers={"Authorization": "Bearer " + token})
    assert r.status_code == 401


def test_profile_page(client):
    # Signing up a user
    password = '123abcABC'
    username = 'testuser1'
    email = 'test1@gmail.com'
    phone_number = '1234567890'
    first_name = 'testfirst'
    last_name = 'testlast'
    payload = {'username': username, 'password': password, 'email': email,
    'phone_number': phone_number, 'first_name': first_name, 'last_name': last_name}
    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the user
    payload = {'username': username, 'password': password}
    r = client.post('/login', json=payload, content_type='application/json')
    token = r.get_json()['token']

    # Accessing the profile page of the user
    r = client.get('/profile', headers={"Authorization": "Bearer " + token})
    assert r.status_code == 200
    assert r.get_json()['username'] == username
    assert r.get_json()['email'] == email
    assert r.get_json()['phone_number'] == phone_number
    assert r.get_json()['first_name'] == first_name
    assert r.get_json()['last_name'] == last_name


def test_edit_profile_page(client):
    # Signing up a user
    password = '123abcABC'
    username = 'testuser1'
    email = 'test1@gmail.com'
    phone_number = '1234567890'
    first_name = 'testfirst'
    last_name = 'testlast'
    payload = {'username': username, 'password': password, 'email': email,
    'phone_number': phone_number, 'first_name': first_name, 'last_name': last_name}
    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the user
    payload = {'username': username, 'password': password}
    r = client.post('/login', json=payload, content_type='application/json')
    token = r.get_json()['token']

    # Editing all of the users information
    new_first_name = 'newtestfirst'
    new_last_name = 'newtestlast'
    new_phone_number = '01234567890'
    new_password = 'new123abcABC'
    payload = {'password': new_password, 'phone_number': new_phone_number,
    'first_name': new_first_name, 'last_name': new_last_name}
    
    r = client.put('/profile', json=payload, headers={"Authorization": "Bearer " + token})
    assert r.status_code == 200
    assert r.get_json()['message'] == 'Profile updated successfully'

    # Editing only one of the users information
    new_password = 'new123abcABC'
    payload = {'password': new_password}
    
    r = client.put('/profile', json=payload, headers={"Authorization": "Bearer " + token})
    assert r.status_code == 200
    assert r.get_json()['message'] == 'Profile updated successfully'


def test_delete_profile_page(client):
    # Signing up a user
    password = '123abcABC'
    username = 'testuser1'
    email = 'test1@gmail.com'

    payload = {'username': username, 'password': password, 'email': email}
    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the user
    payload = {'username': username, 'password': password}
    r = client.post('/login', json=payload, content_type='application/json')
    token = r.get_json()['token']

    # Deleting the user
    r = client.delete('profile/delete', headers={"Authorization": "Bearer " + token})
    assert r.status_code == 200

def test_add_listing_page(client):
    # Signing up a user
    password = '123abcABC'
    username = 'testuser1'
    email = 'test1@gmail.com'

    payload = {'username': username, 'password': password, 'email': email}
    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the user
    payload = {'username': username, 'password': password}
    r = client.post('/login', json=payload, content_type='application/json')
    token = r.get_json()['token']

    # Adding a listing
    listing_title = 'testlisting'
    price = '123'
    payload = {'price': price, 'title': listing_title}

    r = client.post('/listing/add', json=payload, headers={"Authorization": "Bearer " + token})
    assert r.status_code == 200
    assert r.get_json()['message'] == 'Listing has been posted'

    # Adding a listing with all of the optional data
    listing_title = 'testlisting'
    price = '123'
    location = 'testlocation'
    description = 'testdescription'
    payload = {'price': price, 'title': listing_title, 'location': location, 'description': description}

    r = client.post('/listing/add', json=payload, headers={"Authorization": "Bearer " + token})

    # Adding a listing without the mandatory data
    price = '123'
    payload = {'price': price}

    r = client.post('/listing/add', json=payload, headers={"Authorization": "Bearer " + token})
    assert r.status_code == 400
    assert r.get_json() == 'ERROR: Listing could not be created'


def test_edit_listing_page(client):
    # Signing up a user
    password = '123abcABC'
    username = 'testuser1'
    email = 'test1@gmail.com'
    payload = {'username': username, 'password': password, 'email': email}

    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the user
    payload = {'username': username, 'password': password}

    r = client.post('/login', json=payload, content_type='application/json')
    token1 = r.get_json()['token']

    # Adding a listing with all of the optional data
    listing_title = 'testlisting'
    price = '123'
    location = 'testlocation'
    description = 'testdescription'
    payload = {'price': price, 'title': listing_title, 'location': location, 'description': description}

    r = client.post('/listing/add', json=payload, headers={"Authorization": "Bearer " + token1})
    listing_id = r.get_json()['listing_id']

    # Editing all of the listings information
    new_listing_title = 'newtestlisting'
    new_price = '1123'
    new_location = 'newtestlocation'
    new_description = 'newtestdescription'
    payload = {'price': new_price, 'title': new_listing_title, 'location': new_location, 'description': new_description}

    r = client.put(f'/listing/edit/{listing_id}', json=payload, headers={"Authorization": "Bearer " + token1})
    assert r.status_code == 200

    # Editing only one of the listings information
    new_listing_title = 'newtestlisting2'
    payload = {'title': new_listing_title}

    r = client.put(f'/listing/edit/{listing_id}', json=payload, headers={"Authorization": "Bearer " + token1})
    assert r.status_code == 200

     # Editing a listing with the wrong listing id
    new_listing_title = 'newtestlisting2'
    payload = {'title': new_listing_title}

    r = client.put('/listing/edit/wronglistingid', json=payload, headers={"Authorization": "Bearer " + token1})
    assert r.status_code == 400
    assert r.get_json() == 'ERROR: Listing not found'

    # Signing up another user
    password = '123abcABC'
    username = 'testuser2'
    email = 'test2@gmail.com'
    payload = {'username': username, 'password': password, 'email': email}

    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the new user
    payload = {'username': username, 'password': password}

    r = client.post('/login', json=payload, content_type='application/json')
    token2 = r.get_json()['token']

    # Editing the listing with another user
    new_listing_title = 'newtestlisting2'
    payload = {'title': new_listing_title}

    r = client.put(f'/listing/edit/{listing_id}', json=payload, headers={"Authorization": "Bearer " + token2})
    assert r.status_code == 400
    assert r.get_json() == 'ERROR: You are not the owner of this listing'
    

def test_delete_listing_page(client):
    # Signing up a user
    password = '123abcABC'
    username = 'testuser1'
    email = 'test1@gmail.com'
    payload = {'username': username, 'password': password, 'email': email}

    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the user
    payload = {'username': username, 'password': password}

    r = client.post('/login', json=payload, content_type='application/json')
    token1 = r.get_json()['token']

    # Adding a listing with all of the optional data
    listing_title = 'testlisting'
    price = '123'
    location = 'testlocation'
    description = 'testdescription'
    payload = {'price': price, 'title': listing_title, 'location': location, 'description': description}

    r = client.post('/listing/add', json=payload, headers={"Authorization": "Bearer " + token1})
    listing_id = r.get_json()['listing_id']

    # Deleting the listing
    r = client.delete(f'/listing/delete/{listing_id}', headers={"Authorization": "Bearer " + token1})
    assert r.status_code == 200
    assert r.get_json()['message'] == 'Listing deleted successfully'

    # Deleting the listing with the wrong listing id
    r = client.delete('/listing/delete/wronglistingid', headers={"Authorization": "Bearer " + token1})
    assert r.status_code == 400
    assert r.get_json() == 'ERROR: Listing was not found.'

    # Signing up another user
    password = '123abcABC'
    username = 'testuser2'
    email = 'test2@gmail.com'
    payload = {'username': username, 'password': password, 'email': email}

    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the new user
    payload = {'username': username, 'password': password}

    r = client.post('/login', json=payload, content_type='application/json')
    token2 = r.get_json()['token']

    # Deleting the listing with another user
    r = client.delete(f'/listing/delete/{listing_id}', headers={"Authorization": "Bearer " + token2})
    assert r.status_code == 400
    assert r.get_json() == 'ERROR: Listing was not found.'


def test_listings_page(client):
    # Signing up a user
    password = '123abcABC'
    username = 'testuser1'
    email = 'test1@gmail.com'
    payload = {'username': username, 'password': password, 'email': email}

    r = client.post('/signup', json=payload, content_type='application/json')
    
    # Logging in the user
    payload = {'username': username, 'password': password}

    r = client.post('/login', json=payload, content_type='application/json')
    token1 = r.get_json()['token']

    # Getting the listings when there are no listings
    r = client.get('/listings', headers={"Authorization": "Bearer " + token1})
    assert r.status_code == 400
    assert r.get_json() == 'ERROR: No listings found.'

    # Adding a listing with all of the optional data
    listing_title = 'testlisting1'
    price = '123'
    location = 'testlocation'
    description = 'testdescription'
    payload = {'price': price, 'title': listing_title, 'location': location, 'description': description}

    r = client.post('/listing/add', json=payload, headers={"Authorization": "Bearer " + token1})
    listing_id1 = r.get_json()['listing_id']

    # Adding another listing with all of the optional data
    listing_title = 'testlisting2'
    price = '123'
    location = 'testlocation'
    description = 'testdescription'
    payload = {'price': price, 'title': listing_title, 'location': location, 'description': description}

    r = client.post('/listing/add', json=payload, headers={"Authorization": "Bearer " + token1})
    listing_id2 = r.get_json()['listing_id']

    # Getting the listings
    r = client.get('/listings', headers={"Authorization": "Bearer " + token1})
    assert r.status_code == 200




def test_listing_page(client):
    pass

def test_search_listings_page(client):
    pass

def test_all_chats_page(client):
    pass

def test_chat_page(client):
    pass
