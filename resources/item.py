from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import sqlite3
from models.item import ItemModel

class Items(Resource):

    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",type=float,required=True,help="The price is a required value and it must be a numeric")
    parser.add_argument("store_id",type=int,required=True,help="An item must be linked to a store")

    @jwt_required()
    def get(self, item_name):
        item = ItemModel.look_for_item_in_db(item_name)
        if item:
            return {"item": item.json()},200
        else:
            return {"error":f"Item {item_name} does not exist"},404

    def post(self, item_name):

        request_data = Item.parser.parse_args()

        #Validate that item does not already exist
        if ItemModel.look_for_item_in_db(item_name):
            return {"error":f"Item {item_name} already exists"},400

        # Initialise the new item object
        new_item = ItemModel(item_name,request_data["price"],request_data["store_id"])

        # Add the new item to the database
        try:
            new_item.save_to_db()
        except:
            return {"message":"Error occurred"}, 500

        return {"message":"Successfully added item","item":new_item.json()}, 201

    @jwt_required()
    def delete(self,item_name):

        item = ItemModel.look_for_item_in_db(item_name)

        if item == None:
            return {"message": f"{item_name} is not a valid item"}

        item.delete_from_db()

        return {"message": f"{item_name} has been deleted"}

    @jwt_required()
    def put(self,item_name):

        request_data = Item.parser.parse_args()

        message = "Item has been updated"

        item = ItemModel.look_for_item_in_db(item_name)

        if item == None:               #Add new item if name not found
            item = ItemModel(item_name,request_data["price"],request_data["store_id"])
            message = "New item has been added"
        else:                           # Update the item
            item.price = request_data["price"]
            item.store_id = request_data["store_id"]

        item.save_to_db()

        return {"message": message, "item":item.json()}
