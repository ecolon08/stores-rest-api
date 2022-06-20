import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


# Let's create a new resource to allow users to register
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username field must not be blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password field must not be blank!")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']) is not None:
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created successfully'}, 201
