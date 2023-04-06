import os
import tempfile
import pytest
import app

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
        app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE_FILE_PATH'])

def test_check_if_token_revoked(client):
    pass

def test_home_page(client):
    pass

def test_login_page(client):
    pass

def test_signup_page(client):
    pass

def test_logout_page(client):
    pass

def test_profile_page(client):
    pass

def test_edit_profile_page(client):
    pass

def test_delete_profile_page(client):
    pass

def test_add_listing_page(client):
    pass

def test_edit_listing_page(client):
    pass

def test_delete_listing_page(client):
    pass

def test_listings_page(client):
    pass

def test_listing_page(client):
    pass

def test_search_listings_page(client):
    pass

def test_all_chats_page(client):
    pass

def test_chat_page(client):
    pass
