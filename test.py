import requests
import json

# Get the data from the API
url = "http://127.0.0.1:5000/"

# Create a new account
data = {"username": "test", 
        "password": "test",
        "email": "test@testmail.com",
        "phone_number": "1234567890"}

r = requests.post(url + "signup", json=data, verify=False)
print(r.text)

# Login
# r2 = requests.post(url + "login", data=data, verify=False)
# print(r2.text)

# # Get the token
# token = json.loads(r2.text)["token"]

# # Create a new post
# data = {"title": "test", "price": "100", "description": "test", "isbn": "1234567890", "location": "test", "description": "test", "token": token}
# r3 = requests.post(url + "listing/add", data=data, verify=False)