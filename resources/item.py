import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    # Note that there is no self in front, so the parser does not belong to a specific instance of the class
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

    @jwt_required()  # We will have to authenticate before we can call the GET method
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400  # This is a bad request,

        # This data variable is defined here to follow an error-first approach style. If the item already exists,
        # the code above would stop the execution by returning, so we would not have to query the argparser.
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # internal server error

        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()  # Note that we've only added price to the argparser so any other
                                         # arguments will not be assigned to data
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item.json()


# Creating the ItemList resource
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}

