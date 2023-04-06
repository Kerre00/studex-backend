import requests
import json

# # Get the data from the API
url = "http://127.0.0.1:5000/"

# Create a new account
data = {"username": "Elle69", 
        "password": "test",
        "email": "Elliotana@testmail.com",
        "phone_number": "531503203",
        "first_name": "Elliotana",
        "last_name": "Söderströmana"}

r = requests.post(url + "signup", json=data, verify=False)
print(r.text)

# login to that account
data = {"username": "Elle69", "password": "test"}
r2 = requests.post(url + "login", json=data, verify=False)
# print(r2.text)

# Get the token
token = r2.json()["token"]
# print(token, "---------------------------------------------")

# Create a new post
# Send header with token
headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
data = {"title": "test", "description": "test", "price": 10}
r3 = requests.post(url + "listing/add", json=data, verify=False, headers=headers)
print(r3.text)

# Create another account
data = {"username": "Kerre", "password": "test", "email": "lol@loller.se", "phone_number": "072-1525631", "first_name": "Kevin", "last_name": "Rintanen Österblad"}
r4 = requests.post(url + "signup", json=data, verify=False)

# Login to that account
data = {"username": "Kerre", "password": "test"}
r5 = requests.post(url + "login", json=data, verify=False)

# Get the token
token2 = r5.json()["token"]

# Send header with token
headers2 = {"Content-Type": "application/json", "Authorization": "Bearer " + token2}

# Create new chat on the post

print(r3.json()["listing_id"] + "---------------------------------------------")
data = {"listing_id": r3.json()["listing_id"]}
r6 = requests.post(url + "listing/" + data["listing_id"] + "/new_chat", json=data, verify=False, headers=headers2)
print(r6.text)


# Get the chat id
chat_id = r6.json()["chat_id"]

# Send a message to the chat
data = {"chat_id": chat_id, "message": "Hello Elliotana, I am interested in your book!"}
r7 = requests.post(url + "messages/" + data["chat_id"] + "/send", json=data, verify=False, headers=headers2)
print(r7.text)
