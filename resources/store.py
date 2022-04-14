from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel
from models.store import StoreModel

class Stores(Resource):

    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}


class Store(Resource):

    parser = reqparse.RequestParser()
    #parser.add_argument("price",type=float,required=True,help="The price is a required value and it must be a numeric")
    #parser.add_argument("store_id",type=int,required=True,help="An item must be linked to a store")

    @jwt_required()
    def get(self, store_name):
        store = StoreModel.look_for_store_in_db(store_name)
        if item:
            return {"store": store.json()},200
        else:
            return {"error":f"Store {store_name} does not exist"},404

    def post(self, store_name):

        #request_data = request.get_json()

        #Validate that store does not already exist
        if StoreModel.look_for_store_in_db(store_name):
            return {"error":f"Store {store_name} already exists"},400

        # Initialise the new store object
        print(f"New store: {store_name}")
        new_store = StoreModel(store_name)
        print(f"New store: {new_store.store_name}")

        # Add the new store to the database
        try:
            new_store.save_to_db()
        except:
            return {"message":"Error occurred"}, 500

        return {"message":"Successfully added store","store":new_store.json()}, 201

    @jwt_required()
    def delete(self,store_name):

        store = StoreModel.look_for_store_in_db(store_name)

        if store == None:
            return {"message": f"{store_name} is not a valid store"}

        try:
            store.delete_from_db()
        except:
            return {"message": f"{store_name} could not be deleted"}

        return {"message": f"{store_name} has been deleted"}
