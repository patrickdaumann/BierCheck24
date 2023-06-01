from faker import Faker
import json
from django.contrib.auth.hashers import make_password


faker = Faker()

Users = []
PKOffset = 20
NumOfUsers = 1000

Usernames = []

while len(Usernames) < NumOfUsers:
    newname = faker.user_name()
    if newname not in Usernames:
        Usernames.append(newname)


for i in range(len(Usernames)):
    data = {
            "model": "auth.user",
            "pk": i+PKOffset,
            "fields": {
                "username": Usernames[i],
                "password": "Password123"
            }
        }
    Users.append(data)

JSONString = json.dumps(Users)
with open("./Rating/fixtures/Users.json", "w") as f:
    f.write(JSONString)
