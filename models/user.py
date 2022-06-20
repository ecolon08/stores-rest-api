import sqlite3


# In this file, we will create a User object
class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # The parameters always have to be in the form of a tuple

        # Let's fetch the first row from the result set. If there are no rows, we get None back
        row = result.fetchone()
        if row is not None:
            user = cls(*row)  # Expand a set of positional arguments
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))

        row = result.fetchone()
        if row is not None:
            user = cls(*row)
        else:
            user = None
        return user
