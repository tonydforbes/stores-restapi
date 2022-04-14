import sqlite3
from flask_restful import Resource, Api, reqparse
from flask import Flask,request,jsonify
from models.user import UserModel


class Users(Resource):

    #@classmethod
    def get(self):
        return {"users": [user.json() for user in UserModel.query.all()]}

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username",type=str,required=True,help="The username is a required parameter")
    parser.add_argument("password",type=str,required=True,help="The password is a required parameter")

    def post(self):

        request_data = UserRegister.parser.parse_args()

        # Validate that the user does not already exist
        user = UserModel.find_by_username(request_data["username"])

        if user:
            return {"error":f"User {request_data['username']} already exists"},400

        # Insert the new user
        new_user = UserModel(request_data["username"],request_data["password"])
        new_user.insert()

        return new_user.json(), 201
