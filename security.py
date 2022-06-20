from models.user import UserModel


# Function to authenticate our users given a username and a password
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and user.password == password:
        return user


# This identity function is unique to Flask-JWT
# It takes in a payload with the content of the JWT token
# We extract the user_id from that payload, and once we have this
# we can retrieve the specific user that matches this payload
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)