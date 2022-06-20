from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = "testRestApi"
api = Api(app)

# This creates a new endpoint, /auth
# When we call /auth, we send it a username and a password and the JWT
# extension gets the username and password and sends it over to the authenticate function
# in the function, we compare the password and if they match, we return the user and that
# becomes the identity. What happens next is that the /auth endpoint returns a JWT
# That JWT in itself does not do anything, but we can send it to the next request we make
# When we send a JWT, what the JWT library does is it calls the identity function to get the
# user_id and get the correct user
# If it can do that, it means that the user was authenticated
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    # Flask has the debug argument that returns an HTML page with the errors
    app.run(port=5000, debug=True)